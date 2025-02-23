import requests

# Clave de API (NO compartir en público)
API_KEY = "f93a9b96-7e93-42a9-8361-e1e5a01dfbb0"  # Usa tu propia clave

# Set específico a analizar
SET_ID = "sv4"  # Cambia por el set deseado

# Hacer la solicitud a la API
url = f"https://api.pokemontcg.io/v2/cards?q=set.id:{SET_ID}"
headers = {"X-Api-Key": API_KEY}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()["data"]

    # Extraer cartas con precios
    cartas_con_precios = []
    for carta in data:
        if "tcgplayer" in carta and "prices" in carta["tcgplayer"]:
            precios = carta["tcgplayer"]["prices"]
            precio = precios.get("holofoil", {}).get("market") or precios.get("reverseHolofoil", {}).get("market")

            if precio:
                cartas_con_precios.append({"nombre": carta["name"], "precio": precio})

    # Ordenar por precio y obtener el top 10
    top_10 = sorted(cartas_con_precios, key=lambda x: x["precio"], reverse=True)[:10]

    print("Top 10 cartas más caras del set", SET_ID)
    for i, carta in enumerate(top_10, start=1):
        print(f"{i}. {carta['nombre']} - ${carta['precio']:.2f}")

else:
    print("Error en la API:", response.status_code)
