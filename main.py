#Modulos del ipynb
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# modulos propios
from src.load_data import load_data
from src.limpieza import *
from src.auditoria import *
from src.eda import *
from src.visualizacion import *

raw_csv = "data\\raw\\ai_job_replacement_dirty.csv"

#carga
df = load_data(raw_csv)

print(df.sample(5))

#limpieza
renombrar_columnas(df)
quitar_duplicados(df)
normalizacion_sector(df)
corregir_anio(df)
corregir_formato_salarios(df)
regresion_riesgo_automatizacion(df)

imputacion_salario_antes_IA(df)
regresion_imputacion_salario_despues_IA(df)
imputacion_sector(df)

df = df[df['sector'] == 'Finanzas']

#EDA
outliers(df)
volatilidad_ingresos(df) #nota: Antes de la IA la diferencia entre mediana y media era minima, luego de la ia pasa a ser mayor.
agrupar_promedio_max(df,'pais','indice_brecha_habilidades')

#Visualizacion
grafico_funcion_A(df,'año_registro','salario_antes_IA','salario_despues_IA')
grafico_funcion_torta(df,'categoria_riesgo')
grafico_barras(df,'pais','nivel_adopcion_IA')
