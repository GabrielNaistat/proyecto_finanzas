#                  Bitacora de Auditoria de Datos

##  Impacto de la Inteligencia Artificial en el Empleo (2020-2026)
##  Sector Analizado: Finanzas (Finance)

# INDICE

Fase 1: Diagnóstico y Saneamiento


fase 2 : 



#                                        Fase 1 

 Reporte inicial de como se encontraron los datos del archivo original, y como se trataron esos mismos datos

### Inconsistencias identificadas en el DataFrame `ai_job_replacement_dirty (1).csv` (DataFrame original)

Durante el proceso de auditoría y preparación de los datos, se detectaron las siguientes inconsistencias en el DataFrame original:

1.  **Duplicados en `job_id`**: Se encontraron registros duplicados basados en la columna `job_id`. Estos duplicados fueron eliminados para asegurar que cada `job_id` fuera único, evitando sesgos en los análisis.

2.  **Valores nulos significativos**: Las columnas `industry`, `automation_risk_percent`, `salary_before_usd`, y `salary_after_usd` presentaban una cantidad considerable de valores nulos. Estos valores fueron gestionados posteriormente mediante imputación.

3.  **Tipos de datos incorrectos**: 
    *   La columna `year` fue importada como tipo `float64` y posteriormente convertida a `int` para una representación más precisa del año.
    *   Las columnas `salary_before_usd` y `salary_after_usd` fueron inicialmente cargadas como tipo `object` (cadena de texto) debido a la presencia de caracteres especiales como `$` y `,`. Esto impidió realizar cálculos numéricos directos. Se requirió un proceso de limpieza para eliminar estos caracteres y convertirlas a tipo `float`.

4.  **Inconsistencias en el formato de texto**: La columna `industry` mostraba variaciones en la capitalización y la presencia de espacios extra (ej. 'FINANCE', 'Finance', ' Manufacturing ', 'finance'). Esto requirió una estandarización para agrupar correctamente las industrias.

5.  **Valores atípicos y no válidos**: Se identificaron valores no válidos (ej. `-99999`) y valores negativos en la columna `salary_before_usd`, que fueron tratados como `NaN` (Not a Number) para su posterior imputación, ya que no representaban salarios lógicamente posibles.




### Justificaciones Técnicas para la Imputación de Datos Nulos 

Se detalla a continuación los métodos de imputación utilizados para las columnas con valores nulos, según la estrategia aplicada, con las correspondientes justificaciones técnicas:

1.  **Columna `industry`:**
    *   **Método:** Se utilizó la **moda** (el valor más frecuente) para imputar los valores nulos en esta columna.
    *   **Justificación Técnica:** La moda es el método de imputación más apropiado para variables categóricas nominales, como `industry`, donde los valores no tienen un orden inherente. Al asignar el valor más frecuente, se preserva la distribución original de la categoría dominante en la columna, lo que es crucial para no introducir sesgos artificiales en el análisis de las proporciones de industrias. Es un enfoque simple pero efectivo para mantener la integridad de los datos categóricos.


2.  **Columnas `salary_before_usd`, `salary_after_usd` y `automation_risk_percent`:**
    *   **Preprocesamiento:** Antes de la imputación, estas columnas numéricas pasaron por un riguroso proceso de limpieza. Esto incluyó la eliminación de caracteres no numéricos (como `$` y `,`) y la conversión a tipo numérico (`float`) utilizando `pd.to_numeric` con `errors='coerce'`, lo que convirtió cualquier valor no convertible a `NaN`. Para las columnas de salarios, también se gestionaron valores atípicos negativos, convirtiéndolos a `NaN` para asegurar la coherencia de los datos.
    *   **Método de Imputación:** Para estas columnas, se implementó un enfoque avanzado de **imputación por regresión lineal**. La metodología seguida fue:
        1.  **Identificación de Variables Correlacionadas:** Se buscaron las variables en el DataFrame que presentaban la mayor correlación con la columna a imputar (la 'variable objetivo'). Esto se hizo para asegurar que el modelo de regresión tuviera predictores relevantes y predictivos.
        2.  **Entrenamiento del Modelo de Regresión:** Se entrenó un modelo de regresión lineal utilizando únicamente las filas donde la variable objetivo *no* tenía valores nulos. Las variables altamente correlacionadas sirvieron como características de entrada para el modelo.
        3.  **Predicción de Valores Nulos:** Finalmente, el modelo de regresión lineal entrenado se utilizó para predecir los valores de las celdas nulas en la variable objetivo, basándose en los valores de sus respectivas variables predictoras para esas filas.
    *   **Justificación Técnica:** La imputación por regresión lineal es un método superior a la imputación por media o mediana cuando existen relaciones lineales significativas entre la variable a imputar y otras variables en el dataset. A diferencia de los métodos de imputación simples, la regresión lineal utiliza la información disponible en las otras columnas para hacer una estimación más informada y contextualmente relevante del valor faltante. Esto tiene varias ventajas:
        *   **Mayor Precisión:** Las predicciones suelen ser más cercanas a los valores reales que si se usara solo la media o mediana, ya que considera la estructura de las relaciones de los datos.
        *   **Preservación de la Varianza y Covarianza:** Ayuda a mantener la variabilidad natural y las relaciones de covarianza entre las variables, lo cual es fundamental para análisis estadísticos y modelado posteriores. Imputar con la media o mediana tiende a reducir artificialmente la varianza y puede distorsionar las correlaciones.
        *   **Reducción de Sesgos:** Al considerar las interacciones entre variables, este método minimiza el sesgo que podría introducirse al asumir que los valores faltantes son simplemente el promedio o el valor central de la distribución.



Estado Actual del Dataset luego de las tareas realizadas:

- Se eliminaron registros duplicados.
- Se corrigieron errores de formato.
- Se normalizaron categorías.
- Se corrigieron tipos de datos.
- Se transformaron inconsistencias lógicas en valores faltantes.
- Se imputaron valores nulos en variables salariales.

El dataset resultante presenta una estructura más consistente y adecuada para las fases posteriores de analisis estadistico exploratorio (EDA) y visualizacion
