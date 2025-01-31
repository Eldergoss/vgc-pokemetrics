from bs4 import BeautifulSoup
import requests
import json

# Ruta del JSON con los enlaces
ruta_json = "/home/david/vgc-pokemetrics/data/raw_data/link_containeraw.json"
# Ruta del JSON de salida
ruta_json_ = "/home/david/vgc-pokemetrics/data/processed_data/vgc_data.json"

def get_soup_from_url(url):
    """
    Obtiene el contenido HTML de una URL y lo convierte en un objeto BeautifulSoup.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def load_links_from_json(ruta_json):
    """
    Carga los enlaces desde el archivo JSON.
    """
    with open(ruta_json, "r") as file:
        links = json.load(file)
    return links

def extract_data_from_article(article):
    """
    Extrae los datos del artículo de un Pokémon.
    """
    pre = article.find("pre").text.strip()
    lines = pre.split("\n")

    # Primera línea: Nombre e ítem
    name_item = lines[0].split("@")
    name = name_item[0].strip()
    item = name_item[1].strip() if len(name_item) > 1 else None

    # Extraer habilidades y Tera Type
    ability_line = article.find("span", class_="attr", string="Ability: ").next_sibling.strip()
    tera_type_tag = article.find("span", class_="attr", string="Tera Type: ")
    tera_type = tera_type_tag.find_next("span").text.strip() if tera_type_tag else None

    # Extraer movimientos
    moves = [line.split(" ", 1)[-1].strip() for line in lines if line.startswith("-")]

    # Crear el diccionario del Pokémon
    pokemon = {
        "pokemon": name,
        "habilidad": ability_line,
        "tera_type": tera_type,
        "ítem": item,
        "movimientos": moves
    }

    return pokemon

def organize_team_data(articles):
    """
    Organiza los datos extraídos en un equipo de Pokémon.
    """
    team = [extract_data_from_article(article) for article in articles]
    return team

def save_to_json(data, file_path):
    """
    Guarda los datos organizados en un archivo JSON.
    """
    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=4, ensure_ascii=False)

def main():
    # Cargar los enlaces del archivo JSON
    links = load_links_from_json(ruta_json)

    # Diccionario para almacenar todos los equipos procesados
    all_teams = {}

    # Procesar cada enlace sin límite
    for i, link in enumerate(links):
        print(f"Procesando equipo {i+1} de {len(links)}: {link}")
        
        # Obtener el contenido de la página
        soup = get_soup_from_url(link)
        
        # Extraer todos los artículos (cada uno es un Pokémon)
        articles = soup.find_all("article")

        # Organizar los datos del equipo
        team = organize_team_data(articles)

        # Guardar el equipo en el diccionario con índice dinámico
        all_teams[f"team_{i+1}"] = team

    # Guardar el resultado en el archivo JSON de salida
    save_to_json(all_teams, ruta_json_)

# Ejecutar el script
main()
