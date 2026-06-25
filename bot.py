import requests
import csv
import time
from datetime import datetime
from config import MAPA_IMAGENES

# URL base de la nueva API
API_URL = "https://standoff-2.com/skins-new.php"
HISTORIAL_CSV = "historial_precios.csv"

# Cabecera para simular un navegador
cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("🤖 [BOT] Iniciando recolección desde standoff-2.com...")

def obtener_precio(nombre_skin):
    params = {"command": "getStatSale", "name": nombre_skin}
    try:
        r = requests.get(API_URL, headers=cabeceras, params=params, timeout=10)
        if r.status_code == 200:
            datos = r.json()
            # Devolvemos el último registro (el más reciente)
            return float(datos[-1].get("purchase_price", 0))
    except Exception as e:
        print(f"Error consultando {nombre_skin}: {e}")
    return None

try:
    while True:
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(HISTORIAL_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            for nombre_skin in MAPA_IMAGENES.keys():
                precio = obtener_precio(nombre_skin)
                if precio:
                    writer.writerow([fecha_actual, nombre_skin, precio])
                    print(f"💾 {fecha_actual} - {nombre_skin}: {precio} G")
        
        # Esperar un tiempo prudente (ej: 1 hora) para no saturar
        time.sleep(3600) 
except KeyboardInterrupt:
    print("\n🛑 Bot detenido.")

