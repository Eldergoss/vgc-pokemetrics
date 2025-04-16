import requests
import json
import pandas as pd

#pokemon = input("el nombre de pokemon (en caso de ser un ex,gx o v agregarlos al final : )")

URL = "https://api.pokemontcg.io/v2/cards"
params = {"q": 'name:"steelix"'}  # Busca todas las cartas con este nombre
response = requests.get(URL, params=params)
respuesta = response.json()

#inicamos la lista vacia
poke_list = []

#ciclos  for 

for carta in respuesta["data"]:  # Accede a la lista de cartas bajo la clave "data"
    nombre = carta["name"]
    card_id = carta["id"] #extrae el nombre dentro de 
    expansion = carta["set"]["name"]
    
    
    # Extrae el precio (holofoil o reverseHolofoil)
    precios = carta.get("tcgplayer", {}).get("prices", {})
    precio = (
        precios.get("holofoil", {}).get("market") 
        or precios.get("reverseHolofoil", {}).get("market")
    )
    #agregamos ala lista los valores importantes
    poke_list.append({
        "nombre": nombre,
        "id": card_id,
        "expansion": expansion,
        "precio": precio if precio else "No disponible"
    })

#creamos el df
df = pd.DataFrame(poke_list)
print(df)