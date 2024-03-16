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
#Es wird nur der SRC Ordner kopiert, welcher den Code enthält
COPY src ./src

#Exponieren des Ports, auf dem der FastAPI-Server läuft
EXPOSE 8000

#Befehl zum Starten des FastAPI-Servers.
#Der Parameter --reload sorgt dafür, dass der Server bei Änderungen am Code neu gestartet wird
#Der Parameter --host sort dafür, dass der Server von außen erreichbar ist
#Der Parameter --port gibt den Port an, auf dem der Server laufen soll
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]