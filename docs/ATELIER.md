# Suivi de l'atelier

Ce document distingue la préparation des exercices effectivement réalisés. Ne cocher une étape qu'après vérification et ajout des preuves.

- [x] Dépôt GitHub créé.
- [x] Stratégie de branches rédigée dans `docs/STRATEGIE.md`.
- [x] Fichier `.github/CODEOWNERS` préparé sur la branche de documentation.
- [ ] Préparation fusionnée dans `main` pour rendre CODEOWNERS applicable aux PR suivantes.
- [ ] Rebase interactif réalisé : conserver les historiques avant/après et les actions pick/squash/reword.
- [ ] Conflit provoqué puis résolu : conserver les noms de branches, le fichier concerné et le commit de résolution.
- [ ] Cherry-pick réalisé : noter le commit source et le nouveau commit.
- [ ] Bisect réalisé : conserver le journal `git bisect log` et le commit fautif identifié par un test.
- [ ] Cycle PR → revue indépendante → merge : noter le lien de PR et l'identité du relecteur.
- [ ] Protection avancée de `main` active : conserver la configuration et un exemple de blocage.
- [ ] Hook anti-secret installé : vérifier le refus d'un faux secret puis l'acceptation d'un fichier sain. Ne jamais utiliser un véritable secret pour cet exercice.
- [ ] Commit signé : noter le SHA et vérifier la signature. Ne pas confondre signature et ligne Signed-off-by.
- [ ] Tag SemVer `v1.0.0` créé et publié après validation.

## Prochaine étape : un terminal Git

Utiliser Git installé sur le poste ou ouvrir le dépôt dans GitHub Codespaces via Code → Codespaces. Dans un terminal Git local, cloner le dépôt ; Codespaces le clone automatiquement.

```sh
git clone https://github.com/SlowlyTv/atelier-git-avance.git
cd atelier-git-avance
```

Dans le dossier du dépôt (y compris avec Codespaces), vérifier :

```sh
git status
git branch -a
git --version
```

Les exercices seront réalisés et documentés à partir de cet environnement. Pour le travail en solo, demander au formateur comment valider la revue indépendante ; ne pas cocher cette exigence à partir d'une auto-revue.
