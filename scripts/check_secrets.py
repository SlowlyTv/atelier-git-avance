"""Controle pedagogique des contenus indexes, sans afficher les valeurs."""
import re
import subprocess
import sys

PATTERNS = [
    re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(rb'\bgh[pousr]_[A-Za-z0-9]{20,}\b'),
    re.compile(rb'(?im)^\s*(?:api[_-]?key|password|passwd|secret|access[_-]?token)\s*[:=]\s*["\x27]?[^\s"\x27]{4,}'),
]

def suspicious(data):
    return any(pattern.search(data) for pattern in PATTERNS)

def main():
    paths = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z', '--diff-filter=ACMR']).split(b'\0')
    blocked = []
    for raw in filter(None, paths):
        path = raw.decode('utf-8', 'surrogateescape')
        data = subprocess.check_output(['git', 'show', ':' + path])
        if suspicious(data):
            blocked.append(path)
    if blocked:
        for path in blocked:
            print('Commit refuse : motif de secret dans ' + path, file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
