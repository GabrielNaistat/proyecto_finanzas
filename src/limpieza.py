#from columnas import COLUMNAS
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np

def renombrar_columnas(df):
    print("========RENOMBRAR COLUMNAS========")
    #df.columns= COLUMNAS
    df.columns= ['identificador',
                 'profesion',
                 'sector',
                 'pais',
                 'año_registro',
                 'riesgo_automatizacion_estimado%',
                 'puntaje_reemplazo_IA',
                 'indice_brecha_habilidades',
                 'salario_antes_IA',
                 'salario_despues_IA',
                 'variacion_porcentual_salarial',
                 'crecimiento_demanda_habilidades%',
                 'factibilidad_trabajo_rem',
                 'nivel_adopcion_IA',
                 'nivel_educativo_req','categoria_riesgo',
                 'presion_reconversion_laboral',
                 'indice_volatilidad_salarial',
                 'urgencia_reentrenamiento',
                 'intensidad_global_disrupcion_IA']

def quitar_duplicados(df):
    print("========QUITAR DUPLICADOS========")
    #print("Filas completamente duplicadas:", df.duplicated().sum())
    df = df.drop_duplicates()
    print("Filas completamente duplicadas:", df.duplicated().sum())

def normalizacion_sector(df) :
    """Normalizamos los valores de la columna sector para que no haya inconsistencias de formato"""

    print("========NORMALIZACION SECTOR========")

    # revisamos como estan los valores unicos de la columna sector antes de normalizar
    print(df['sector'].unique())
    
    # corregimos inconsistencias de formato Finance
    diccionario = ['FINANCE','Finance',' Finance ','finance']
    df['sector'] = df['sector'].replace(diccionario, 'Finanzas')

    # corregimos inconsistencias de formato Technology
    diccionario = ['Technology','technology','TECHNOLOGY',' Technology ']
    df['sector'] = df['sector'].replace(diccionario, 'Tecnologia')

    # corregimos inconsistencias de formato Manufactura
    diccionario = ['manufacturing','Manufacturing',' Manufacturing ','MANUFACTURING']
    df['sector'] = df['sector'].replace(diccionario, 'Manufactura')

    # corregimos inconsistencias de formato Salud
    diccionario = ['Healthcare','healthcare',' Healthcare ','HEALTHCARE']
    df['sector'] = df['sector'].replace(diccionario, 'Salud')

    # corregimos inconsistencias de formato Comercio y Minorista
    diccionario = [' Retail ','Retail','RETAIL','retail']
    df['sector'] = df['sector'].replace(diccionario, 'Comercio y Minorista')

    # corregimos inconsistencias de formato Educacion
    diccionario = ['Education','education',' Education ','EDUCATION']
    df['sector'] = df['sector'].replace(diccionario, 'Educacion')

    # corregimos inconsistencias de formato Transporte
    diccionario = ['Transportation','transportation',' Transportation ','TRANSPORTATION']
    df['sector'] = df['sector'].replace(diccionario, 'Transporte')

    # corregimos inconsistencias de formato Energia
    diccionario = ['Energy','energy',' Energy ','ENERGY']
    df['sector'] = df['sector'].replace(diccionario, 'Energia')

    # revisamos como quedaron los valores unicos de la columna sector despues de normalizar
    print(df['sector'].unique())


def corregir_anio(df): 
    """Corregimos el formato de la columna año_registro para que sea int para mejorar la consistencia de los datos y evitar errores en el análisis posterior
    """

    print("========CORREGIR AÑO========")
    print(df['año_registro'].unique())

    # convertimos la columna a int
    df['año_registro'] = df['año_registro'].astype(int)

    print(df['año_registro'].unique())

