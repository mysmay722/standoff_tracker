import requests
from bs4 import BeautifulSoup

URL = "https://standoff2markettracker.com/"
cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("🕵️‍♂️ [INSPECTOR] Buscando tus skins en el mapa del sitio...")

try:
    respuesta = requests.get(URL, headers=cabeceras, timeout=10)
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    
    # Buscaremos si "M40 Disguise" o "M4 Lizard" aparecen en el código estático
    skin_test = "M4"
    encontrado = soup.find(string=lambda t: t and skin_test.lower() in t.lower())
    
    if encontrado:
        print(f"✅ ¡Encontré coincidencias para '{skin_test}'!")
        # Mostramos el bloque de código de alrededor para analizarlo
        padre = encontrado.parent.parent
        print("\n--- CAPTURA DEL CÓDIGO HTML DETECTADO ---")
        print(padre.prettify()[:1200])
    else:
        print(f"🔍 No encontré la palabra '{skin_test}' en la página de inicio.")
        print("Esto suele significar que los precios están en una subpágina (ej: /market, /skins) o cargan dinámicamente.")
        
        # Alivio de luto: Listamos los primeros enlaces de la página para investigar el menú
        print("\n📋 Menú de secciones encontrado:")
        enlaces = soup.find_all('a', href=True)
        for i, link in enumerate(enlaces[:15]):
            print(f"   [{i}] {link.text.strip()} -> {link['href']}")

except Exception as e:
    print(f"💥 Error durante la inspección: {e}")

