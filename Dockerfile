# Verwenden Sie das offizielle Python-Image als Basis
FROM python:3.9-slim

# Setzen des Arbeitsverzeichnis innerhalb des Containers
WORKDIR /app

# Kopieren der Datei requirements.txt in das Arbeitsverzeichnis
COPY requirements.txt .

# Installieren der Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des src Ordners in das Arbeitsverzeichnis, damit z.B. die config.py in das Image kopiert wird
#12 Factor Regeln sollen umgesetzt werden, sodass die Konfiguration über Umgebungsvariablen erfolgt
COPY src ./src

#Exponieren des Ports, auf dem der FastAPI-Server läuft
EXPOSE 8000

#Befehl zum Starten des FastAPI-Servers
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]