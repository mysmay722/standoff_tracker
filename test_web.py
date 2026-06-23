import requests

URL = "https://standoff2markettracker.com/"
print(f"🤖 Intentando conectar con: {URL}...")

# Fingimos ser un navegador web normal (Chrome) para que no nos bloqueen de inmediato
cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    respuesta = requests.get(URL, headers=cabeceras, timeout=10)
    print(f"📡 Código de respuesta del servidor: {respuesta.status_code}")
    
    if respuesta.status_code == 200:
        print("✅ ¡Conexión exitosa! La página web nos permitió leer su contenido.")
        print("\nPrimeros 200 caracteres del código de la página:")
        print(respuesta.text[:200])
    else:
        print("❌ El servidor nos denegó el acceso o la página no existe.")

except Exception as e:
    print(f"💥 Error al intentar conectar: {e}")

