import requests

url = "https://standoff-2.com/skins-new.php"

# Vamos a probar con una de tus skins
nombre_a_probar = "M4 Lizard"
params = {"command": "getStatSale", "name": nombre_a_probar} 

# Siempre es buena práctica llevar el User-Agent
cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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
            print("⚠️ La API respondió bien, pero el JSON está vacío. El nombre podría estar mal escrito para este servidor.")
    except Exception as e:
        print(f"❌ Error al intentar leer el JSON. El servidor devolvió texto crudo:\n{r.text[:200]}")
else:
    print(f"❌ Error de conexión HTTP: {r.status_code}")
