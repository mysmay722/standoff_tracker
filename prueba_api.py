import requests

url = "https://standoff-2.com/skins-new.php"

# Fíjate en las comillas simples por fuera y las dobles por dentro
nombre_a_probar = 'M4 "Lizard"' 
params = {"command": "getStatSale", "name": nombre_a_probar} 

# Agregamos Referer y otras cabeceras para imitar un navegador perfecto
cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://standoff-2.com/",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest"
}

print(f"Haciendo la prueba de conexión para: {nombre_a_probar}...")
r = requests.get(url, params=params, headers=cabeceras)

if r.status_code == 200:
    try:
        datos = r.json()
        if datos:
            ultimo_precio = datos[-1].get("purchase_price", "N/A")
            print(f"✅ ¡Éxito! La API reconoció la skin. El precio actual es: {ultimo_precio} G")
        else:
            print("⚠️ La API respondió bien, pero el JSON está vacío. Revisa el nombre.")
    except Exception as e:
        print(f"❌ Error al intentar leer el JSON: {e}")
else:
    print(f"❌ Sigue el error de conexión HTTP: {r.status_code}")
