import requests
import json

# ID del set Paradox Rift
SET_ID = "sv3"





# Clave de API (NO compartir en público)
API_KEY = "f93a9b96-7e93-42a9-8361-e1e5a01dfbb0"  # Usa tu propia clave



# Hacer la solicitud a la API
url = f"https://api.pokemontcg.io/v2/cards?q=set.id:{SET_ID}"
headers = {"X-Api-Key": API_KEY}  # Reemplaza con tu API Key
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json().get("data", [])
    
    # Extraer solo cartas con precios Holofoil
    cartas_con_precios = []
    for carta in data:
        if "tcgplayer" in carta and "prices" in carta["tcgplayer"] and "holofoil" in carta["tcgplayer"]["prices"]:
            precio = carta["tcgplayer"]["prices"]["holofoil"].get("market")
            if precio:
                cartas_con_precios.append({
                    "nombre": carta["name"],
                    "precio": precio
                })
    
    # Ordenar de mayor a menor precio
    cartas_con_precios.sort(key=lambda x: x["precio"], reverse=True)

    # Imprimir en consola los resultados
    for carta in cartas_con_precios:
        print(f"{carta['nombre']}: ${carta['precio']}")
else:
    print("Error en la API:", response.status_code)
