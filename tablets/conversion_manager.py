from .models import PCs, Notebooks, Impresoras, Tablets
from datetime import datetime, timedelta, date
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split

def calcular_metricas_producto(df):
    
    # Filtrar los resultados con menos de 50 visitas
    df = df[df['visits_last_month'] >= 50]
    
    # Agrupar por la columna "producto"
    grouped_df = df.groupby('producto')
    
    # Calcular la suma de "sold_quantity" y "visits_last_month" para cada grupo
    total_sold_quantity = grouped_df['sold_quantity'].sum()
    total_visits_last_month = grouped_df['visits_last_month'].sum()
    
    # Calcular el promedio de "price" para cada grupo
    average_price = grouped_df['price'].mean()
    
    # Obtener el "permalink" y "thumbnail" del primer producto detectado en cada grupo
    first_product_data = grouped_df.first()
    permalink = first_product_data['permalink']
    thumbnail = first_product_data['thumbnail']
    
    # Obtener el primer valor de "brand", "model" y "line" para cada grupo
    brand = first_product_data['brand']
    model = first_product_data['model']
    line = first_product_data['line']
    
    # Contar el número único de vendedores para cada grupo (producto)
    total_sellers = grouped_df['seller_id'].nunique()
    
    # Calcular la variable "sells_per_visit" (ventas por visita)
    sells_per_visit = total_sold_quantity / total_visits_last_month
    sells_per_visit = sells_per_visit.fillna(0)  # Reemplazar NaN con cero
    
    # Calcular la desviación estándar de "visits_last_month" para cada grupo (producto)
    std_visits_last_month = grouped_df['visits_last_month'].std()
    
    # Reemplazar NaN en std_visits_last_month con el promedio de las desviaciones estándar existentes
    std_visits_last_month_max = std_visits_last_month.max()
    std_visits_last_month = std_visits_last_month.fillna(std_visits_last_month_max)
    
    # Crear el nuevo DataFrame con las métricas calculadas
    result_df = pd.DataFrame({
        'product': total_sold_quantity.index,
        'brand': brand.values,
        'line': line.values,
        'model': model.values,
        'average_price': average_price.values,
        'total_sold_quantity': total_sold_quantity.values,
        'total_visits_last_month': total_visits_last_month.values,
        'total_sellers': total_sellers.values,
        'sells_per_visit': sells_per_visit.values,
        'std_visits_last_month': std_visits_last_month.values,
        'permalink': permalink.values,
        'thumbnail': thumbnail.values
        
    })
    
    # Ordenar el DataFrame por "total_visits_last_month" en orden descendente
    #result_df = result_df.sort_values(by='total_visits_last_month', ascending=False)
    result_df = result_df.sort_values(by='total_sellers', ascending=False)
    #result_df = result_df.sort_values(by='total_sold_quantity', ascending=False)

    
    return result_df

# Definir una clase personalizada para calcular la variable objetivo

# CLASE A DEFINIR
class ObjectiveValueCalculator(BaseEstimator, TransformerMixin):
    def __init__(self, weight_total_visits=0.45, weight_sells_per_visit=0.15, weight_std_visits=0.3, weight_total_sellers = 0.1):
        self.weight_total_visits = weight_total_visits
        self.weight_sells_per_visit = weight_sells_per_visit
        self.weight_std_visits = weight_std_visits
        self.weight_total_sellers = weight_total_sellers
        self.scaler = MinMaxScaler()

    def fit(self, x, y=None):
        # Ajustar el MinMaxScaler a los datos
        self.scaler.fit(x)
        return self

    def transform(self, x):
        # Escalar los datos utilizando el MinMaxScaler
        x_scaled = self.scaler.transform(x)

        # Calcular la variable objetivo
        label = (self.weight_total_visits * x_scaled[:, 2]) + \
                (self.weight_sells_per_visit * x_scaled[:, 4]) + \
                (self.weight_std_visits * (1 - x_scaled[:, 5])) + \
                (self.weight_total_sellers * x_scaled[:, 3]) 


        return label

# CUARTA FUNCIÓN
def calculate_objective(df):
    # Seleccionar solo las columnas numéricas del DataFrame
    df_numeric = df.select_dtypes(include='number')
    
    # Definir el objetivo utilizando la clase personalizada ObjectiveValueCalculator
    objective_calculator = ObjectiveValueCalculator()
    df_label = objective_calculator.fit_transform(df_numeric)
    
    return df_label

# Definir las transformaciones que se aplicarán a las columnas
# En este caso, aplicamos OneHotEncoder solo a la columna 'brand'
# QUINTA FUNCIÓN
def encode_dataframe(df):
    # Crear el transformador para One-Hot Encoding de la columna 'brand'
    one_hot = ColumnTransformer([
        ('', OneHotEncoder(sparse_output=False), ['brand'])
    ])

    # Aplicar las transformaciones al DataFrame original
    brand_encoded = one_hot.fit_transform(df)

    # Convertir la matriz resultante en un DataFrame
    df_encoded = pd.DataFrame(brand_encoded)

    # Obtener nombres de columnas para brand
    df_encoded.columns = one_hot.get_feature_names_out(input_features=df.columns)
    
    # Columnas a eliminar
    columns=['product', 'line', 'model', 'total_sold_quantity', 'brand', 'total_visits_last_month', 'total_sellers', 'sells_per_visit', 'std_visits_last_month', 'permalink', 'thumbnail']
    
    # Eliminar la columnas asignadas del DataFrame original
    df_without_brand = df.drop(columns=columns)
    # Concatenar el DataFrame codificado con el DataFrame original sin la columna 'brand'
    df_combined = pd.concat([df_without_brand, df_encoded], axis=1)

    return df_combined