# Stratégie : trunk-based

La règle de référence est également inscrite dans README.md.

- main : version stable ; branches courtes feature/*, fix/*, docs/* et chore/*.
- exercice/* : traces pédagogiques conservées ; release/0.1 : cible du report du correctif dans le scénario d'incident.
- Nettoyer une branche personnelle non partagée par rebase interactif avant sa PR.
- PR avec quoi et pourquoi, revue de fond par le CODEOWNER, discussions résolues, puis Squash and merge avec un message type(scope): description.
- Après activation des protections : PR obligatoire, approbation CODEOWNER, historique linéaire pour les nouveaux changements, aucun contournement administrateur, pas de suppression ni de push forcé sur main.
- Tags v* : empêcher déplacement et suppression. Première version de développement v0.1.0 ; v1.0.0 seulement après validation du livrable.

Les merges pédagogiques antérieurs aux protections restent dans l'historique. L'historique partagé n'est pas réécrit pour masquer ces exercices.
