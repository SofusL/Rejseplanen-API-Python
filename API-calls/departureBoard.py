import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Vestamager Station: 8603317

load_dotenv()

ACCESS_ID = os.getenv("REJSEPLANEN_API_KEY") # Henter automatisk API-nøgle fra din .env fil
BASE_URL = "https://www.rejseplanen.dk/api"  
ID = "8603317" # Indsæt stationens ID - Kan anskaffes ved hjælp af location.nerbystops
DURATION = "10" # Indsæt antal minuter i fremtiden den skal kigge.

def get_next_train():
    # Parameter som API kaldet er lavet på baggrund af flere kan tilføjes hvis nødvændigt
    params = {
        "accessId": ACCESS_ID,
        "id": ID,
        "duration": DURATION,
        "format": "json"
    }

    # Laver API kaldet baseret på ovenstående paramter og benytter location.nearbystops funktionen
    resp = requests.get(f"{BASE_URL}/departureBoard", params=params)
    resp.raise_for_status()
    data = resp.json()
    print(data)

    # Behandler data fra API vedrørrende produktlisten
    def get_products(product_list):
        return [prod.get('name', '') for prod in product_list]

    # Behandler data fra API vedrørrende noterne
    def get_notes(notes_list):
        return [note.get('value', '') for note in notes_list]

    # Bearbejder dataen fra API for at returnere læseligt data
    for entry in data['Departure']:
        stop = entry['JourneyDetailRef']
        name = stop.get('name', '')
        extId = stop.get('extId', '')
        lon = stop.get('lon', '')
        lat = stop.get('lat', '')
        dist = stop.get('dist', '')
        products = get_products(stop.get('productAtStop', []))
        notes = get_notes(stop.get('LocationNotes', {}).get('LocationNote', []))

        print(f"Stop Name: {name}")
        print(f"  ID: {extId}")
        print(f"  Location: ({lat}, {lon})")
        print(f"  Distance: {dist} meters")
        print(f"  Products: {', '.join(products)}")
        if notes:
            print(f"  Notes: {', '.join(notes)}")
        print('-' * 40)
    

# Primære funktion som køre scripten
if __name__ == "__main__":
    try:
        stop = get_next_train()
    except Exception as e:
        print("Fejl:", e)