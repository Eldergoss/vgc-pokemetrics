import pyperclip
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar opciones de Chrome
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

# FUNCION DE NAVEGACION
# Abrir la página del torneo y navegar entre los concursantes
def open_tournament_page(driver, url):
    driver.get(url)

    # Esperar a que los elementos con la clase específica estén presentes
    divs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.flex.flex-col.items-start.gap-1"))
    )

    # Verifica que hay al menos dos divs
    if len(divs) > 1:
        for i in range(len(divs)):
            # Crea una acción para hacer clic en el div correspondiente
            actions = ActionChains(driver)
            actions.move_to_element(divs[i]).click().perform()
            print(f"✅ Click realizado en el div {i+1} correctamente.")
            
            # Esperamos 10 segundos para cargar la página del jugador
            time.sleep(10)

            # Llamamos a la función para copiar el deck de este concursante
            copy_deck_and_save(driver, i)
            
            # Regresamos a la página anterior antes de pasar al siguiente concursante
            driver.back()
            time.sleep(5)  # Esperamos un poco para que se recargue la página

    else:
        print("⚠️ No se encontraron suficientes divs.")

# FUNCION DE EXTRACCION
# Realizar el click en los botones y copiar el deck
def copy_deck_and_save(driver, index):
    try:
        # Hacer clic en el botón de desplegar el deck usando el XPath relativo
        button_deck = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/button"))
        )
        button_deck.click()
        print(f"✅ Deck desplegado correctamente para el concursante {index+1}.")
        
        # Esperamos 20 segundos para que se despliegue completamente
        time.sleep(20)

        # Hacer clic en el botón de copiar deck usando el XPath absoluto
        buttoncopy = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div[3]/div/div[2]/div/div/div[1]/button"))
        )
        buttoncopy.click()
        print(f"✅ Deck copiado correctamente para el concursante {index+1}.")
        
        # Esperamos un breve momento para que el texto se copie
        time.sleep(2)

        # Obtener el texto copiado al portapapeles usando pyperclip
        copied_deck = pyperclip.paste()
        print(f"✅ Deck obtenido del portapapeles para el concursante {index+1}.")

        # Guardar el deck copiado en un archivo JSON
        deck_data = {"deck": copied_deck}
        filename = f"deck_{index+1}.json"  # Nombrar el archivo con el índice del concursante
        with open(filename, "w") as json_file:
            json.dump(deck_data, json_file, indent=4)
        print(f"✅ Deck guardado en {filename}.")

    except Exception as e:
        print(f"❌ Error al copiar el deck del concursante {index+1}: {e}")

# Función principal que organiza el flujo
def main():
    # Página de torneo
    url = "https://ptcg-standings.fly.dev/tournaments/0000147/standings"
    driver = initialize_driver()

    try:
        open_tournament_page(driver, url)
    finally:
        # Cierra el navegador
        driver.quit()

# Ejecutar el flujo principal
if __name__ == "__main__":
    main()
