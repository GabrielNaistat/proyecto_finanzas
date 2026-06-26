import pandas as pd
import numpy as np

def outliers(df) :
    print("========INICIO LIMPIAR OUTLIERS========")
    variables = ['salario_antes_IA','salario_despues_IA']
    
    for var in variables:   
        print(var, "menor a cero: ", df[df[var] < 0])
        if df[var].min() < 0 : 
            df = df[df[var] > 0]



def volatilidad_ingresos(df) :
    print("========INICIO VOLATILIDAD INGRESOS========")
    variables = ['salario_antes_IA','salario_despues_IA']
    for var in variables:
        maximo = df[var].max()
        minimo =  df[var].min()
        rango = maximo - minimo
        varianza = df[var].var()
        # desvio = df[var].std()
        # q1 = df[var].quantile(0.25)
        # q3 = df[var].quantile(0.75)
        # iqr = q3 - q1

        print(f"\n>>> Variable: {var}")
        print(f"    Maximo           : {maximo:.2f}")
        print(f"    Minimo           : {minimo:.2f}")
        print(f"    Promedio         : {df[var].mean():.2f}")
        print(f"    Rango            : {rango:.2f}")
        print(f"    Varianza         : {varianza:.4f}")

def agrupar_promedio(df,nombre_grupo,nombre_grupo_promedio):
    agrupado = ( df.groupby(nombre_grupo)[nombre_grupo_promedio].mean())
    print(agrupado)
    return  agrupado


def agrupar_promedio_max(df,nombre_grupo,nombre_grupo_promedio):
    promedio_pais=agrupar_promedio(df,nombre_grupo,nombre_grupo_promedio)

    pais_critico = promedio_pais.idxmax()
    valor = promedio_pais.max()
    print(f"País con mayor brecha: {pais_critico}")
    print(f"Promedio: {valor:.2f}")

###########################################################
if __name__ == "__main__":
    print(f"¡Has ejecutado el módulo de EDA directamente!")
    raw_csv = "data\\raw\\ai_job_replacement_dirty.csv"

    #carga
    df = pd.read_csv(raw_csv)






