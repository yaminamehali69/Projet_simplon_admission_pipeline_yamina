# Dockerfile
## + rapide et + légère car elle as le strict minum 
FROM python:3.10-slim  

WORKDIR /app

RUN pip install requests pandas tabulate

# Ligne ajoutée pour forcer Docker à ignorer le cache de l'étape COPY
RUN echo "Forcing file refresh"

COPY . /app

CMD ["python", "main_pipeline.py"]