from .data_manager import obtener_data
from .data_manager import agregar_producto
from .conversion_manager import calcular_metricas_producto
from .conversion_manager import calculate_objective
from .conversion_manager import encode_dataframe
from sklearn.model_selection import train_test_split
from .ml_manager import preprocessing_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from .ml_manager import get_model_with_min_std

def total_process(nombre):
    # Obtiene los datos y los pasa a DataFrame
    df = obtener_data(nombre)
    # Agrega columna de productos
    df = agregar_producto(df)
    # Categorizar tabla por producto y agregar nuevos datos
    df_pp = calcular_metricas_producto(df)
    # Calcular variable objetivo
    df_result = calculate_objective(df_pp)
    # Codificar en One-Hot y eliminar columnas que no serán usadas en modelo
    df = encode_dataframe(df_pp) 
    # Separar entre train y test
    X_train, X_test, y_train, y_test = train_test_split(df, df_result, test_size=0.2, random_state=42)
    # Transformar valores númericos en valores consistentes con un modelo de Machine Learning
    X_train_prepared = preprocessing_pipeline.fit_transform(X_train)
    # Ajustar modelos a los datos
    lin_reg = LinearRegression()
    lin_reg.fit(X_train_prepared, y_train)
    forest_reg = RandomForestRegressor(n_estimators=100, random_state=42)
    forest_reg.fit(X_train_prepared, y_train)
    tree_reg = DecisionTreeRegressor(random_state=42)
    tree_reg.fit(X_train_prepared, y_train)
    # Usar Cross Validation para ver el mejor modelo
    scores_linear = cross_val_score(lin_reg, X_train_prepared, y_train,
                        scoring="neg_mean_squared_error", cv=5)
    linear_rmse_scores = np.sqrt(-scores_linear)

    scores_tree = cross_val_score(tree_reg, X_train_prepared, y_train,
                            scoring="neg_mean_squared_error", cv=5)
    tree_rmse_scores = np.sqrt(-scores_tree)

    scores_forest = cross_val_score(forest_reg, X_train_prepared, y_train,
                            scoring="neg_mean_squared_error", cv=5)
    forest_rmse_scores = np.sqrt(-scores_forest)
    # Crear una lista con los modelos correspondientes
    models = [lin_reg, tree_reg, forest_reg]
    # Crear una lista con los RMSE scores correspondientes
    rmse_scores_list = [linear_rmse_scores, tree_rmse_scores, forest_rmse_scores]
    # Encontrar el modelo con menor desviación estándar
    best_model = get_model_with_min_std(models, rmse_scores_list)
    # Usamos el dataframe original de productos total para predecir
    X_total_prepared = preprocessing_pipeline.transform(df)
    # Predecimos
    X_total_predict = best_model.predict(X_total_prepared)
    # Agregar las predicciones al DataFrame df_pp
    df_pp['Prediction'] = X_total_predict
    # Ordenar el DataFrame df_pp por las predicciones en orden descendente
    df_predicted = df_pp.sort_values(by='Prediction', ascending=False)
    return df_predicted

