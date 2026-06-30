#from columnas import COLUMNAS
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import numpy as np

def renombrar_columnas(df):
    print("========RENOMBRAR COLUMNAS========")
    #df.columns= COLUMNAS
    print("\nColumnas antes de renombrar: \n", df.columns)
    df.columns= ['identificador',
                 'profesion',
                 'sector',
                 'pais',
                 'año_registro',
                 'riesgo_automatizacion_estimado%',
                 'puntaje_reemplazo_ia',
                 'indice_brecha_habilidades',
                 'salario_antes_ia',
                 'salario_despues_ia',
                 'variacion_porcentual_salarial',
                 'crecimiento_demanda_habilidades%',
                 'factibilidad_trabajo_rem',
                 'nivel_adopcion_ia',
                 'nivel_educativo_req','categoria_riesgo',
                 'presion_reconversion_laboral',
                 'indice_volatilidad_salarial',
                 'urgencia_reentrenamiento',
                 'intensidad_global_disrupcion_ia']
    print("\nColumnas renombradas: \n", df.columns)
    return df

def quitar_duplicados(df):
    print("========QUITAR DUPLICADOS========")
    print("\nFilas completamente duplicadas:\n", df.duplicated().sum())
    df = df.drop_duplicates()
    print("\nFilas completamente duplicadas luego de limpieza:\n", df.duplicated().sum())
    return df

def norma(df, l=True, hc=False): # Siempre recibe un DataFrame
  '''
      De acuerdo a los parámetros que recibe 'norma'
      seleccionamos que devuelve: por defecto, cambia
      a minúculas los encabezados de las columnas,
      los espacios en blanco por guiones bajos y elimina
      espacios al inicio y fin de cada título. Si
      hc = True, cambia también los valores de
      las celdas y "l" debe ser False'''

  # Guardamos la lista de columnas originales antes de cualquier cambio
  columnas_originales = df.columns.tolist()

  if l and hc: # Caso de error: opciones mutuamente excluyentes
    print("Error: 'l' y 'hc' no pueden ser ambos True. Son mutuamente excluyentes.")
    print("Si desea normalizar sólo los títulos, pase el DataFrame como argumento (ej: norma(df))")
    print("Si desea normalizar también las celdas, pase 'l=False' y 'hc=True' (ej: norma(df, l=False, hc=True))")
    return df # Devuelve el df original en caso de error o podría ser tambien una copia

  # Limpiamos valores de celdas si hc es True
  if hc:
    print(f"\nIniciando limpieza de valores de celdas para columnas: \n{columnas_originales}")
    for col in columnas_originales:
        # Verificar si la col es tipo Objeto.(puede ser texto o cualquier u otra cosa)
        if df[col].dtype == 'object':
            # Convierte a string para asegurar que .str métodos funcionen en todos los elementos,
            # (porque comprobamos que a veces los metodos str no funcionaban con tipos Object)
            # luego limpia espacios y convierte a minúsculas.
            # Finalmente, revierte el string 'nan' a np.nan para mantener los valores faltantes.
            df[col] = df[col].astype(str).str.strip().str.lower()
            df[col] = df[col].replace('nan', np.nan)

  # Limpiamos y renombramos los encabezados de columnas si 'l' es True (por defecto) o 'hc' es True
    if l or hc:
      # Crea un mapeo de nombres de columnas originales a los nuevos nombres limpios
      new_columns_map = {col: col.strip().lower().replace(' ', '_') for col in columnas_originales}
      df.rename(columns=new_columns_map, inplace=True)

  return df #Devolvemos el df

def normalizacion_sector(df) :
    """Normalizamos los valores de la columna sector para que no haya inconsistencias de formato"""

    print("========NORMALIZACION SECTOR========")

    # revisamos como estan los valores unicos de la columna sector antes de normalizar
    print("\nAntes de normalizacion:\n", df['sector'].unique(), 'Cantidad:', df['sector'].nunique())
    df = norma(df, False, True) #para que normalice campos tambien
    print("\nDespues de normalizacion:\n", df['sector'].unique(), 'Cantidad:', df['sector'].nunique())

    # Traducimos los 10 sectores sectores
    diccionario = ['finance']
    df['sector'] = df['sector'].replace(diccionario, 'finanzas')

    diccionario = ['technology']
    df['sector'] = df['sector'].replace(diccionario, 'tecnologia')

    diccionario = ['manufacturing']
    df['sector'] = df['sector'].replace(diccionario, 'manufactura')

    diccionario = ['healthcare']
    df['sector'] = df['sector'].replace(diccionario, 'salud')

    diccionario = ['retail']
    df['sector'] = df['sector'].replace(diccionario, 'comercio minorista')

    diccionario = ['education']
    df['sector'] = df['sector'].replace(diccionario, 'educacion')

    diccionario = ['transportation']
    df['sector'] = df['sector'].replace(diccionario, 'transporte')

    diccionario = ['energy']
    df['sector'] = df['sector'].replace(diccionario, 'energia')

    # revisamos como quedaron los valores unicos de la columna sector despues de normalizar
    print("\nDespues de traduccion:\n", df['sector'].unique(), 'Cantidad:', df['sector'].nunique())
    return df

