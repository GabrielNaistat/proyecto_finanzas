#from columnas import COLUMNAS
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

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

def normalizacion_sector(df, l=True, hc=False): # Siempre recibe un DataFrame :
    print("========NORMALIZACION SECTOR========")
    print(df['sector'].unique())
    #diccionario = ['FINANCE','Finance',' Finance ','finance']
    #df['sector'] = df['sector'].replace(diccionario, 'Finanzas')
    #diccionario = ['Technology','technology','TECHNOLOGY',' Technology ']
    #df['sector'] = df['sector'].replace(diccionario, 'Tecnologia')
    #diccionario = ['manufacturing','Manufacturing',' Manufacturing ','MANUFACTURING']
    #df['sector'] = df['sector'].replace(diccionario, 'Manufactura')
    #diccionario = ['Healthcare','healthcare',' Healthcare ','HEALTHCARE']
    #df['sector'] = df['sector'].replace(diccionario, 'Salud')
    #diccionario = [' Retail ','Retail','RETAIL','retail']
    #df['sector'] = df['sector'].replace(diccionario, 'Comercio y Minorista')
    #diccionario = ['Education','education',' Education ','EDUCATION']
    #df['sector'] = df['sector'].replace(diccionario, 'Educacion')
    #diccionario = ['Transportation','transportation',' Transportation ','TRANSPORTATION']
    #df['sector'] = df['sector'].replace(diccionario, 'Transporte')
    #diccionario = ['Energy','energy',' Energy ','ENERGY']
    #df['sector'] = df['sector'].replace(diccionario, 'Energia')
    
    '''
      De acuerdo a los parámetros que recibe 'normalizacion_sector'
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
    return df # Devuelve el df original en caso de error

  # Paso 1: Limpiar valores de celdas si hc es True
    if hc:
        print(f"Iniciando limpieza de valores de celdas para columnas: {columnas_originales}")
        for nombre_col in columnas_originales:
        # Verificar si la columna es tipi "Object", que suelen indicar que las columnas tienen tipos mezclados mezclados o de tipo string
            if df[nombre_col].dtype == 'object':
            # Convierte a string para asegurar que los métodos .str funcionen en todos los elementos,
            # luego limpia espacios y convierte a minúsculas.
            # Finalmente, revierte el string 'nan' a np.nan para mantener los valores faltantes.
                df[col_name] = df[col_name].astype(str).str.strip().str.lower()
                df[col_name] = df[col_name].replace('nan', np.nan)

  # Paso 2: Limpiar y renombrar encabezados de columnas si 'l' es True (por defecto) o 'hc' es True
        if l or hc:
      # Crea un mapeo de nombres de columnas originales a los nuevos nombres limpios
            mapa_nuevas_columnas = {col: col.strip().lower().replace(' ', '_') for col in columnas_originales}
            df.rename(columns=mapa_nuevas_columnas, inplace=True)
        print(df['sector'].unique())

        return df

# Reasignar el resultado de la función al df para asegurarnos de que queden los cambios


def corregir_anio(df): 
    print("========CORREGIR AÑO========")
    print(df['año_registro'].unique())
    df['año_registro'] = df['año_registro'].astype(int)
    print(df['año_registro'].unique())

def corregir_formato_salarios(df) :
    print("========CORREGIR FORMATO SALARIOS========")
    df['salario_antes_IA'] = (df['salario_antes_IA'].str.replace('$','', regex=False).str.replace(',', '', regex=False))
    df['salario_antes_IA'] = pd.to_numeric(df['salario_antes_IA'])
    df['salario_despues_IA'] = (df['salario_despues_IA'].str.replace('$', '', regex=False).str.replace(',', '', regex=False))
    df['salario_despues_IA'] = pd.to_numeric(df['salario_despues_IA'])

def regresion_imputacion_salario_antes_IA(df) :
    print("========REGRESION SALARIO ANTES========")
    v_imputar = 'salario_antes_IA'
    matriz_corr = df.corr(numeric_only=True)[v_imputar].sort_values(ascending=False)
    cols_relevante =  matriz_corr[matriz_corr > 0.5]
    print("Columnas con mas de 0.5 de correlacion \n: ", cols_relevante)
    cols_relevante = matriz_corr[matriz_corr > 0.5].index.to_list() #lista de columnas
    cols_relevante.remove(v_imputar)
    print(cols_relevante)

    # REGRESION LINEAL SIMPLE ENTRE SALARIO_ANTES_IA Y SALARIO_DESPUES_IA
    train = df[(df['salario_antes_IA'].notna()) & (df['salario_despues_IA'].notna())] #en una fila ninguno sea nulo para entrenar
    pred = df[(df['salario_antes_IA'].isna()) & (df['salario_despues_IA'].notna())] #en una fila sea nulo la variable respuesta y no nulo la predictora

    X = train[['salario_despues_IA']]
    y = train['salario_antes_IA']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=100
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)


    predicciones = modelo.predict(X_test)

    print("R² =", r2_score(y_test, predicciones))

    X_pred = pred[['salario_despues_IA']]

    df.loc[
        pred.index,
        'salario_antes_IA'
    ] = modelo.predict(X_pred)


def mediana_imputacion_salario_antes_IA(df) :
    print("========MEDIANA SALARIO ANTES========")
    df['salario_antes_IA'] = df['salario_antes_IA'].fillna( df.groupby('profesion')['salario_antes_IA'].transform('median'))

def imputacion_salario_antes_IA(df) :
    print("========IMPUTAR SALARIO ANTES========")
    regresion_imputacion_salario_antes_IA(df)
    #para los casos que salario antes y tambien salario despues eran nulos
    mediana_imputacion_salario_antes_IA(df)

def regresion_imputacion_salario_despues_IA(df) :
    print("========IMPUTAR SALARIO DESPUES========")
    v_imputar = 'salario_despues_IA'
    matriz_corr = df.corr(numeric_only=True)[v_imputar].sort_values(ascending=False)
    cols_relevante =  matriz_corr[matriz_corr > 0.5]
    print("Columnas con mas de 0.5 de correlacion \n: ", cols_relevante)
    cols_relevante = matriz_corr[matriz_corr > 0.5].index.to_list() #lista de columnas
    cols_relevante.remove(v_imputar)
    print(cols_relevante)
    # AHORA LLENAMOS LOS NULOS DE LA COLUMNA SALARIOS_DESPUES_IA

    train = df[ (df[v_imputar].notna())]

    pred = df[(df[v_imputar].isna()) ]

    X = train[['salario_antes_IA']]
    y = train['salario_despues_IA']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    predicciones = modelo.predict(X_test)

    print("R² =", r2_score(y_test, predicciones))

    X_pred = pred[['salario_antes_IA']]

    df.loc[
        pred.index,
        'salario_despues_IA'
    ] = modelo.predict(X_pred)

def regresion_riesgo_automatizacion(df) :
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

    df['sector'] = df['sector'].fillna(
        df.groupby('profesion')['sector'].transform(
            lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan
        )
    )
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
