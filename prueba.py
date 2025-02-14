from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess

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
            try:
                # Volver a buscar el div al inicio de cada iteración
                divs = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.flex.flex-col.items-start.gap-1"))
                )

                # Crea una acción para hacer clic en el div correspondiente
                actions = ActionChains(driver)
                actions.move_to_element(divs[i]).click().perform()
                print(f"✅ Click realizado en el div {i+1} correctamente.")
                
                # Esperamos 10 segundos para cargar la página del jugador
                time.sleep(10)

                # Llamamos a la función externa para copiar el deck de este concursante
                subprocess.run(['python3', 'extract_deck.py', str(i+1)])
                
                # Regresamos a la página anterior antes de pasar al siguiente concursante
                driver.back()
                time.sleep(5)  # Esperamos un poco para que se recargue la página

            except Exception as e:
                print(f"❌ Error al hacer clic en el div {i+1}: {e}")
    else:
        print("⚠️ No se encontraron suficientes divs.")

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
