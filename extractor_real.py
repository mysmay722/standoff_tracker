import requests
import json
from bs4 import BeautifulSoup

URL_BASE = "https://standoff2markettracker.com/"
URL_JSON = "https://standoff2markettracker.com/items.json"

cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("🚀 [EXTRACTOR] Intentando descargar items.json directamente...")

# INTENTO 1: Ver si el archivo .json está accesible directamente
r = requests.get(URL_JSON, headers=cabeceras, timeout=10)

if r.status_code == 200 and "json" in r.headers.get("Content-Type", "").lower():
    print("🎉 ¡Premio gordo! El archivo items.json es público y accesible.")
    try:
        data = r.json()
        print("\nMuestra de los datos encontrados:")
        print(json.dumps(data, indent=2)[:800])
    except Exception as e:
        print(f"No se pudo procesar como JSON directo: {e}")
else:
    # INTENTO 2: Si está protegido, lo buscamos en los bloques de código del fondo
    print("❌ No se pudo acceder al JSON directo. Buscando en los scripts del fondo...")
    r_main = requests.get(URL_BASE, headers=cabeceras, timeout=10)
    soup = BeautifulSoup(r_main.text, 'html.parser')
    scripts = soup.find_all('script')
    
    encontrado = False
    for i, s in enumerate(scripts):
        if s.string and "window.ITEMS" in s.string:
            print(f"✅ ¡Encontré el bloque de datos escondido en el script #{i}!")
            print("\nInicio del bloque de datos:")
            print(s.string[:800].strip())
            encontrado = True
            break
            
    if not encontrado:
        print("🔍 No pudimos ver las variables crudas. Vamos a imprimir los últimos scripts de la página para ver dónde se esconden.")
        for i, s in enumerate(scripts[-3:]):
            print(f"\n--- Script Final {i} ---")
            print(s.string[:300] if s.string else f"[Script externo: {s.get('src')}]")

