import requests
import csv
from config import MAPA_IMAGENES

URL = "https://standoff-2.com/skins-new.php"
HISTORIAL_CSV = "historial_precios.csv"

cabeceras = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://standoff-2.com/",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

print("⏳ [MÁQUINA DEL TIEMPO] Iniciando descarga histórica...")

# Aquí guardaremos todos los datos antiguos que descarguemos
nuevos_registros = []

for nombre_skin in MAPA_IMAGENES.keys():
    print(f"📥 Descargando historial de: {nombre_skin}...")
    params = {"command": "getStatSale", "name": nombre_skin}
    
    try:
        r = requests.get(URL, params=params, headers=cabeceras)
        if r.status_code == 200:
            historial = r.json()
            
            for item in historial:
                # 👇 REVISA TU CAPTURA Y CAMBIA ESTAS PALABRAS SI ES NECESARIO 👇
                # Si en tu terminal el tiempo se llama "time" o "created_at", cámbialo aquí.
                fecha_cruda = item.get("Date") 
                # Si en tu terminal el precio se llama "purchase_price", cámbialo aquí.
                precio_crudo = item.get("purchase_price") 
                
                if fecha_cruda and precio_crudo:
                    # Cortamos la fecha a 16 caracteres para que encaje perfecto como "YYYY-MM-DD HH:MM"
                    fecha_limpia = str(fecha_cruda)[:16] 
                    nuevos_registros.append([fecha_limpia, nombre_skin, float(precio_crudo)])
    except Exception as e:
        print(f"❌ Error al procesar {nombre_skin}: {e}")

# Leemos los datos automatizados que ya recolectó el bot hoy, para no borrarlos
datos_actuales = []
try:
    with open(HISTORIAL_CSV, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        datos_actuales = list(reader)
except FileNotFoundError:
    pass

# Juntamos el pasado con el presente
datos_totales = datos_actuales + nuevos_registros

# Reescribimos tu archivo CSV con absolutamente todos los datos
with open(HISTORIAL_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(datos_totales)

print(f"✅ ¡Éxito! Se inyectaron {len(nuevos_registros)} registros antiguos a tu base de datos.")
