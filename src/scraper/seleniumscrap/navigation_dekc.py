# extract_sele/navigation_deck.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Importamos la función de extracción (que guarda los decks con índices dinámicos)
from extract_sele.extraccion_deck import copy_deck_and_save

def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # Para ver el navegador, comenta la siguiente línea; para modo headless, descoméntala:
    chrome_options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def open_tournament_page(driver, url):
    driver.get(url)
    time.sleep(35)  # Espera inicial para que cargue la página

    index = 0
    while True:
        # Obtenemos la lista actual de concursantes
        divs = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-col.items-start.gap-1")
        if index >= len(divs):
            # Si no hay suficientes elementos, hacemos scroll para cargar nuevos
            driver.execute_script("window.scrollBy(0,300);")  # Aumentado el scroll a 300 píxeles
            time.sleep(10)  # Tiempo de espera incrementado para dar mayor oportunidad a cargar nuevos elementos
            divs = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-col.items-start.gap-1")
            if index >= len(divs):
                print("⚠️ No se encontraron más concursantes. Terminando el proceso.")
                break

        try:
            # Hacemos clic en el concursante actual
            current_div = divs[index]
            actions = ActionChains(driver)
            actions.move_to_element(current_div).click().perform()
            print(f"✅ Click realizado en el concursante {index+1}.")
            time.sleep(15)  # Aumentado el tiempo de espera para que la página del concursante cargue completamente

            # Llamamos a la función de extracción del deck
            extraction_success = copy_deck_and_save(driver, index)
            if extraction_success:
                # Si la extracción fue exitosa, se requiere volver dos veces atrás:
                driver.back()  # Salir de la página del deck
                time.sleep(7)
                driver.back()  # Volver a la lista de concursantes
                time.sleep(7)
            else:
                # Si la extracción falló, regresamos con un solo clic atrás
                driver.back()
                time.sleep(12)
            
            # Luego, después de procesar el concursante, se hace scroll para avanzar
            driver.execute_script("window.scrollBy(0,300);")
            time.sleep(7)
            
            index += 1

        except Exception as e:
            print(f"❌ Error al procesar el concursante {index+1}: {e}")
            index += 1

def main():
    url = "https://ptcg-standings.fly.dev/tournaments/0000147/standings"
    driver = initialize_driver()
    try:
        open_tournament_page(driver, url)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