def corregir_anio(df): 
    """Corregimos el formato de la columna año_registro para que sea int para mejorar la consistencia de los datos y evitar errores en el análisis posterior
    """

    print("========CORREGIR AÑO========")
    print(df['año_registro'].unique())
    
    # convertimos la columna a int
    df['año_registro'] = df['año_registro'].astype(int)

    print(df['año_registro'].unique())
    return df

def corregir_formato_salarios(df) :
    """Corregimos el formato de los valores de las columnas de salarios para que sean numéricas y mejorar la consistencia de los datos
    """

    print("========CORREGIR FORMATO SALARIOS========")
    print(df.columns)
    # columna salario_antes_ia
    df['salario_antes_ia'] = (df['salario_antes_ia'].str.replace('$','', regex=False).str.replace(',', '', regex=False))
    # convertimos a valor numerico aquellos valores que pueden ser reconvertidos en numero, y los que no pueden son convertidos a NaN
    df['salario_antes_ia'] = pd.to_numeric(df['salario_antes_ia'])

    #columna salario_despues_ia
    df['salario_despues_ia'] = (df['salario_despues_ia'].str.replace('$', '', regex=False).str.replace(',', '', regex=False))
    # convertimos a valor numerico aquellos valores que pueden ser reconvertidos en numero, y los que no pueden son convertidos a NaN
    df['salario_despues_ia'] = pd.to_numeric(df['salario_despues_ia'])
    return df



def regresion_imputacion_salario_antes_ia(df):

    print("========REGRESION SALARIO ANTES========")

    # columna a imputar "salario_antes_ia"
    v_imputar = 'salario_antes_ia'
    # calculamos la matriz de correlacion para ver que columnas tienen mayor correlacion con la columna a imputar
    matriz_corr = df.corr(numeric_only=True)[v_imputar].sort_values(ascending=False)
    # seleccionamos las columnas con correlacion mayor a 0.5
    cols_relevante =  matriz_corr[abs(matriz_corr) > 0.5]
    print("Columnas con mas de 0.5 de correlacion \n: ", cols_relevante)
    cols_relevante = matriz_corr[matriz_corr > 0.5].index.to_list() #lista de columnas
    # eliminamos la columna a imputar de la lista de columnas relevantes pq no podemos usarla como predictora
    cols_relevante.remove(v_imputar)
    print(cols_relevante)

    # CREAMOS EL MODELO DE REGRESION LINEAL PARA IMPUTAR LOS VALORES NULOS DE LA COLUMNA SALARIO_ANTES_ia
    # entradas a entrenar: aquellas que no tienen nulos en la columna objetivo y que no tienen nulos en las columnas predictoras

    # REGRESION LINEAL SIMPLE ENTRE SALARIO_ANTES_ia Y SALARIO_DESPUES_ia
    train = df[(df['salario_antes_ia'].notna()) & (df['salario_despues_ia'].notna())] #en una fila ninguno sea nulo para entrenar
    pred = df[(df['salario_antes_ia'].isna()) & (df['salario_despues_ia'].notna())] #en una fila sea nulo la variable respuesta y no nulo la predictora

    X = train[['salario_despues_ia']]
    y = train['salario_antes_ia']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=100
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)


    predicciones = modelo.predict(X_test)

    print("R² =", r2_score(y_test, predicciones))

    X_pred = pred[['salario_despues_ia']]

    # completamos los valores nulos de la columna salario_antes_ia con las predicciones del modelo
    df.loc[pred.index,'salario_antes_ia'] = modelo.predict(X_pred) 
    return df

def mediana_imputacion_salario_antes_ia(df) :
    print("========MEDIANA SALARIO ANTES========")
    df['salario_antes_ia'] = df['salario_antes_ia'].fillna( df.groupby('profesion')['salario_antes_ia'].transform('median')) 
    return df

