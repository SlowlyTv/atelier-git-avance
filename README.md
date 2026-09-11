# atelier-git-avance
Atelier Git avancé : branches, rebase, conflits, pull requests et sécurité.

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

Les étapes collaboratives nécessitent un vrai second participant. Le formateur peut assurer la revue CODEOWNER, comme prévu dans le PDF. Ajouter son compte avec les droits nécessaires, lui attribuer les zones concernées dans CODEOWNERS sur main, puis ouvrir une PR touchant ces zones. Son commentaire doit expliquer un point concret du diff avant son approbation.

Version de développement prévue : v0.1.0, pour une première fonctionnalité testée dont le livrable pédagogique reste en cours de validation. Le passage à v1.0.0 attendra la validation complète.
