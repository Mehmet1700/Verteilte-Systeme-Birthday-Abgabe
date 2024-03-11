# Importieren der erforderlichen Bibliotheken
from fastapi import FastAPI, HTTPException, Query
import os
from fastapi.staticfiles import StaticFiles
import requests
from fastapi.responses import HTMLResponse


#Da wir die Konfigurationsvariablen in Docker und Kubernetes extern holen, müssen wir eine Exception werfen, da die Variablen nicht aus der config.py-Datei importiert werden können.
try: 
    from config import COUCHDB_HOST, COUCHDB_PORT, COUCHDB_USERNAME, COUCHDB_PASSWORD
except ImportError as e:
    # Falls das Importieren fehlschlägt, greife auf Umgebungsvariablen zurück
    COUCHDB_HOST = os.getenv('COUCHDB_HOST')
    COUCHDB_PORT = os.getenv('COUCHDB_PORT')
    COUCHDB_USERNAME = os.getenv('COUCHDB_USERNAME')
    COUCHDB_PASSWORD = os.getenv('COUCHDB_PASSWORD')
    # Debugging-Anweisung
    print( COUCHDB_HOST, COUCHDB_PORT, COUCHDB_USERNAME, COUCHDB_PASSWORD)

app = FastAPI()

# Statische Dateien (z. B. CSS, JavaScript) in FastAPI einbinden
app.mount("/src", StaticFiles(directory="src"), name="src")

# Pfad zur HTML-Datei
html_file_path = "src/index.html"

# Funktion zum Lesen des Inhalts der HTML-Datei
def read_html_file():
    with open(html_file_path, "r") as file:
        print(COUCHDB_HOST, COUCHDB_PORT, COUCHDB_USERNAME, COUCHDB_PASSWORD)
        return file.read()

# HTML-Inhalt für die Startseite
html_content = read_html_file()

# Route für die Startseite
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_content


# Konfiguration für die Verbindung zur CouchDB
URL = os.getenv('COUCHDB_URL', f'http://{COUCHDB_HOST}:{COUCHDB_PORT}')
AUTH_USERNAME = os.getenv('COUCHDB_USERNAME', COUCHDB_USERNAME)
AUTH_PASSWORD = os.getenv('COUCHDB_PASSWORD', COUCHDB_PASSWORD)

# Route für die Suche nach Geburtstagen
@app.get('/api/v1/get_data')
# async def search_birthday(request: Request, date: str):
async def get_data(month: int = Query(..., description="Month (1-12)", ge=1, le=12),
                   day: int = Query(..., description="Day (1-31)", ge=1, le=31)):
    # Mango Query für CouchDB erstellen 
    mango_query = {
        "selector": {
            # Beachten Sie die JavaScript-Konvention für den Monat (0-11)
            "month": str(month - 1 ),
            "day": str (day)
        },
        "fields": ["first", "name", "prof","day","month","year"],
        "sort": [{"year": "asc"}]
    }

    # POST Request an CouchDB senden
    try:
        response = requests.post(
            f'{URL}/birthday_db/_find',
            json=mango_query,
            auth=(AUTH_USERNAME, AUTH_PASSWORD),
            headers={"Content-Type": "application/json"},
            timeout=2  # Timeout von 5 Sekunden setzen
        )
        print("Response received:", response)  # Debugging-Anweisung


        if response.status_code == 200:
            if response.json()['docs']:
                return response.json()['docs']
            else:
                raise HTTPException(status_code=204, detail="No data found")
        elif response.status_code == 401:  # Ungültige Anmeldeinformationen
            raise HTTPException(status_code=401, detail="Invalid credentials")
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve data")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request to CouchDB timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    # Route für den Health Endpoint
@app.get("/health")
async def health_check():
    return {"status": "Microservice is running smoothly!"}