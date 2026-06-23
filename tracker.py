import csv
import os

ARCHIVO_PRECIOS = "precios_skins.csv"

def guardar_precio(skin, precio):
    archivo_existe = os.path.exists(ARCHIVO_PRECIOS)
    with open(ARCHIVO_PRECIOS, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        if not archivo_existe:
            escritor.writerow(["Skin", "Precio (Oro)"])
        escritor.writerow([skin, precio])
    print(f"¡Guardado con éxito: {skin} -> {precio} oro!\n")

# --- EL BUCLE COMPORTAMIENTO REPETITIVO ---
print("--- TRACKER DE STANDOFF 2 ---")
print("Escribe 'salir' en el nombre de la skin cuando quieras terminar.\n")

while True:
    nombre_skin = input("Introduce el nombre de la skin: ")
    
    # Si el usuario escribe 'salir', el bucle se rompe y el programa termina
    if nombre_skin.lower() == 'salir':
        print("¡Proceso terminado! Datos guardados en precios_skins.csv")
        break
        
    precio_skin = input("Introduce el precio actual en oro: ")
    
    # Guardamos y el bucle vuelve a empezar
    guardar_precio(nombre_skin, precio_skin)