def corregir_formato_salarios(df) :
    """Corregimos el formato de los valores de las columnas de salarios para que sean numéricas y mejorar la consistencia de los datos
    """

    print("========CORREGIR FORMATO SALARIOS========")

    # columna salario_antes_IA
    df['salario_antes_IA'] = (df['salario_antes_IA'].str.replace('$','', regex=False).str.replace(',', '', regex=False))
    # convertimos a valor numerico aquellos valores que pueden ser reconvertidos en numero, y los que no pueden son convertidos a NaN
    df['salario_antes_IA'] = pd.to_numeric(df['salario_antes_IA'])

    #columna salario_despues_IA
    df['salario_despues_IA'] = (df['salario_despues_IA'].str.replace('$', '', regex=False).str.replace(',', '', regex=False))
    # convertimos a valor numerico aquellos valores que pueden ser reconvertidos en numero, y los que no pueden son convertidos a NaN
    df['salario_despues_IA'] = pd.to_numeric(df['salario_despues_IA'])


# crea modelo de regresion lineal buscando entradas con mayor correlacion, en este caso las variable predictora es "salario_despues_IA" para predecir objetivo "salario_antes_IA"
# divide train y pred. train: df con columnas "salario_antes_IA" y "salario_despues_IA" ambas colums sin nulas
# pred: df con columnas "salario_antes_IA" nula y "salario_despues_IA" no nula

def regresion_imputacion_salario_antes_IA(df):  # tommy  --- sub main 1 para imputar "salario_antes_IA"---

    print("========REGRESION SALARIO ANTES========")

    # columna a imputar "salario_antes_IA"
    v_imputar = 'salario_antes_IA'
    # calculamos la matriz de correlacion para ver que columnas tienen mayor correlacion con la columna a imputar
    matriz_corr = df.corr(numeric_only=True)[v_imputar].sort_values(ascending=False)
    # seleccionamos las columnas con correlacion mayor a 0.5 o menor a -0.5 solo que le sacamos el signo y queda como correlaciones 0.5 aunque sea -0.5
    cols_relevante =  matriz_corr[abs(matriz_corr) > 0.5]      
    print("Columnas con mas de 0.5 de correlacion \n: ", cols_relevante)
    cols_relevante = matriz_corr[(abs(matriz_corr)) > 0.5].index.to_list() # convertimos en lista aquellas columnas con mayor correlacion, queda adentro solamente la columna "salario_antes_IA" y "salario_despues_IA"
    # eliminamos la columna objetivo a imputar de la lista de columnas relevantes pq no podemos usarla como predictora
    cols_relevante.remove(v_imputar)
    print(cols_relevante) 


    # CREAMOS EL MODELO DE REGRESION LINEAL PARA IMPUTAR LOS VALORES NULOS DE LA COLUMNA SALARIO_ANTES_IA
    # entradas a entrenar: aquellas que no tienen nulos en la columna objetivo y que no tienen nulos en las columnas predictoras

    # REGRESION LINEAL SIMPLE ENTRE SALARIO_ANTES_IA Y SALARIO_DESPUES_IA
    
    # train se filtran aquellas filas que no tienen nulos en la columna objetivo y que no tienen nulos en la columna predictora con la mayor correlacion
    train = df[(df['salario_antes_IA'].notna()) & (df['salario_despues_IA'].notna())] 

    # datos que va a imputar el modelo
    # pred se filtran las filas con nulos en la columna objetivo y que no tienen nulos en la columna predictora con la mayor correlacion
    pred = df[(df['salario_antes_IA'].isna()) & (df['salario_despues_IA'].notna())] 

    # x: variable predictora, y: variable objetivo
    # x = train[['salario_despues_IA']] columna sin nulos
    # y = train['salario_antes_IA']     columna sin nulos
    X = train[['salario_despues_IA']]
    y = train['salario_antes_IA']

    # dividimos el dataset en train y test para evaluar el modelo
    # train_test_split divide el dataset en 4 partes: X_train, X_test, y_train, y_test
    # test_size=0.2 significa que el 20% del dataset se usará para test y el 80% para train
    # random_state=100 significa que se usará una semilla para que la división sea reproducible
    
    # x_train y x_test son los datos de entrada para entrenar y evaluar el modelo
    # y_train y y_test son los datos de salida para entrenar y evaluar el modelo

    # todos estos datos tain y test no tienen nulos, son para entrenar y evaluar el modelo
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=100
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # Luego de entrenar el modelo con los datos (no nulos) de entrenamiento, predecimos los valores de la columna objetivo (salario_antes_IA) para los datos de prueba (X_test) y comparamos con los valores reales (y_test) con los valores predichos del modelo para evaluar el modelo
    predicciones = modelo.predict(X_test)

    # predicciones es un array con los valores predichos por el modelo para los datos de prueba (X_test)

    # evaluamos el modelo con el coeficiente de determinación R², que indica qué tan bien se ajusta el modelo a los datos. Un valor de R² cercano a 1 indica un buen ajuste, mientras que un valor cercano a 0 indica un mal ajuste.
    # y_test son los valores reales de la variable a predecir sin nulos, y predicciones son los valores predichos del modelo 
    print("R² =", r2_score(y_test, predicciones))
    
    # filtramos la variable pred, que contiene filas nulas en colum objetivo (salario_antes_IA) y no nulos en colum predictora (salario_despues_IA), nos quedamos con la columna predictora para predecir los valores nulos de la columna objetivo
    X_pred = pred[['salario_despues_IA']]

    # completamos los valores nulos de la columna salario_antes_IA con las predicciones del modelo
    # pred.index son los indices de las filas que tienen nulos en la columna objetivo (salario_antes_IA) y no nulos en la columna predictora (salario_despues_IA)
    df.loc[pred.index,'salario_antes_IA'] = modelo.predict(X_pred) 


