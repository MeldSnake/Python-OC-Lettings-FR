## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`


### Déploiement

Le site web est deployer via CircleCI sur la plateforme Heroku a l'adresse suivante: [mld-oc-lettings.herokuapp.com/](https://mld-oc-lettings.herokuapp.com/) .
**Lorsqu'un ou plusieurs nouveaux commits** sont publiés sur le repository git, CircleCI effectue **automatiquement un déploiement** en suivant les instructions suivantes décrites dans le fichier [config.yml](.circleci/config.yml), soit:
1. **Compilation, Test et Verification de la Pep8.**
    1. Installation des **dépendances** du fichier [requirements.txt](requirements.txt).
    2. Verification de la **pep8** via l'utilitaire **flake8**.
    3. Test des fichiers de **migrations**
        - Avec une base de donnée *non-existante*.
        - Avec une base de donnée *existante*.
    4. Lancement des **tests** avec la commande **pytest**.
2. **Creation d'une image Docker** via le fichier [Dockerfile](Dockerfile) sur le registre [docker.io](https://hub.docker.com/repository/docker/meldsnake/oc-lettings-fr/general) avec le tag `latest`.
3. **Deploiement de l'image Docker sur Heroku**
    - L'image est publié sur le registry de heroku puis délivrée sur le serveur de l'application via la commande CLI `heroku`.

*nb: Les étapes de creation de l'image et de déploiement sont effectué seulement sur la branche `master`*

Afin de pouvoir repliquer les etapes sur un autre serveur, les variables d'environement suivantes pour chaque service sont requise:
- CircleCI :
    - **DOCKER_REGISTRY** : Le registre docker utilisé *(ici: `docker.io`)*
    - **DOCKER_IMAGE_NAME** : Le nom de l'image docker sur le registre *(ici: `meldsnake/.oc-lettings-fr`)*
    - **DOCKER_LOGIN** et **DOCKER_PASSWORD** : Le nom d'utilisateur et le mot de passe du compte utilisé pour la publication de l'image
    - **DOCKER_PROD_TAG** : Le tag utilisé lor de la publication de l'image *(ici: `latest`)*
    - **HEROKU_API_KEY** : La clé d'API pour Heroku permettant de publier l'image sur le server Heroku.
    - **HEROKU_APP_NAME** : Nom de l'application Heroku utilisée *(ici: `mld-oc-lettings`)*.
- Heroku :
    - **DJANGO_ALLOWED_HOSTS** : une liste de nom de domaine ou d’hôte séparés par une virgule *(ici: `.herokuapp.com,localhost`)* [doc](https://docs.djangoproject.com/fr/3.0/ref/settings/#allowed-hosts)
    - **DJANGO_DEBUG** : Valeur `True` si les serveur est un serveur de test.
    - **DJANGO_SECRET_KEY** : Clé de signature cryptographique de l'application django, voir le repository original pour la clé. *(ici: `fp$9^593hsriajg$_%=5trot9g!1qa@ew(o-1#@=&4%=hp46(s`)*
    - **SENTRY_API** : *Optionel*, l'adresse du point d'entré de [Sentry](https://sentry.io/) pour la récupération des évènements d'erreur.