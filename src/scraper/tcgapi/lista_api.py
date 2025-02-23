import requests

SET_API_URL = "https://api.pokemontcg.io/v2/sets"

response = requests.get(SET_API_URL)

if response.status_code == 200:
    sets_data = response.json()
    sets = sets_data["data"]  # Lista de sets

    # Mostrar los nombres de los primeros 10 sets
    for set_info in sets[-12:]:
        print(set_info["id"], "-", set_info["name"])
else:
    print("Error al obtener los sets:", response.status_code)
