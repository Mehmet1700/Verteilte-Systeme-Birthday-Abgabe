from fastapi import FastAPI , Request
from fastapi.responses import FileResponse
from datetime import datetime
import requests


app = FastAPI()


# Route für die HTML-Datei
@app.get("/", response_class=FileResponse)
async def read_root():
    return "index.html"

# Route für die CSS-Datei
@app.get("/styles.css", response_class=FileResponse)
async def read_styles():
    return "styles.css"

# Route für die Suche nach Geburtstagen
@app.get("/search")
async def search_birthday(request: Request, date: str):
    try:
        formatted_date = datetime.strptime(date, "%m-%d")
        return {"message": f"Geburtstage für das Datum {formatted_date.strftime('%m-%d')} wurden nicht gefunden."}
    except ValueError:
        return {"message": "Ungültiges Datumsformat. Bitte verwenden Sie das Format MM-DD."}
