import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_ID = os.getenv("REJSEPLANEN_API_KEY") # Henter automatisk API-nøgle fra din .env fil
BASE_URL = "https://www.rejseplanen.dk/api"  
LAT = "" # Indsæt latitude på lokationen
LON = "" # Indsæt longitude på lokationen
ANTAL = "5" # Antal af stoppesteder du ønsker at fremvise i søgningen
RADIUS = "1000000" # Søge radius i meter

def get_nearest_stop():
    # Parameter som API kaldet er lavet på baggrund af flere kan tilføjes hvis nødvændigt
    params = {
        "accessId": ACCESS_ID,
        "originCoordLat": LAT,
        "originCoordLong": LON,
        "maxNo": ANTAL,
        "r": RADIUS, 
        "format": "json"
    }

    # Laver API kaldet baseret på ovenstående paramter og benytter location.nearbystops funktionen
    resp = requests.get(f"{BASE_URL}/location.nearbystops", params=params)
    resp.raise_for_status()
    data = resp.json()

    # Behandler data fra API vedrørrende produktlisten
    def get_products(product_list):
        return [prod.get('name', '') for prod in product_list]

    # Behandler data fra API vedrørrende noterne
    def get_notes(notes_list):
        return [note.get('value', '') for note in notes_list]

    # Bearbejder dataen fra API for at returnere læseligt data
    for entry in data['stopLocationOrCoordLocation']:
        stop = entry['StopLocation']
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
        stop = get_nearest_stop()
    except Exception as e:
        print("Fejl:", e)