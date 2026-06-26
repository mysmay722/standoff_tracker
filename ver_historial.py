import requests
import json

url = "https://standoff-2.com/skins-new.php"
nombre_a_probar = 'M4 "Lizard"' 
params = {"command": "getStatSale", "name": nombre_a_probar} 

cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://standoff-2.com/",
    "Accept": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

print(f"Descargando el historial completo de: {nombre_a_probar}...")
r = requests.get(url, params=params, headers=cabeceras)

if r.status_code == 200:
    datos = r.json()
    total_registros = len(datos)
    print(f"¡Se encontraron {total_registros} registros históricos!")
    
    print("\n--- ESTRUCTURA DEL PRIMER REGISTRO (MÁS ANTIGUO) ---")
    # Imprimimos el registro [0] con indentación para que sea fácil de leer
    print(json.dumps(datos[0], indent=4))
else:
    print(f"Error de conexión: {r.status_code}")
