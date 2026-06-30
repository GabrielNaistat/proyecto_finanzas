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
from src.auditoria import auditoria_completa
from src.eda import *
from src.visualizacion import *

raw_csv = "data\\raw\\ai_job_replacement_dirty.csv"

#carga
df = load_data(raw_csv)

# auditoria
auditoria_completa(df)

#limpieza
df = renombrar_columnas(df)
df = quitar_duplicados(df)
df = normalizacion_sector(df)
df = corregir_anio(df)
df = corregir_formato_salarios(df)

#Limpieza imputacion

df = imputacion_salario_antes_IA(df)
df = regresion_imputacion_salario_despues_IA(df)
df = regresion_riesgo_automatizacion(df)
df = imputacion_sector(df)

df = df[df['sector'] == 'finanzas']

#EDA
outliers(df) #para quitar valores negativos
volatilidad_ingresos(df) #nota: Antes de la ia la diferencia entre mediana y media era minima, luego de la ia pasa a ser mayor.
agrupar_promedio_max(df,'pais','indice_brecha_habilidades')


#Visualizacion
grafico_funcion_A(df,'año_registro','salario_antes_ia','salario_despues_ia')
grafico_funcion_torta(df,'categoria_riesgo')
grafico_barras(df,'pais','nivel_adopcion_ia')
plt.show()

print(df.info())
df.to_csv('data/processed/ai_job_replacement_clean.csv', index=False, sep=';')