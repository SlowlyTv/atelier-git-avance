# Sécurité du dépôt

Installation locale après chaque clone :

    git config core.hooksPath .githooks
    chmod +x .githooks/pre-commit
    python3 -m unittest discover -s tests -v

Le hook inspecte les contenus indexés (ce qui va entrer dans le commit), pas seulement les fichiers du répertoire. Il refuse des motifs évidents de mot de passe, clé API, jeton GitHub ou clé privée, sans afficher leur valeur. C'est un contrôle pédagogique par motifs, pas une garantie de détection universelle. Les hooks locaux ne se transmettent pas automatiquement avec la configuration Git : il faut les activer après clonage.

La preuve hook-rejet.txt montre une tentative réelle de commit d'un faux secret rejetée. Aucun vrai secret n'a été utilisé. Les tests vérifient aussi qu'un fichier nettoyé mais non réindexé reste bloqué.

Les commits du Codespace utilisent sa configuration de signature GPG existante. Le statut de vérification GitHub sera conservé dans preuves/signature.json. Il s'agit de la signature gérée par Codespaces, pas d'une clé privée personnelle générée pendant l'exercice.