def mediana_imputacion_salario_antes_IA(df) :  # tommy  --- sub main 1 para imputar "salario_antes_IA"---
    print("========MEDIANA SALARIO ANTES========")
    # transform('median') calcula la mediana de la columna salario_antes_IA para cada grupo de profesion y fillna() completa los valores nulos de la columna salario_antes_IA con la mediana correspondiente a cada grupo de profesion
    df['salario_antes_IA'] = df['salario_antes_IA'].fillna( df.groupby('profesion')['salario_antes_IA'].transform('median'))


def imputacion_salario_antes_IA(df) :  # tommy --- main 1 para imputar "salario_antes_IA"---
    print("========IMPUTAR SALARIO ANTES========")

    # imputa por regresion lineal la columna "salario_antes_IA"
    regresion_imputacion_salario_antes_IA(df)

    # si quedan nulos en la columna "salario_antes_IA" imputamos por mediana de la columna "salario_antes_IA" agrupada por profesion
    mediana_imputacion_salario_antes_IA(df)


# imputamos con otro modelo de regresion lineal para imputar "salario_despues_IA". Previamente antes de ejecutar esta funcion ya se imputaron los nulos de la columna "salario_antes_IA"
def regresion_imputacion_salario_despues_IA(df) :  # tommy  --- main 2 para imputar "salario_despues_IA"---
    print("========IMPUTAR SALARIO DESPUES========")

    # calculamos la correlacion de las columnas con la columna a imputar "salario_despues_IA"
    v_imputar = 'salario_despues_IA'
    matriz_corr = df.corr(numeric_only=True)[v_imputar].sort_values(ascending=False)
    cols_relevante =  matriz_corr[abs(matriz_corr) > 0.5]
    print("Columnas con mas de 0.5 de correlacion \n: ", cols_relevante)
    cols_relevante = matriz_corr[abs(matriz_corr) > 0.5].index.to_list() #lista de columnas predictoras con mayor correlacion
    cols_relevante.remove(v_imputar) 
    print(cols_relevante) # la unica variable predictora con mayor correlacion es "salario_antes_IA"


    
    # AHORA LLENAMOS LOS NULOS DE LA COLUMNA SALARIOS_DESPUES_IA, creando un modelo de regresion lineal con las columnas que tienen mayor correlacion con la columna a objetivo a imputar
    # en este caso la variable predictora con mas correlacion es "salario_antes_IA" y la variable objetivo es "salario_despues_IA"

    # train guarda las filas no nulas en la columna objetivo (salario_despues_IA), 
    # no hace falta filtrar las filas no nulas en la columna predictora (salario_antes_IA) pq ya estan imputadas previamente al entrar en esta funcion
    train = df[df[v_imputar].notna()]

    # pred filtra solamente el df con la columna a imputar (salario_despues_IA) nula, y la columna predictora (salario_antes_IA) queda no nula 
    pred = df[df[v_imputar].isna()]
    
    # datos "x","y" de entrenamiento no nulos para el modelo de regresion lineal
    X = train[['salario_antes_IA']] # columna predictora con datos no nulos
    y = train['salario_despues_IA'] # columna objetivo con datos no nulos

    # division de datos no nulos en "x","y" para entrenamiento y testeo del modelo
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    # se guardan las predicciones del modelo usando como entrada los x_test
    predicciones = modelo.predict(X_test)

    # se miden las predicciones del modelo con los valores reales de y_test
    print("R² =", r2_score(y_test, predicciones))

    # x_pred guarda la columna predictora q estan imputados
    X_pred = pred[['salario_antes_IA']]

    # predecimos los valores nulos de la columna salario_despues_IA con las predicciones del modelo
    df.loc[pred.index,'salario_despues_IA'] = modelo.predict(X_pred)



