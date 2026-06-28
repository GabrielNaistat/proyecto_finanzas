# de esta manera podemos importar todas las funciones de limpieza desde un solo archivo
from src.load_data import *
from src.limpieza import (
    renombrar_columnas,
    quitar_duplicados,
    normalizacion_sector,
    corregir_anio,
    corregir_formato_salarios,
    regresion_riesgo_automatizacion,
    imputacion_salario_antes_IA,
    regresion_imputacion_salario_despues_IA,
    imputacion_sector
)

# Ejemplo de uso
def procesar_datos(ruta_csv):
    """
    Carga el CSV, aplica limpieza y devuelve el dataframe procesado.
    """
    # 1. Cargar datos
    data = load_data(ruta_csv)
    print(f"✓ Datos cargados: {data.shape}")
    
    # 2. Renombrar columnas
    renombrar_columnas(data)
    print("✓ Columnas renombradas")
    
    # 3. Quitar duplicados
    quitar_duplicados(data)
    print("✓ Duplicados removidos")
    
    # 4. Normalizar sector
    normalizacion_sector(data)
    print("✓ Sector normalizado")

    # 5. Corregir año
    corregir_anio(data)
    print("✓ Año corregido")

    # 6. Corregir formato de salarios
    corregir_formato_salarios(data)
    print("✓ Formato de salarios corregido")

    # 7. Regresión de riesgo de automatización
    regresion_riesgo_automatizacion(data)
    print("✓ Regresión de riesgo de automatización realizada")

    # 8. Imputación de salario antes de IA
    imputacion_salario_antes_IA(data)
    print("✓ Imputación de salario antes de IA realizada")

    # 9. Regresión de imputación de salario después de IA
    regresion_imputacion_salario_despues_IA(data)
    print("✓ Regresión de imputación de salario después de IA realizada")

    # 10. Imputación de sector
    imputacion_sector(data)
    print("✓ Imputación de sector realizada")

    return data # Devolver el dataframe procesado


# Ejemplo: usar en tu código
if __name__ == "__main__":
    # Ruta al CSV raw
    csv_path = "data\\raw\\ai_job_replacement_dirty.csv"
    
    # Procesar datos
    data_cleaned = procesar_datos(str(csv_path))
    
    print(f"\n✓ DataFrame procesado listo: {data_cleaned.shape}")
    print(data_cleaned.isna().sum())  # Mostrar conteo de valores nulos por columna
    
    print("\n¡Procesamiento completo!")