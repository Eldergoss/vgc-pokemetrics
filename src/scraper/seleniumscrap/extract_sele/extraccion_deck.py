# extract_sele/extraccion_deck.py
import pyperclip
import json
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

        return True  # Extracción exitosa

    except Exception as e:
        print(f"❌ Error al copiar el deck del concursante {index+1}: {e}")
        return False  # Indica que la extracción falló

# Si se desea, se puede mantener un bloque para ejecutar directamente este script:
if __name__ == "__main__":
    # Se espera que se pase el índice del concursante como argumento
    index = int(sys.argv[1]) - 1
    # En este caso se asume que se crea un driver y se navega a la página del concursante
    # Por simplicidad, se muestra solo la llamada a la función.
    # En un flujo real, se integraría con la navegación.
    print("Ejecutando extracción independiente...")
