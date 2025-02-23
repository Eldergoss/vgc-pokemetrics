import requests
import pandas as pd

# 🔑 API Key de Pokémon TCG (Reemplázala con la tuya)
API_KEY = "TU_API_KEY_AQUI"

# 🎴 Expansión a consultar (Ejemplo: "sv04" para Paradox Rift)
SET_ID = "sv3"

# 📌 URL de la API
URL = f"https://api.pokemontcg.io/v2/cards?q=set.id:{SET_ID}"
HEADERS = {"X-Api-Key": API_KEY}

def obtener_datos_expansion():
    """Obtiene todas las cartas de una expansión desde la API de Pokémon TCG."""
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error en la API: {response.status_code}")
        return []

def extraer_precios(cartas):
    """Extrae todos los precios de TCGPlayer para cada carta y devuelve una lista con la información."""
    cartas_con_precios = []
    
    for carta in cartas:
        if "tcgplayer" in carta and "prices" in carta["tcgplayer"]:
            precios = carta["tcgplayer"]["prices"]
            
            # 📌 Extraer precios de todas las versiones disponibles (normal, holofoil, reverseHolofoil, etc.)
            detalles_precios = {}
            for version, valores in precios.items():
                for key, value in valores.items():
                    detalles_precios[f"{version}_{key}"] = value  # Ejemplo: normal_market, holofoil_high
            
            # 📌 Añadir información de la carta con todos los precios disponibles
            if detalles_precios:
                carta_info = {
                    "nombre": carta["name"],
                    "id": carta["id"],
                    "set": SET_ID,
                    **detalles_precios  # Agregar todos los precios
                }
                cartas_con_precios.append(carta_info)
    
    return cartas_con_precios

def guardar_en_csv(datos, filename):
    """Guarda la lista de cartas en un archivo CSV usando Pandas."""
    df = pd.DataFrame(datos)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"📂 Datos guardados en {filename}")
    return df

def main():
    """Ejecuta el proceso de obtención, extracción y guardado de precios."""
    cartas = obtener_datos_expansion()
    cartas_con_precios = extraer_precios(cartas)
    
    if cartas_con_precios:
        # 🔎 Ordenar por el precio de mercado más alto disponible
        for carta in cartas_con_precios:
            carta["max_market"] = max(
                (carta.get(key, 0) for key in carta.keys() if "market" in key),
                default=0
            )
        cartas_con_precios.sort(key=lambda x: x["max_market"], reverse=True)

        # 📊 Guardar en CSV y mostrar DataFrame
        df = guardar_en_csv(cartas_con_precios, "precios_expansion.csv")
        print("\n📊 DataFrame de los precios obtenidos:")
        print(df.head(20))  # Muestra las primeras 20 cartas más caras
    else:
        print("⚠️ No se encontraron cartas con precios disponibles.")

if __name__ == "__main__":
    main()
