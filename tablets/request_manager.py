import pytz
import requests
from time import sleep
from django.utils import timezone
from tablets.models import Tokens
from requests.exceptions import ConnectTimeout

# Método para obtener el access_token y refresh_token de la base de datos
def get_tokens():
    try:
        tokens = Tokens.objects.first()
        if tokens is None:
            return None
        return tokens.access_token, tokens.refresh_token, tokens.expiration_date
    except Tokens.DoesNotExist:
        return None

# Método para guardar el access_token y refresh_token en la base de datos
def save_tokens(access_token, refresh_token, expiration_date):
    # Elimina todos los registros existentes de Tokens
    Tokens.objects.all().delete()
    # Crea un nuevo registro con los datos proporcionados
    Tokens.objects.create(access_token=access_token, refresh_token=refresh_token, expiration_date=expiration_date)

# Método para obtener un nuevo access_token y refresh_token
def get_new_tokens(refresh_token):
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": "5030313997317379",
        "client_secret": "zTJax3dLAiog35gQdaOVEhTSwxXxbTTY",
        "refresh_token": refresh_token
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    data = response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_in = data['expires_in']
    expiration_date = timezone.now() + timezone.timedelta(seconds=expires_in)
    save_tokens(access_token, refresh_token, expiration_date)
    return access_token, refresh_token, expiration_date

# Método para hacer una petición a la API
def do_request(url, params=None):
    tokens = get_tokens()
    if tokens is None or tokens[2] < timezone.now():
        refresh_token = tokens[1] if tokens is not None else input("Ingrese refresh_token: ")
        access_token, refresh_token, _ = get_new_tokens(refresh_token)
    else:
        access_token, refresh_token, _ = tokens
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    retries = 3  # Número máximo de reintentos
    retry_delay = 30  # Tiempo de espera en segundos antes de cada reintento
    
    for _ in range(retries):
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)  # Establece un tiempo de espera de 10 segundos
            response.raise_for_status()
            data = response.json()
            return data
        except ConnectTimeout:
            print("Error de tiempo de espera de conexión. Se realizará un reintento después de 30 segundos...")
            sleep(retry_delay)
    
    print("Se ha excedido el número máximo de intentos de conexión. Se aborta la solicitud.")
    return None

# Método para obtener las visitas de cada producto
def get_product_visits(product_id):
    today = timezone.now().date()
    last_month = today - timezone.timedelta(days=30)
    
    endpoint = "https://api.mercadolibre.com/visits/items"
    params = {
        "ids": product_id,
        "date_from": last_month.isoformat(),
        "date_to": today.isoformat()
    }

    # Aquí se utiliza la función do_request para realizar la solicitud con el access token
    response = do_request(endpoint, params=params)
    if response and isinstance(response, dict):
        product_visits = response.get(product_id)
        return product_visits
    
    return None