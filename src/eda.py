import pandas as pd
import numpy as np

"""
modulo de EDA (Exploratory Data Analysis) para analizar los datos y obtener información relevante sobre la distribución de los datos, la volatilidad de los ingresos y la brecha de habilidades por país.
"""

# detecta y elimina los outliers de las variables salario_antes_ia y salario_despues_ia, mostrando los registros que tienen valores menores a cero
def outliers(df) :
    print("========INICIO LIMPIAR OUTLIERS========")
    variables = ['salario_antes_ia','salario_despues_ia']

    for var in variables:   
        if df[var].min() < 0 : 
            df[var] = abs(df[var])

        Q1 = df[var].quantile(0.25)
        Q3 = df[var].quantile(0.75)
        IQR = Q3 - Q1
        
        print(f"\n    Variable: {var}")
        print(f"    Q1         : {Q1:.2f}")
        print(f"    Q3            : {Q3:.2f}")
        print(f"    IQR         : {IQR:.4f}")

        lim_inf = Q1 - 1.5 * IQR
        lim_sup = Q3 + 1.5 * IQR
        outliers = df[(df[var] < lim_inf) | (df[var] > lim_sup)]
        print(f"\{var}: límites [{lim_inf:.2f}, {lim_sup:.2f}]. Outliers encontrados: {len(outliers)}")

        df = df[(df[var] > lim_inf) & (df[var] < lim_sup)]

    return df


# calcula la volatilidad de los ingresos antes y despues de la ia, mostrando el maximo, minimo, promedio, rango, varianza y desviacion estandar de las variables salario_antes_ia y salario_despues_ia
# para responder la pregunta: ¿Qué nos dice esto sobre la estabilidad del sector?
def volatilidad_ingresos(df):
    """Calcula la volatilidad de los ingresos antes y despues de la ia, mostrando el maximo, minimo, promedio, rango, varianza y desviacion estandar de las variables salario_antes_ia y salario_despues_ia"""
    print("========INICIO VOLATILIDAD INGRESOS========")
    variables = ['salario_antes_ia','salario_despues_ia']
    for var in variables:
        maximo = df[var].max()
        minimo =  df[var].min()
        rango = maximo - minimo
        varianza = df[var].var()
        desv_estandar = df[var].std()


        print(f"\n>>> Variable: {var}")
        print(f"    Maximo           : {maximo:.2f}")
        print(f"    Minimo           : {minimo:.2f}")
        print(f"    Promedio         : {df[var].mean():.2f}")
        print(f"    Rango            : {rango:.2f}")
        print(f"    Varianza         : {varianza:.4f}")
        print(f"    Desv. Estándar   : {desv_estandar:.2f}")




def agrupar_promedio(df,nombre_grupo,nombre_grupo_promedio):
    """Agrupa los datos por una columna y calcula el promedio de otra columna"""
    agrupado = ( df.groupby(nombre_grupo)[nombre_grupo_promedio].mean())
    print(agrupado)
    return  agrupado


# encuentra el país con mayor brecha de habilidades y su promedio, para responder la pregunta: ¿Qué país tiene la mayor brecha de habilidades y cuál es su promedio?
def agrupar_promedio_max(df,nombre_grupo,nombre_grupo_promedio):
    """
    imprime el país con mayor brecha de habilidades y su promedio, 
    """
    promedio_pais=agrupar_promedio(df,nombre_grupo,nombre_grupo_promedio)

    pais_critico = promedio_pais.idxmax()
    valor = promedio_pais.max()
    print(f"País con mayor brecha: {pais_critico}")
    print(f"Promedio: {valor:.2f}")

###########################################################

# 
if __name__ == "__main__":
    print(f"¡Has ejecutado el módulo de EDA directamente!")
    raw_csv = "data\\raw\\ai_job_replacement_dirty.csv"

    #carga
    df = pd.read_csv(raw_csv)






