import requests

# URL que quieres extraer
url = 'https://limitlesstcg.com/tournaments/472'

# Hacer la solicitud GET
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Guardar el contenido del HTML en un archivo
    with open('pagina_extraida.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("HTML guardado exitosamente.")
else:
    print(f"Error al hacer la solicitud: {response.status_code}")
