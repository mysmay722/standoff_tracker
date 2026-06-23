import requests
import json

URL_JSON = "https://standoff2markettracker.com/items.json"
cabeceras = {"User-Agent": "Mozilla/5.0"}

respuesta = requests.get(URL_JSON, headers=cabeceras)
datos = respuesta.json()

# Buscamos solo una skin para ver toda su información
skin_ejemplo = "M4 Lizard"
for item in datos:
    if "Lizard" in item.get("name", ""):
        print(f"--- Datos completos para: {item['name']} ---")
        print(json.dumps(item, indent=4))
        break000
