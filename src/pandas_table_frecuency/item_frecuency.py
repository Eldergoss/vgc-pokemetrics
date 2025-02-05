import json
import pandas as pd
from collections import Counter

# Ruta del archivo JSON
ruta = "/home/david/vgc-pokemetrics/data/processed_data/vgc_data.json"

#bloque de inputs


equipos = int(input("numero total de participantes : "))


def cargar_json(ruta_json):
    """Carga el archivo JSON y lo devuelve como un diccionario."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        datos = json.load(file)
    return datos

def top_10_pokemon_frecuencia(datos, total_equipos_pokemon=equipos):
    """Genera una tabla con el top 10 de Pokémon más usados con métricas detalladas."""
    lista_items = []
    
    for equipos in datos.values():
        for items in equipos:
            lista_items.append(items["ítem"])
    
    # Contar la frecuencia de cada Pokémon
    contador = Counter(lista_items)
    
    # Crear DataFrame con el top 10
    df_top_10 = pd.DataFrame(contador.most_common(10), columns=["Pokémon", "Frecuencia Absoluta"])
    
    # Calcular frecuencias acumuladas y relativas
    df_top_10["Frecuencia Acumulada"] = df_top_10["Frecuencia Absoluta"].cumsum()
    df_top_10["Frecuencia Relativa"] = df_top_10["Frecuencia Absoluta"] / 4410
    df_top_10["Frecuencia Relativa Acumulada"] = df_top_10["Frecuencia Relativa"].cumsum()
    
    # Convertir a porcentaje con 2 decimales
    df_top_10["Frecuencia Relativa (%)"] = (df_top_10["Frecuencia Relativa"] * 100).round(2)
    df_top_10["Frecuencia Relativa Acumulada (%)"] = (df_top_10["Frecuencia Relativa Acumulada"] * 100).round(2)
    df_top_10["porcentaje de uso"]= (df_top_10["Frecuencia Absoluta"]*100/total_equipos_pokemon).round(2)

    
    # Ajustar índices desde 1
    df_top_10.index = df_top_10.index + 1
    
    return df_top_10

def guardar_csv(df):
    """Pregunta al usuario el nombre del archivo y guarda el DataFrame en CSV."""
    nombre_archivo = input("📁 Ingresa el nombre del archivo CSV (sin extensión): ").strip()
    if not nombre_archivo.endswith(".csv"):
        nombre_archivo += ".csv"
    
    df.to_csv(nombre_archivo, index=False, encoding="utf-8")
    print(f"✅ Archivo guardado como: {nombre_archivo}")

# Cargar JSON y calcular top 10
datos_json = cargar_json(ruta)
df_top_10 = top_10_pokemon_frecuencia(datos_json)

# Mostrar tabla y guardar CSV
print(df_top_10)
guardar_csv(df_top_10)
