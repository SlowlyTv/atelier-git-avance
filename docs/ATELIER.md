# Bilan de la séance 1

## Réalisé et prouvé

- Dépôt publié ; stratégie trunk-based et règles de fusion documentées dans le README ; structure et .gitignore présents.
- Rebase interactif : cinq commits brouillons ramenés à deux commits de code par pick, squash, fixup et reword. Un commit distinct ajoute ensuite les preuves. Voir preuves/rebase-avant.txt, rebase-actions.txt et rebase-apres.txt. La branche originale a été publiée après le nettoyage.
- Conflit de contenu : deux branches modifient la même ligne de accueil.txt ; première fusion sur main puis seconde fusion en conflit. Résolution combinant les idées, sans marqueurs résiduels dans accueil.txt. Les marqueurs d'origine sont conservés volontairement dans preuves/conflit-marqueurs.txt.
- Bisect : régression identifiée parmi huit commits par un test automatisé reproductible. Voir preuves/bisect-log.txt et bisect-execution.txt.
- Cherry-pick : correctif reporté seul depuis fix/addition-hotfix vers release/0.1. SHA différents, fichier corrigé identique, travail annexe exclu. Voir preuves/cherry-pick.txt.
- Hook local activé ; tentative réelle de commit d'un faux secret refusée ; HEAD inchangé après le refus. Voir preuves/hook-rejet.txt et tests-securite.txt.
- CODEOWNERS réparti par chemins existants ; toutes les zones sont pour l'instant attribuées à SlowlyTv.

## À finaliser ou à vérifier avec le formateur

- Revue indépendante avec commentaire de fond par le propriétaire désigné, puis fusion. Les PR de préparation ne satisfont pas cette exigence.
- Contributions de plusieurs personnes réelles. Les deux branches du conflit ont été manipulées par le même compte ; l'exercice technique est réalisé, le travail de groupe ne l'est pas.
- Signature : vérifier le résultat le plus récent dans preuves/signature.json ; un résultat verified=false ne valide pas l'étape.
- Protections main et tags : voir preuves/protections/ lorsqu'elles auront été appliquées et testées.
- Tag SemVer : version initiale de développement v0.1.0 prévue ; v1.0.0 sera réservée au livrable final validé.

## Écarts historiques conservés

Le dépôt a été initialisé sur GitHub, pas par git remote add depuis un dépôt local. Le premier commit ne contenait pas de .gitignore. Initial commit et le message de merge de la PR #1 ne suivent pas Conventional Commits. Ils sont conservés plutôt que de réécrire main déjà partagé. Les messages brouillons sur les branches témoins servent de preuves du rebase et de la régression volontaire.
