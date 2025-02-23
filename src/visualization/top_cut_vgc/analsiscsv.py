# analisis.py
import pandas as pd
import plotly.express as px

rutacsv = "/home/david/vgc-pokemetrics/src/scraper/limitles_scrap/competidores_top33.csv"

def analizar_csv(csv_filename):
    try:
        df = pd.read_csv(csv_filename)
        
        frecuencia_absoluta = df["Mazo"].value_counts()
        frecuencia_relativa = df["Mazo"].value_counts(normalize=True)
        porcentaje_uso = frecuencia_relativa * 100
        
        resumen_frecuencia = pd.DataFrame({
            "Mazo": frecuencia_absoluta.index,  # Convertir el índice en columna
            "Frecuencia Absoluta": frecuencia_absoluta.values,
            "Frecuencia Relativa": frecuencia_relativa.values,
            "Porcentaje de Uso": porcentaje_uso.values
        })
        
        # Agrupar valores con porcentaje de uso menor a 5%
        threshold = 5
        resumen_frecuencia.loc[resumen_frecuencia["Porcentaje de Uso"] < threshold, "Mazo"] = "Otros"
        resumen_frecuencia = resumen_frecuencia.groupby("Mazo", as_index=False).sum()
        
        print("\nResumen de frecuencias:")
        print(resumen_frecuencia)
        
        fig = px.pie(resumen_frecuencia, 
                     names="Mazo", 
                     values="Frecuencia Absoluta", 
                     title="Distribución de mazos en el Top 33 (Agrupados <5% en 'Otros')")
        print(fig)
        fig.show()
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo CSV.")

if __name__ == "__main__":
    analizar_csv(rutacsv)
