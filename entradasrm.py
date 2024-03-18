import os
import requests
from bs4 import BeautifulSoup

def send_telegram_message(text):
    token = os.getenv('TOKEN_TL')
    chat_id = os.getenv('CHAT_ID')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    print(response.json())

def check_ticket_availability(url):
    session = requests.Session()
    response = session.get(url)

    if response.status_code == 200:
        # Forzar a BeautifulSoup a usar la codificación de la respuesta
        soup = BeautifulSoup(response.content, 'html.parser')

        cookie_button = soup.find('button', id='onetrust-accept-btn-handler')
        if cookie_button:
            session.get(url)

        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        paragraphs = soup.find_all('p', class_='event-card__text')
        unavailable_text = "Entradas aforo general desde 75 € disponibles próximamente"

        for paragraph in paragraphs:
            # Convierte el texto a minúsculas directamente sin reemplazar espacios o guiones
           # print(f"Verificando párrafo: {paragraph}")  # Para depuración
            if unavailable_text in paragraph:
                return False

        print("El texto que indica la no disponibilidad ha desaparecido. Las entradas podrían estar disponibles.")
        return True
    else:
        print(f"Error al acceder a la página: {response.status_code}")
        return False

ticket_url = 'https://www.realmadrid.com/es-ES/entradas'

if check_ticket_availability(ticket_url):
    print('Las entradas de aforo general pueden estar disponibles.')
    send_telegram_message("Las entradas para el proximo partido estan disponibles")
else:
    print('Las entradas de aforo general aún no están disponibles.')
    send_telegram_message("Las entradas para el proximo partido no estan disponibles")
