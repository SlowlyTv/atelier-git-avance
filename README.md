# atelier-git-avance
Atelier Git avancé : branches, rebase, conflits, pull requests et sécurité.

## Strategie : trunk-based

main contient la version stable. Chaque changement part de main a jour sur une branche courte : feature/*, fix/*, docs/* ou chore/*. Les branches exercice/* conservent les preuves pedagogiques.

Avant publication, nettoyer uniquement les branches personnelles non partagees par rebase interactif. Ouvrir une PR decrivant quoi et pourquoi, demander une revue de fond au CODEOWNER, resoudre les discussions puis utiliser Squash and merge avec un message Conventional Commits. Les exercices de merge sont effectues avant activation de la protection lineaire ; les commits de merge deja presents sont des traces pedagogiques conservees.

## Conventions et versions

Messages : type(scope): description (feat, fix, docs, test, chore). SemVer : MAJEUR pour une rupture de compatibilite, MINEUR pour une fonctionnalite compatible, CORRECTIF pour une correction compatible. Le livrable initial sera v1.0.0 apres validation.

## Transparence et suivi

Atelier realise par SlowlyTv avec assistance de Codex. Aucune contribution ne sera attribuee a un coequipier fictif. Une revue independante et des contributions reelles de plusieurs membres restent a organiser avec le formateur. La PR #1 est une preparation fusionnee sans revue independante. Le depot a ete cree sur GitHub puis clone dans Codespaces ; le premier commit contenait seulement le README et le .gitignore a ete ajoute ensuite.

Les preuves seront conservees dans preuves/ ; la strategie detaillee figure dans docs/STRATEGIE.md.
