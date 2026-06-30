'''
Se depreca el archivo'''

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
    err_format = True #check_format(df,)
    return dups,vacios,err_format



if __name__ == "__main__":
    import pandas as pd

    print(f"¡Has ejecutado el módulo de auditoria directamente!")
    raw_csv = "data\\raw\\ai_job_replacement_dirty.csv"

    #carga
    df = pd.read_csv(raw_csv)
    vacios = check_vacios(df)
    hay_duplicados, hay_vacios, hay_format_err = auditoria(df)



