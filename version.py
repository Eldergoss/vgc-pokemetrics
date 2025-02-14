import os
import shutil
import subprocess

# Ruta donde descargaste ChromeDriver
chromedriver_path = "/home/david/Descargas/chromedriver-linux64/chromedriver"

# Ruta destino en /usr/local/bin
install_path = "/usr/local/bin/chromedriver"

def install_chromedriver():
    try:
        # Verificar si el archivo existe
        if not os.path.exists(chromedriver_path):
            print(f"❌ No se encontró ChromeDriver en {chromedriver_path}")
            return
        
        # Mover ChromeDriver a /usr/local/bin
        shutil.move(chromedriver_path, install_path)
        
        # Dar permisos de ejecución
        subprocess.run(["chmod", "+x", install_path], check=True)

        print(f"✅ ChromeDriver instalado correctamente en {install_path}")
    
    except Exception as e:
        print(f"⚠️ Error durante la instalación: {e}")

if __name__ == "__main__":
    install_chromedriver()
