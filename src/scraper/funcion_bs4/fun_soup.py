import os
import requests
from bs4 import BeautifulSoup
import time
import json

# Enlace del cual queremos extraer datos
link = "https://standings.stalruth.dev/2025/regional-toronto/masters"

# Ruta donde se guardará el archivo JSON
ruta_json = "/home/david/vgc-pokemetrics/data/raw_data/link_containeraw.json"

def extract_teams_with_pause(enlace, pause_after=20, pause_duration=20, output_file=None):
    # Hacemos una petición HTTP al enlace proporcionado
    response = requests.get(enlace)
    
    # Verificamos que la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al realizar la solicitud: {response.status_code}")
        return None
    
    # Obtenemos el contenido HTML de la página
    html = response.text
    
    # Creamos el objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(html, "html.parser")
    
    # Buscamos todas las filas <tr> dentro del tbody
    filas = soup.select("tbody#standings-body tr")
    
    # Lista para almacenar los enlaces
    enlaces = []
    
    # Iteramos por todas las filas sin límite
    for i, fila in enumerate(filas):
        # Dentro de cada fila, buscamos el div con clase "team"
        equipo_div = fila.find("div", class_="team")
        if equipo_div:
            # Dentro del div, encontramos el enlace <a>
            enlace_team = equipo_div.find("a")
            if enlace_team and enlace_team.get("href"):
                enlaces.append(enlace_team['href'])  # Agregamos el enlace a la lista
                print(f"Enlace del equipo {i+1}: {enlace_team['href']}")
        
        # Hacemos una pausa después de cada 'pause_after' equipos
        if (i + 1) % pause_after == 0:
            print(f"Descansando por {pause_duration} segundos...")
            time.sleep(pause_duration)
    
    # Guardar los enlaces en el archivo JSON
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(enlaces, f, indent=4)
        print(f"Enlaces guardados en: {output_file}")

# Llamamos a la función sin límite, con pausas cada 20 equipos y guardamos los enlaces en un archivo JSON
extract_teams_with_pause(link, pause_after=20, pause_duration=20, output_file=ruta_json)
