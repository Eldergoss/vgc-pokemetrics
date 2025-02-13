import requests
from bs4 import BeautifulSoup
import csv

# URL de la página
url = "https://limitlesstcg.com/tournaments/472"

# Realizar la solicitud HTTP
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Usar BeautifulSoup para procesar el HTML obtenido
    soup = BeautifulSoup(response.text, 'html.parser')

    # Buscar todas las filas (<tr>) que tengan los atributos data-rank, data-deck y data-name
    filas = soup.find_all("tr", attrs={"data-rank": True, "data-deck": True, "data-name": True})

    # Verificar si se encontraron filas
    if filas:
        # Crear una lista para almacenar los datos de los competidores
        competidores = []

        # Recorrer todas las filas encontradas y filtrar hasta el competidor 33
        for fila in filas:
            rank = int(fila.get("data-rank"))  # Obtener el rank como entero
            if rank > 64:
                break  # Detenerse después del competidor 33
            
            nombre = fila.get("data-name")
            deck = fila.get("data-deck")
            competidores.append({"Rank": rank, "Nombre": nombre, "Mazo": deck})

        # Imprimir los datos de los competidores
        print("Competidores y sus mazos (Top 33):")
        for competidor in competidores:
            print(f"Rank: {competidor['Rank']}, Nombre: {competidor['Nombre']}, Mazo: {competidor['Mazo']}")

        # Guardar los datos en un archivo CSV
        with open("competidores_top33.csv", mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=["Rank", "Nombre", "Mazo"])
            escritor.writeheader()  # Escribir la cabecera
            escritor.writerows(competidores)  # Escribir los datos

        print("\nDatos guardados en 'competidores_top33.csv'.")
    else:
        print("No se encontraron filas con los atributos esperados.")
else:
    print(f"Error al realizar la solicitud HTTP: {response.status_code}")
