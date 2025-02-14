"""import requests

def descargar_html(url, archivo_salida="pagina.html"):
    try:
        respuesta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        respuesta.raise_for_status()  # Lanza un error si el código de estado no es 200
        
        with open(archivo_salida, "w", encoding="utf-8") as archivo:
            archivo.write(respuesta.text)
        
        print(f"HTML guardado en {archivo_salida}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la página: {e}")

if __name__ == "__main__":
    url = input("Introduce la URL a extraer: ")
    descargar_html(url)
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager  

# Opciones para ejecutar Chrome sin interfaz gráfica (headless)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # No abrirá ventana gráfica
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Iniciar Chrome con Selenium y WebDriverManager
service = Service(ChromeDriverManager().install())  
driver = webdriver.Chrome(service=service, options=options)

# Abrir la página
url = "https://ptcg-standings.fly.dev/tournaments/0000147/masters/Henry_Chao_[US]/decklist"
driver.get(url)

# Extraer HTML de la página
html = driver.page_source

# Guardar el HTML en un archivo
with open("pagina.html", "w", encoding="utf-8") as file:
    file.write(html)

print("✅ HTML guardado en 'pagina.html'")

# Cerrar el navegador
driver.quit()
