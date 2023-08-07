from .models import PCs, Notebooks, Impresoras, Tablets
from django.utils import timezone
from datetime import datetime, timedelta, date
import pandas as pd
from .request_manager import do_request, get_product_visits

productos = {
    "tablets": "https://api.mercadolibre.com/sites/MLC/search?category=MLC82067",
    "notebooks": "https://api.mercadolibre.com/sites/MLC/search?category=MLC1652",
    "pcs": "https://api.mercadolibre.com/sites/MLC/search?category=MLC181025",
    "impresoras": "https://api.mercadolibre.com/sites/MLC/search?category=MLC1676"
}

productos_modelos = {
    "notebooks": Notebooks,
    "tablets": Tablets,
    "pcs": PCs,
    "impresoras": Impresoras,
}

# Método para insertar los datos en la tabla
def insert_data(table_name, data):
    # Utiliza el modelo adecuado según el tipo de producto (table_name)
    model_class = productos_modelos[table_name]

    # Itera sobre los datos y guarda cada instancia del modelo individualmente
    for item in data:
        instance = model_class(**item)
        instance.save()
    
# Método para obtener los datos de la tabla correspondientes a esta semana
def get_data(table_name):
    # Obtener la fecha de inicio y fin de la semana actual
    fecha_actual = timezone.now()
    fecha_inicio_semana = fecha_actual - timedelta(days=7)

    # Consulta utilizando el Django ORM para obtener los datos de la semana actual
    model_class = productos_modelos[table_name]
    df = model_class.objects.filter(date_retrieved__range=(fecha_inicio_semana, fecha_actual))

    return df


# Método para verificar si los datos de la API son más viejos a una semana
def check_data_age(table_name):
    # Utiliza el modelo adecuado según el tipo de producto (table_name)
    model_class = productos_modelos[table_name]

    try:
        # Obtiene la fecha más reciente en la tabla utilizando el Django ORM
        latest_retrieved_date = model_class.objects.latest('date_retrieved').date_retrieved
        if latest_retrieved_date is None:
            return True
        else:
            # Verifica si los datos son más viejos a una semana
            return timezone.now() - latest_retrieved_date > timedelta(days=7)
    except model_class.DoesNotExist:
        return True
    
# Método para obtener datos por página y guardarlos en la base de datos utilizando insert_data
def obtener_datos_por_pagina(total_resultados, url, table_name):
    resultados_por_pagina = 50
    paginas = total_resultados // resultados_por_pagina
    datos_filtrados_full = []

    for pagina in range(1, paginas + 1):
        parametros = {
            "offset": (pagina - 1) * resultados_por_pagina,
            "limit": resultados_por_pagina
        }
        respuesta = do_request(url, parametros)
        if "results" in respuesta and respuesta["results"]:
            datos_pagina = respuesta["results"]
        else:
            break

        for publicacion in datos_pagina:
            # Crea un diccionario con los datos filtrados para cada publicación
            publicacion_filtrada = {
                "id": publicacion["id"],
                "title": publicacion["title"],
                "condition": publicacion["condition"],
                "price": publicacion["price"],
                "permalink": publicacion["permalink"],
                "thumbnail": publicacion["thumbnail"],
                "sold_quantity": publicacion["sold_quantity"],
                "available_quantity": publicacion["available_quantity"],
                "seller_id": publicacion["seller"]["id"],
                "seller_nickname": publicacion["seller"]["nickname"],
                "brand": None,
                "line": None,
                "model": None,
                "shipping": publicacion["shipping"]["free_shipping"],
                "visits_last_month": get_product_visits(publicacion["id"]),
                "date_retrieved": timezone.now()
            }
            for atributo in publicacion["attributes"]:
                if atributo["id"] == "BRAND":
                    publicacion_filtrada["brand"] = atributo["value_name"]
                elif atributo["id"] == "LINE":
                    publicacion_filtrada["line"] = atributo["value_name"]
                elif atributo["id"] == "MODEL":
                    publicacion_filtrada["model"] = atributo["value_name"]

            # Agrega el diccionario a la lista de datos filtrados
            datos_filtrados_full.append(publicacion_filtrada)

    # Inserta los datos en la base de datos utilizando la función insert_data
    insert_data(table_name, datos_filtrados_full)

    # Crea un DataFrame con los datos filtrados
    dataframe = pd.DataFrame(datos_filtrados_full)

    return dataframe

total_resultados = 3950

def obtener_data(producto):
    if check_data_age(producto):
        df_product = obtener_datos_por_pagina(total_resultados, productos[producto], producto)
    else:
        # Obtiene los datos de la tabla
        df_product_queryset = get_data(producto)
        df_product = pd.DataFrame.from_records(df_product_queryset.values())
    return df_product

# Definir una función para agregar la columna 'producto'
def agregar_producto(df):
    df = df.copy()
    df['producto'] = df['brand'] + ' '+ df['line'] + ' ' + df['model']
    return df