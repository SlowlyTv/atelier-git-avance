# atelier-git-avance

[![CI](https://github.com/SlowlyTv/atelier-git-avance/actions/workflows/ci.yml/badge.svg)](https://github.com/SlowlyTv/atelier-git-avance/actions/workflows/ci.yml)

Atelier Git avancé : branches, rebase, conflits, pull requests et sécurité.

## Intégration continue

Le workflow CI se déclenche sur chaque pull request et sur les push vers `main`. Il vérifie d'abord le style avec flake8, puis exécute les tests pytest sur Python 3.10, 3.11 et 3.12. Les dépendances pip sont mises en cache et un rapport de couverture HTML est conservé comme artefact pour chaque version de Python.

## Strategie : trunk-based

main contient la version stable. Chaque changement part de main a jour sur une branche courte : feature/*, fix/*, docs/* ou chore/*. Les branches exercice/* conservent les preuves pedagogiques.

Avant publication, nettoyer uniquement les branches personnelles non partagees par rebase interactif. Ouvrir une PR decrivant quoi et pourquoi, demander une revue de fond au CODEOWNER, resoudre les discussions puis utiliser Squash and merge avec un message Conventional Commits. Les exercices de merge sont effectues avant activation de la protection lineaire ; les commits de merge deja presents sont des traces pedagogiques conservees.

## Conventions et versions

Messages : type(scope): description (feat, fix, docs, test, chore). SemVer : MAJEUR pour une rupture de compatibilite, MINEUR pour une fonctionnalite compatible, CORRECTIF pour une correction compatible. Le livrable initial sera v1.0.0 apres validation.

## Transparence et suivi

Atelier realise par SlowlyTv. Aucune contribution ne sera attribuee a un coequipier fictif. Une revue independante et des contributions reelles de plusieurs membres restent a organiser avec le formateur. La PR #1 est une preparation fusionnee sans revue independante. Le depot a ete cree sur GitHub puis clone dans Codespaces ; le premier commit contenait seulement le README et le .gitignore a ete ajoute ensuite.

Les preuves seront conservees dans preuves/ ; la strategie detaillee figure dans docs/STRATEGIE.md.

## Résultats et preuves

Le bilan détaillé est dans [docs/ATELIER.md](docs/ATELIER.md). Les journaux avant/après du rebase, le conflit, bisect, cherry-pick et les essais du hook sont dans [preuves/](preuves/).

Pour exécuter les tests : python3 -m unittest discover -s tests -v.
Pour activer le hook après clonage : git config core.hooksPath .githooks.

Version de développement prévue : v0.1.0, pour une première fonctionnalité testée dont le livrable pédagogique reste en cours de validation. Le passage à v1.0.0 attendra la validation complète.

## Docker - comparaison des images

Les deux images ont été reconstruites sans cache le 18 septembre 2026 avant la mesure.

| Variante | Dockerfile | Image de base | Serveur | Taille |
| --- | --- | --- | --- | ---: |
| Naive | `starter-app/Dockerfile.naive` | `python:3.12` | Flask | **1,63 Go** |
| Multi-stage | `starter-app/Dockerfile` | `python:3.12-slim` | Gunicorn | **215 Mo** |

Le build multi-stage réduit la taille de **87,5 %**. Le stage `builder` crée le virtualenv et installe les dépendances. Le stage final récupère uniquement ce virtualenv et `app.py` : les outils de build et les caches ne sont pas conservés.

```bash
docker build --pull --no-cache -f starter-app/Dockerfile.naive -t atelier-git-avance:naive-mesure starter-app
docker build --pull --no-cache -t atelier-git-avance:multistage-mesure starter-app
docker images atelier-git-avance
```

Pour tester depuis un Codespace :

```bash
docker run --rm -p 8082:5000 atelier-git-avance:multistage-mesure
```

Le `localhost` appartient à la machine distante du Codespace. Pour ouvrir le service sur votre ordinateur, utilisez **Ports**, repérez le port `8082`, puis choisissez **Ouvrir dans le navigateur**.


## Exécuter la pile Docker Compose

La pile comprend l'application Flask et Redis 7. Redis est joint avec le nom de service `redis`, sur un réseau Docker dédié. Le volume nommé `redis-data` conserve le compteur de visites.

```bash
docker build -t atelier-git-avance:local starter-app
docker compose -f starter-app/docker-compose.yml config
docker compose -f starter-app/docker-compose.yml up -d --build
docker compose -f starter-app/docker-compose.yml ps
```

Points d'accès :

- `/health` vérifie l'état du service web ;
- `/status` renvoie la version de l'application ;
- `/visits` incrémente un compteur persistant dans Redis.

Dans GitHub Codespaces, ouvrez l'onglet **Ports** puis le port **8080** pour accéder à l'application depuis votre ordinateur. Le `localhost` du Codespace appartient à la machine distante.

Pour arrêter la pile :

```bash
docker compose -f starter-app/docker-compose.yml down
```

## Image publiée

L'image est publiée dans GitHub Container Registry : [ghcr.io/slowlytv/atelier-git-avance](https://github.com/users/SlowlyTv/packages/container/package/atelier-git-avance).

```bash
docker pull ghcr.io/slowlytv/atelier-git-avance:v1.0.0
docker pull ghcr.io/slowlytv/atelier-git-avance:latest
docker run --rm -p 8080:5000 ghcr.io/slowlytv/atelier-git-avance:v1.0.0
```

## Vérification finale de l'atelier 3

- [x] Dockerfile naïf conservé pour la comparaison.
- [x] Image multi-stage légère et utilisateur non-root.
- [x] Application accessible sur le port 8080 du Codespace.
- [x] Compose avec web, Redis, réseau dédié et volume nommé.
- [x] Healthchecks web et Redis, avec attente de Redis avant le démarrage web.
- [x] Compteur `/visits` persistant après redémarrage du service web.
- [x] Publication GHCR avec les tags `v1.0.0` et `latest`.
- [x] Commandes de construction et d'exécution documentées.

## Pipeline CI/CD blue/green

Le pipeline execute lint, les tests Python, publie l'image Docker avec les tags github.sha et latest, puis lance deploy/deploy.sh dans l'environment GitHub production.

Le deploiement demarre la couleur inactive, attend le vrai endpoint /health, controle deploy_color et commit_sha dans /status, recharge nginx puis arrete l'ancienne couleur. Si un controle echoue, le candidat est supprime et la couleur active ne change pas.

Verification locale :

    cd starter-app
    docker compose --profile blue up -d --build
    curl http://localhost:8080/status
    EXPECTED_SHA=demo ./deploy/deploy.sh

## Observabilite avec Prometheus et Grafana

L'application expose ses metriques sur `/metrics`. Le compteur
`http_requests_total` distingue la methode, l'endpoint et le code HTTP. La
latence est mesuree avec l'histogramme
`http_request_duration_seconds`. L'endpoint `/metrics` est exclu du compteur
pour que les scrapes Prometheus ne faussent pas les resultats.

Pour lancer toute la stack en une commande :

```bash
cd starter-app
cp .env.example .env
docker compose --profile blue up -d --build
```

Services disponibles :

- application : <http://localhost:5001> ;
- metriques Flask : <http://localhost:5001/metrics> ;
- Prometheus : <http://localhost:9090> ;
- cibles Prometheus : <http://localhost:9090/targets> ;
- regles Prometheus : <http://localhost:9090/rules> ;
- alertes Prometheus : <http://localhost:9090/alerts> ;
- Grafana : <http://localhost:3000>.

Grafana utilise l'utilisateur `admin`. Son mot de passe est lu depuis
`GRAFANA_ADMIN_PASSWORD` dans le fichier `.env`. La datasource Prometheus est
provisionnee automatiquement avec l'adresse interne
`http://prometheus:9090`.

Le dashboard **Atelier - Observabilite**, range dans le dossier
**Atelier DevOps**, est charge automatiquement depuis
`observability/grafana/dashboards/atelier-observabilite.json`. Il montre :

1. le debit de requetes par endpoint ;
2. le taux global de reponses HTTP 5xx ;
3. la latence p95 calculee avec `histogram_quantile()`.

La regle `HighHttpErrorRate` passe en alerte lorsque la proportion de reponses
5xx depasse **5 % pendant au moins 30 secondes**. Pour la tester, generer du
trafic normal puis appeler `/simulate-error` de facon soutenue pendant plus de
30 secondes. Son etat evolue de `inactive` a `pending`, puis `firing`.

Exemple PowerShell :

```powershell
1..10 | ForEach-Object { curl.exe -s http://localhost:5001/ | Out-Null }
$fin = (Get-Date).AddSeconds(45)
while ((Get-Date) -lt $fin) {
    curl.exe -s http://localhost:5001/simulate-error | Out-Null
    Start-Sleep -Milliseconds 200
}
```

Les exemples PromQL de l'atelier sont conserves dans
`observability/queries.promql`. Pour arreter et supprimer les conteneurs :

```bash
docker compose --profile blue down
```
