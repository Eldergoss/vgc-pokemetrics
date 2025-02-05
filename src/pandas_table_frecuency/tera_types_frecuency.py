import json
import pandas as pd
from collections import Counter

# Ruta del archivo JSON
ruta = "/home/david/vgc-pokemetrics/data/processed_data/vgc_data.json"

def cargar_json(ruta_json):
    """Carga el archivo JSON y lo devuelve como un diccionario."""
    with open(ruta_json, 'r', encoding='utf-8') as file:
        datos = json.load(file)
    return datos

def top_10_teratipos_frecuencia(datos):
    """Genera una tabla con el top 10 de Teratipos más usados con métricas detalladas."""
    lista_teratipos = []
    
    for equipos in datos.values():
        for pokemon in equipos:
            tera = pokemon["tera_type"]
            if tera != "-":  # Filtrar Teratipos vacíos
                lista_teratipos.append(tera)
    
    # Contar la frecuencia de cada Teratipo
    contador = Counter(lista_teratipos)
    
    # Obtener total de Teratipos válidos
    total_teratipos = sum(contador.values())

    # Crear DataFrame con el top 10
    df_top_10 = pd.DataFrame(contador.most_common(10), columns=["TeraTipo", "Frecuencia Absoluta"])
    
    # Calcular frecuencias relativas y acumuladas
    df_top_10["Frecuencia Relativa"] = df_top_10["Frecuencia Absoluta"] / total_teratipos
    df_top_10["Frecuencia Relativa (%)"] = (df_top_10["Frecuencia Relativa"] * 100).round(2)
    df_top_10["Frecuencia Acumulada"] = df_top_10["Frecuencia Absoluta"].cumsum()
    df_top_10["Frecuencia Relativa Acumulada"] = df_top_10["Frecuencia Relativa"].cumsum()
    df_top_10["Frecuencia Relativa Acumulada (%)"] = (df_top_10["Frecuencia Relativa Acumulada"] * 100).round(2)
    
    # Calcular porcentaje de uso respecto al total de equipos
    total_equipos_pokemon = len(datos) * 6  # Número total de Pokémon en todos los equipos
    df_top_10["Porcentaje de Uso"] = (df_top_10["Frecuencia Absoluta"] * 100 / total_equipos_pokemon).round(2)
    
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
df_top_10 = top_10_teratipos_frecuencia(datos_json)

# Mostrar tabla y guardar CSV
print(df_top_10)
guardar_csv(df_top_10)