def imputacion_salario_antes_ia(df) :
    print("========IMPUTAR SALARIO ANTES========")
    df = regresion_imputacion_salario_antes_ia(df) #para los que tienen salario despues
    df = mediana_imputacion_salario_antes_ia(df) #para los casos que salario antes y tambien salario despues son nulos
    return df

def regresion_imputacion_salario_despues_ia(df) :
    print("========IMPUTAR SALARIO DESPUES========")

    # calculamos la correlacion de las columnas con la columna a imputar "salario_despues_ia"
    v_imputar = 'salario_despues_ia'
    matriz_corr = df.corr(numeric_only=True)[v_imputar].sort_values(ascending=False)
    cols_relevante =  matriz_corr[abs(matriz_corr) > 0.5]
    print("Columnas con mas de 0.5 de correlacion \n: ", cols_relevante)
    cols_relevante = matriz_corr[matriz_corr > 0.5].index.to_list() #lista de columnas
    cols_relevante.remove(v_imputar)
    print(cols_relevante)

    # AHORA LLENAMOS LOS NULOS DE LA COLUMNA SALARIOS_DESPUES_ia, creando un modelo de regresion lineal con las columnas que tienen mayor correlacion con la columna a imputar

    train = df[ (df[v_imputar].notna())]

    pred = df[(df[v_imputar].isna()) ]

    X = train[['salario_antes_ia']]
    y = train['salario_despues_ia']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    predicciones = modelo.predict(X_test)

    print("R² =", r2_score(y_test, predicciones))

    X_pred = pred[['salario_antes_ia']]

    # predecimos los valores nulos de la columna salario_despues_ia con las predicciones del modelo
    df.loc[pred.index,'salario_despues_ia'] = modelo.predict(X_pred)
    return df

def regresion_riesgo_automatizacion(df) :
    """Imputamos los valores nulos de la columna riesgo_automatizacion_estimado% con un modelo de regresion lineal con las columnas que tienen mayor correlacion con la columna a imputar/objetivo"""

    print("========RIESGO AUTOMATIZACION========")
    v_imputar = 'riesgo_automatizacion_estimado%'
    #print(df.corr(numeric_only=True)['riesgo_automatizacion_estimado%'].sort_values(ascending=False))

    matriz_corr = df.corr(numeric_only=True)[v_imputar].sort_values(ascending=False)
    print("Matris copleto de correlacion: \n" ,matriz_corr)
    cols_relevante =  matriz_corr[abs(matriz_corr) > 0.5]
    print("Columnas con mas de 0.5 de correlacion : \n", cols_relevante)
    cols_relevante = matriz_corr[matriz_corr > 0.5].index.to_list() #lista de columnas
    cols_relevante.remove(v_imputar)
    print(cols_relevante)

    # variable respuesta
    train = df[df[v_imputar].notna()] 

    # Filas a imputar
    pred = df[df[v_imputar].isna()] 

    # Variables predictoras
    X = train[cols_relevante] # df['puntaje_reemplazo_ia', 'urgencia_reentrenamiento', 'presion_reconversion_laboral', 'intensidad_global_disrupcion_ia']

    # Variable objetivo
    y = train[v_imputar] # df[riesgo_automatizacion_estimado%].notna(). Serie

    # Evaluación del modelo
    X_train, X_test, y_train, y_test = train_test_split( # xtrain:
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
    # modelo.fit(X, y)

    # Imputación
    X_pred = pred[cols_relevante]

    df.loc[
        pred.index, #indices de los que son NaN
        v_imputar
    ] = modelo.predict(X_pred) #completa con predicciones
    return df

def imputacion_sector(df) :
    print("========IMPUTAR SECTOR========")
    # AHORA LLENAMOS LOS NULOS DE LA COLUMNA SECTOR
    mascara = df['sector']=='finanzas'
    print('Cantidad de nulos en sector:',df['sector'].isna().sum())
    print('Cantidad de registros FINANZAS:', df['sector'][df['sector']=='finanzas'].value_counts())

    # ??????????
    df['sector'] = df['sector'].fillna(df.groupby('profesion')['sector'].transform(lambda x: x.mode().iloc[0]))


    print('Cantidad de nulos en sector despues imputacion:',df['sector'].isna().sum())
    print('Cantidad de registros FINANZAS despues imputacion:', df['sector'][df['sector']=='finanzas'].value_counts())
    return df





    
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
    imputacion_salario_antes_ia(df)
    regresion_imputacion_salario_despues_ia(df)
    imputacion_sector(df)
