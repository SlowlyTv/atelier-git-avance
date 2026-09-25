#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
APP_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$APP_DIR"

STATE_FILE=deploy/active-color
ACTIVE_COLOR=$(cat "$STATE_FILE" 2>/dev/null || printf blue)
if [[ "$ACTIVE_COLOR" == blue ]]; then
  INACTIVE_COLOR=green
  INACTIVE_PORT=5002
else
  INACTIVE_COLOR=blue
  INACTIVE_PORT=5001
fi

SERVICE="app-$INACTIVE_COLOR"
EXPECTED_SHA=${EXPECTED_SHA:-${GITHUB_SHA:-development}}
DEPLOY_SHA=${DEPLOY_SHA:-$EXPECTED_SHA}
export DEPLOY_SHA

cleanup_candidate() {
  docker compose --profile "$INACTIVE_COLOR" stop "$SERVICE" >/dev/null 2>&1 || true
  docker compose --profile "$INACTIVE_COLOR" rm -f "$SERVICE" >/dev/null 2>&1 || true
}

fail_deployment() {
  echo "Deployment rejected; $ACTIVE_COLOR remains active" >&2
  cleanup_candidate
  exit 1
}

if [[ -n "${APP_IMAGE:-}" ]]; then
  docker pull "$APP_IMAGE"
  START_MODE=(--no-build)
else
  START_MODE=(--build)
fi

docker compose up -d redis nginx
docker compose --profile "$INACTIVE_COLOR" up -d --no-deps "${START_MODE[@]}" "$SERVICE"

READY=false
for attempt in $(seq 1 20); do
  if curl -fsS --max-time 3 "http://localhost:$INACTIVE_PORT/health" >/dev/null; then
    READY=true
    break
  fi
  echo "Waiting for $SERVICE ($attempt/20)"
  sleep 2
done
[[ "$READY" == true ]] || fail_deployment

STATUS_JSON=$(curl -fsS --max-time 3 "http://localhost:$INACTIVE_PORT/status") || fail_deployment
STATUS_JSON="$STATUS_JSON" EXPECTED_COLOR="$INACTIVE_COLOR" EXPECTED_SHA="$EXPECTED_SHA" python - <<'PY' || fail_deployment
import json
import os

status = json.loads(os.environ["STATUS_JSON"])
assert status["deploy_color"] == os.environ["EXPECTED_COLOR"]
assert status["commit_sha"] == os.environ["EXPECTED_SHA"]
print(f"Smoke test OK: {status['deploy_color']} {status['commit_sha']}")
PY

cp "deploy/nginx-$INACTIVE_COLOR.conf" deploy/nginx.conf
docker compose exec -T nginx nginx -s reload
sleep 1

LIVE_JSON=$(curl -fsS --max-time 5 http://localhost:8080/status) || fail_deployment
LIVE_JSON="$LIVE_JSON" EXPECTED_COLOR="$INACTIVE_COLOR" EXPECTED_SHA="$EXPECTED_SHA" python - <<'PY' || fail_deployment
import json
import os

status = json.loads(os.environ["LIVE_JSON"])
assert status["deploy_color"] == os.environ["EXPECTED_COLOR"]
assert status["commit_sha"] == os.environ["EXPECTED_SHA"]
print(f"Traffic switched: {status['deploy_color']} {status['commit_sha']}")
PY

docker compose --profile "$ACTIVE_COLOR" stop "app-$ACTIVE_COLOR" >/dev/null 2>&1 || true
docker compose --profile "$ACTIVE_COLOR" rm -f "app-$ACTIVE_COLOR" >/dev/null 2>&1 || true
printf '%s
' "$INACTIVE_COLOR" > "$STATE_FILE"
echo "Deployment successful: $ACTIVE_COLOR -> $INACTIVE_COLOR"
