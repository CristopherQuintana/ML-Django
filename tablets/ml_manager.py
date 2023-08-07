from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Definir las columnas numéricas y categóricas para el ColumnTransformer
numeric_features = ['average_price']

# Definir la Pipeline para la transformación de datos
preprocessing_pipeline = ColumnTransformer([
    ('numeric', MinMaxScaler(), numeric_features),
], remainder='passthrough')

def get_model_with_min_std(models, rmse_scores):
    min_std_idx = np.argmin([np.std(scores) for scores in rmse_scores])
    return models[min_std_idx]