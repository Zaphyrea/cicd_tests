# Utilisez l'image de base Python
FROM python:3.11

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur

COPY requirements.txt /app/

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le code de l'application dans le conteneur
COPY . /app/

# Exposez le port pour le conteneur
EXPOSE 5000

# Commande pour exécuter l'application
CMD [ "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000" ]
