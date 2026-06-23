import requests
import csv
import time
from datetime import datetime

URL_JSON = "https://standoff2markettracker.com/items.json"
HISTORIAL_CSV = "historial_precios.csv"

# Lista de skins con sus filtros
SKINS_OBJETIVO = [
    {"mostrar": "M4 Lizard", "incluir": ["m4", "lizard"], "excluir": ["stattrack", "statt"]},
    {"mostrar": "G22 Flock", "incluir": ["g22", "flock"], "excluir": ["stattrack", "statt"]},
    {"mostrar": "M4 Flock", "incluir": ["m4", "flock"], "excluir": ["m4a1", "stattrack", "statt"]},
    {"mostrar": "Desert Eagle Violet Flame", "incluir": ["desert eagle", "violet flame"], "excluir": ["stattrack", "statt"]},
    {"mostrar": "Val Joker", "incluir": ["val", "joker"], "excluir": ["stattrack", "statt"]},
    {"mostrar": "M4A1 Stainless", "incluir": ["m4a1", "stainless"], "excluir": ["stattrack", "statt"]},
    {"mostrar": "USP Ghosts", "incluir": ["usp", "ghosts"], "excluir": ["stattrack", "statt"]},
    {"mostrar": "M40 Disguise", "incluir": ["m40", "disguise"], "excluir": ["stattrack", "statt"]}
]

cabeceras = {"User-Agent": "Mozilla/5.0"}

print("🤖 [BOT HISTÓRICO] Iniciando recolección...")

try:
    while True:
        respuesta = requests.get(URL_JSON, headers=cabeceras, timeout=10)
        if respuesta.status_code == 200:
            todo_el_mercado = respuesta.json()
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Abrimos en modo 'a' (append) para añadir datos sin borrar los anteriores
            with open(HISTORIAL_CSV, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                for skin in SKINS_OBJETIVO:
                    for item in todo_el_mercado:
                        nombre_web = item.get("name", "").lower()
                        cumple_incluir = all(p.lower() in nombre_web for p in skin["incluir"])
                        cumple_excluir = not any(e.lower() in nombre_web for e in skin.get("excluir", []))
                        
                        if cumple_incluir and cumple_excluir:
                            precio = float(item.get("price", 0))
                            writer.writerow([fecha_actual, skin["mostrar"], precio])
                            break
            print(f"💾 {fecha_actual} - Historial actualizado.")
        
        time.sleep(120)
except KeyboardInterrupt:
    print("\n🛑 Bot detenido.")

