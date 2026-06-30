'''
decretado'''

import pandas as pd

def check_duplicados(df):
    '''
    Chequeamos si hace falta quitar duplicados
    '''
    print("========CHEQUEO DE DUPLICADOS========")
    print("Filas completamente duplicadas:", df.duplicated().sum())
    ret = True if df.duplicated().sum() > 0 else False
    return ret

def check_vacios(df) :
    df_c = df.copy()
    # for line in df_c.isna().sum():
    #     if line > 0 :
    #         print(line)
    #print(df_c.isna().sum())
    print("suma sin drop", df_c.shape[0])
    print("suma dropna", df_c.dropna().shape[0])
    
    if df_c.shape[0] !=  df_c.dropna().shape[0] : 
        ret = True 
    else: 
        ret = False
    return ret

def describe_all(df):
    cols = df.columns.to_list()
    for columna in cols :
        print(df[columna].describe())


def auditoria(df) :
    print("========INICIO AUDITORIA========")
    copia = df.copy()
    dups = check_duplicados(copia)
    vacios = check_vacios(copia)
    # err_format = True #check_format(df,)
    return dups,vacios

def auditoria_completa(df_original) :

    """
    Auditoria completa del dataframe original, para detectar duplicados, vacios y errores de formato
    """
    print("========INICIO AUDITORIA COMPLETA========")
    
    df = df_original.copy()
    # limpiar espacios en nombres de columna
    df.columns = df.columns.str.strip()

    # se detectan duplicados en job_id
    print("Cantidad de duplicados en job_id:")
    print((df["job_id"].duplicated()).sum())

    # valores nulos en distintas columnas
    print("dataframe cantidad de nulos por columna:")
    print(df.isnull().sum())

    # tipos de datos incorrectos en distintas columnas "salario_antes_IA" y "salario_despues_IA" deben ser float, "year" debe ser int, "country" y "industry" deben ser string
    print(f"dataframe info:")
    print(df.info())

    # salarios negativos en "salario_antes_IA" y "salario_despues_IA" deben ser positivos
    print("Cantidad de valores negativos en salary_before_usd y salary_after_usd:")

    # convertimos a numerico para poder detectar negativos
    salary_before = pd.to_numeric(df["salary_before_usd"], errors='coerce')
    salary_after = pd.to_numeric(df["salary_after_usd"], errors='coerce')

    df_negativos = df[(salary_before< 0) | (salary_after < 0)]
    print(df_negativos)

    # se detectaron caracteres especiales en "salario_antes_IA" y "salario_despues_IA" que deben ser eliminados
    print("Existen valores con caracteres especiales en salary_before_usd y salary_after_usd:")
    print(df.sample(20))
    
    print("")
    print("========FIN AUDITORIA========")
    
    



if __name__ == "__main__":
    import pandas as pd

    print(f"¡Has ejecutado el módulo de auditoria directamente!")
    raw_csv = "data\\raw\\ai_job_replacement_dirty.csv"

    #carga
    df = pd.read_csv(raw_csv)

    # funcion que audita el dataframe y devuelve un resumen de duplicados, vacios y errores de formato
    # auditoria_completa(df)



    # vacios = check_vacios(df)
    # hay_duplicados, hay_vacios, hay_format_err = auditoria(df)



