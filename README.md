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
