# Stratégie de branches

- `main` : version stable et livrable du projet.
- `docs/*` : documentation.
- `feature/*` : fonctionnalités isolées.
- `fix/*` : corrections.
- `exercice/*` : branches conservées comme preuves des manipulations Git.

Chaque changement part de `main` à jour. Les commits sont courts et décrivent une intention (`docs:`, `feat:`, `fix:`, `test:`). Avant publication, un rebase interactif permet de regrouper les commits de brouillon. Ne pas réécrire l'historique partagé de `main`.

Les changements passent par une pull request. Une autre personne disposant des droits nécessaires effectue la revue. Après validation des contrôles et résolution des discussions, la branche peut être fusionnée. Les branches d'exercice restent disponibles pour l'évaluation.

## Protection cible (à configurer et vérifier)

Sur `main` : imposer une pull request, la résolution des discussions et un contrôle automatisé réussi ; bloquer les suppressions et les push forcés. Exiger une approbation CODEOWNER une fois un relecteur disponible.

## Versions

Utiliser des tags `vMAJEUR.MINEUR.CORRECTIF` : correctif compatible = CORRECTIF, ajout compatible = MINEUR, rupture de compatibilité = MAJEUR. Le premier livrable validé recevra le tag annoté `v1.0.0`.

## Situation de départ

Atelier réalisé seul. La revue par un autre compte reste à organiser : une auto-revue ne sera pas présentée comme une approbation indépendante.
