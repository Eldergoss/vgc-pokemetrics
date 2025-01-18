import requests
import os

# Ruta donde quieres guardar el HTML
ruta_html = "/home/david/vgc-pokemetrics/reports/pagina_vgc.html"

# URL de la página del torneo
url = 'https://pokepast.es/9da40dd18cb19713'

# Realizar la solicitud GET
response = requests.get(url)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    html_content = response.text
    print("HTML extraído correctamente")
    # Guardar el HTML en la ruta especificada
    with open(ruta_html, 'w', encoding='utf-8') as file:
        file.write(html_content)
else:
    print(f"Error al obtener la página: {response.status_code}")
