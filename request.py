from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager

# Configurar Selenium con Firefox
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # No abrir navegador
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service, options=options)

# URL base del torneo
BASE_URL = 'https://ptcg-standings.fly.dev'
TOURNAMENT_URL = f'{BASE_URL}/tournaments/0000147/standings'

# 1️⃣ Abrir la página de standings
driver.get(TOURNAMENT_URL)
time.sleep(5)  # Esperar carga

# 2️⃣ Extraer el primer enlace de participante
soup = BeautifulSoup(driver.page_source, "html.parser")
first_participant = soup.find("div", class_="cursor-pointer")

if first_participant:
    link = first_participant.find("a")
    if link and link.get("href"):
        participant_url = BASE_URL + link["href"]
        print(f"🔗 Abriendo perfil: {participant_url}")

        # 3️⃣ Abrir perfil del participante
        driver.get(participant_url)
        time.sleep(3)  # Esperar carga

        # 4️⃣ Buscar y hacer clic en el botón correcto
        try:
            deck_button = driver.find_element(By.XPATH, "//button[contains(text(), 'event')]")
            ActionChains(driver).move_to_element(deck_button).click().perform()
            time.sleep(3)  # Esperar que cargue

            # 5️⃣ Obtener el HTML actualizado después de la carga
            html_after_click = driver.page_source

            # 6️⃣ Guardar el HTML en un archivo
            with open("deck_prueba.html", "w", encoding="utf-8") as file:
                file.write(html_after_click)

            print("✅ HTML después del clic guardado en 'deck_prueba.html'")

        except Exception as e:
            print(f"❌ Error al hacer clic en el botón: {e}")

else:
    print("⚠ No se encontró el primer participante.")

# Cerrar Selenium
driver.quit()