def regresion_riesgo_automatizacion(df) :
    """Imputamos los valores nulos de la columna riesgo_automatizacion_estimado% con un modelo de regresion lineal con las columnas que tienen mayor correlacion con la columna a imputar/objetivo"""

    print("========RIESGO AUTOMATIZACION========")
    v_imputar = 'riesgo_automatizacion_estimado%'
    #print(df.corr(numeric_only=True)['riesgo_automatizacion_estimado%'].sort_values(ascending=False))
    matriz_corr = df.corr(numeric_only=True)[v_imputar].sort_values(ascending=False)
    cols_relevante =  matriz_corr[matriz_corr > 0.5]
    print("Columnas con mas de 0.5 de correlacion : \n", cols_relevante)
    cols_relevante = matriz_corr[matriz_corr > 0.5].index.to_list() #lista de columnas
    cols_relevante.remove(v_imputar)
    print(cols_relevante)

    # variable respuesta
    train = df[df[v_imputar].notna()]

    # Filas a imputar
    pred = df[df[v_imputar].isna()]

    # Variables predictoras
    X = train[cols_relevante]

    # Variable objetivo
    y = train[v_imputar]

    # Evaluación del modelo
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=100
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    predicciones = modelo.predict(X_test)

    print("R² =", r2_score(y_test, predicciones))

    # Entrenamiento final con todos los datos disponibles
    modelo.fit(X, y)

    # Imputación
    X_pred = pred[cols_relevante]

    df.loc[
        pred.index, #indices de los que son NaN
        v_imputar
    ] = modelo.predict(X_pred) #completa con predicciones


def imputacion_sector(df) :
    print("========IMPUTAR SECTOR========")
    # AHORA LLENAMOS LOS NULOS DE LA COLUMNA SECTOR
    mascara = df['sector']=='Finanzas'
    print('Cantidad de nulos en sector:',df['sector'].isna().sum())
    print('Cantidad de registros FINANZAS:', df['sector'][df['sector']=='Finanzas'].value_counts())

    # ??????????
    df['sector'] = df['sector'].fillna(df.groupby('profesion')['sector'].transform(lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan))


    print('Cantidad de nulos en sector despues imputacion:',df['sector'].isna().sum())
    print('Cantidad de registros FINANZAS despues imputacion:', df['sector'][df['sector']=='Finanzas'].value_counts())





    
####################################################################
####################################################################

if __name__ == "__main__":


    print(f"¡Has ejecutado el módulo de limpieza directamente!")
    raw_csv = "data\\raw\\ai_job_replacement_dirty.csv"

    df = pd.read_csv(raw_csv)


    renombrar_columnas(df)
    quitar_duplicados(df)
    normalizacion_sector(df)
    corregir_anio(df)
    corregir_formato_salarios(df)
    regresion_riesgo_automatizacion(df)
    imputacion_salario_antes_IA(df)
    regresion_imputacion_salario_despues_IA(df)
    imputacion_sector(df)
