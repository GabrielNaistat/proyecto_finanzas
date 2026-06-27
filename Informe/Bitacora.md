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





#                                        Fase 2

### Análisis Estadístico y Exploratorio (EDA) - Decisiones y Hallazgos

En esta fase, se realizaron análisis clave para comprender mejor la dinámica del sector financiero frente a la IA. Las decisiones metodológicas y los resultados obtenidos para cada punto fueron los siguientes:


#### 1. Volatilidad de Ingresos: Rango y Varianza de Salarios

**Decisiones:**

*   **Método:** Para evaluar la volatilidad de los ingresos, se calcularon el **rango** (diferencia entre el salario máximo y mínimo) y la **varianza** de las columnas `salary_before_usd` y `salary_after_usd`.
*   **Justificación:** Estas métricas son indicadores fundamentales de la dispersión de los datos. Un rango grande indica una amplia diversidad salarial, mientras que una varianza alta sugiere una mayor inestabilidad o desigualdad en los salarios, lo que nos permite inferir sobre la estabilidad del sector.

**Hallazgos e Interpretación:**

*   **Resultados:**
    *   Salarios Antes de la IA: Rango: ~$119,892.81, Varianza: ~1,089,732,623.05
    *   Salarios Después de la IA: Rango: ~$887,859.39, Varianza: ~1,636,209,154.45

*   **Conclusión:** La varianza de los salarios DESPUÉS de la IA es **MAYOR** que ANTES de la IA. Esto sugiere que la introducción de la IA ha **aumentado la dispersión o inestabilidad de los salarios** en el sector financiero. Un rango y una varianza mayores indican una mayor volatilidad de los ingresos, lo que podría implicar que los salarios se distribuyen en un espectro más amplio, o que hay más incertidumbre en torno a los ingresos en el sector. Esto puede ser resultado de la creación de roles muy bien pagados y la disminución de salarios en roles menos demandados.

---

#### 2. Brecha de Habilidades: Promedio de `skill_gap_index` por País

**Decisiones:**

*   **Método:** Se calculó el **promedio del `skill_gap_index` agrupado por `country`** y se imprime el resultados pais con mayor brecha más crítica.
*   **Justificación:** El `skill_gap_index` es una métrica directa que cuantifica la diferencia entre las habilidades existentes y las demandadas. Agrupar por país nos permite una comparativa geográfica y la identificación de regiones que necesitan mayor atención en capacitación.

**Hallazgos e Interpretación:**

*   **Resultados (ejemplo de los primeros países):**
    *   India: 53.57
    *   Brazil: 50.67
    *   Singapore: 49.96
    *   Japón: 49.41

*   **Conclusión:** Los países con un valor más alto en el `skill_gap_index` promedio (como India y Brasil) son aquellos donde el **desfase formativo es más crítico**. Esto significa que la discrepancia entre las habilidades que tienen los trabajadores y las habilidades que demanda el mercado laboral (especialmente por la integración de la IA) es mayor en esas regiones. Un `skill_gap_index` alto podría indicar la necesidad de programas de capacitación y reentrenamiento urgentes en esos países.

---

#### 3. Detección de Outliers en Salarios

**Decisiones:**

*   **Método:** Para identificar outliers, se utilizó el método del **rango intercuartílico (IQR)** para las columnas `salary_before_usd` y `salary_after_usd`. Se calcularon el primer cuartil (Q1), el tercer cuartil (Q3) y el IQR (Q3 - Q1). Los valores por debajo de `Q1 - (1.5 * IQR)` o por encima de `Q3 + (1.5 * IQR)` se consideraron outliers.
*   **Justificación:** El método IQR es robusto frente a distribuciones asimétricas y la presencia de valores extremos, lo que lo hace adecuado para detectar salarios que se desvían significativamente de la mayoría de los datos, sin ser excesivamente influenciado por ellos.

**Hallazgos e Interpretación:**

*   **Resultados:**
    *   `salary_before_usd`: 0 outliers altos, 0 outliers bajos.
    *   `salary_after_usd`: 2 outliers altos, 0 outliers bajos.

*   **Conclusión:** Se encontraron **2 outliers altos en la columna `salary_after_usd`**, lo que sugiere la existencia de salarios excepcionalmente altos después de la IA en el sector financiero. No se detectaron outliers bajos ni en `salary_before_usd` ni en `salary_after_usd`.








##                                        Fase 3

### Visualización y Comunicación - Justificaciones y Hallazgos Clave

En esta fase, se generaron y analizaron diversos gráficos para visualizar patrones y tendencias clave en el sector financiero bajo el impacto de la IA. A continuación, se detallan las justificaciones técnicas y las interpretaciones de cada visualización:

---

#### 1. Gráfico de Evolución: Tendencia Anual del Salario Promedio en Finanzas (2020-2026)

**Justificación Técnica:**
*   **Tipo de Gráfico:** Se empleó un gráfico de líneas (`sns.lineplot`/`plt.plot`) con marcadores. Este tipo de visualización es ideal para mostrar **tendencias a lo largo del tiempo** (series temporales), ya que conecta los puntos de datos consecutivos para ilustrar claramente la dirección y magnitud de los cambios.
*   **Métricas Representadas:** Se graficó el salario promedio (`salary_before_usd` y `salary_after_usd`) contra el año (`year`). La inclusión de ambas líneas permite una **comparación directa del impacto de la IA** en la evolución salarial.
*   **Agrupación:** La agrupación por año (`df_Finance.groupby('year')`) y el cálculo del promedio asegura que se represente la tendencia central anual.

**Interpretación:**
*   El gráfico ilustra la evolución del salario promedio en el sector financiero, diferenciando entre el salario antes y después de la influencia de la IA. Se observa que el salario 'Después de la IA' supera al 'Antes de la IA' en los primeros años (2020-2022), lo que podría sugerir un **premio salarial inicial** para roles que adoptan o trabajan con la IA.
*   Sin embargo, a partir de 2022, la tendencia del salario 'Después de la IA' muestra una ligera disminución, mientras que el salario 'Antes de la IA' también desciende, aunque con un patrón más variable. Esto podría indicar una **estabilización o incluso una leve contracción** de los salarios después del auge inicial, o que la IA devalúa el trabajo humano en ciertos roles a medida que madura su implementación.
*   La **brecha entre ambas líneas** (salario antes vs. después de la IA) es un indicador crucial del impacto directo de la automatización y la inteligencia artificial en la compensación de los roles financieros, mostrando cómo la IA reconfigura la valoración económica de las habilidades.

---

#### 2. Gráfico de Distribución: Roles por Categoría de Riesgo de Automatización

**Justificación Técnica:**
*   **Tipo de Gráfico:** Se utilizó un gráfico de pastel (`plt.pie`). Este tipo es efectivo para visualizar la **distribución proporcional** de categorías dentro de un todo, es decir, cómo cada parte contribuye al 100%.
*   **Métrica Representada:** Se graficó la frecuencia relativa de `automation_risk_category` (Bajo, Medio, Alto). `value_counts()` es la función adecuada para obtener estas frecuencias.
*   **Etiquetado:** El parametro`autopct='%1.1f%%'` muestra los porcentajes dentro del gráfico, facilitando la comprension de las proporciones.

**Interpretación:**
*   El gráfico de pastel revela la **exposición relativa del sector financiero a la automatización**. Se observa que la mayoría de los roles se encuentran en la categoría de riesgo 'Medio' (41.3%), seguido de 'Alto' (31.0%) y 'Bajo' (27.6%).
*   La significativa proporción de roles en riesgo 'Medio' y 'Alto' sugiere que una **parte considerable de los empleos actuales en finanzas podría ser impactada o potencialmente reemplazada por la IA**.
*   Este hallazgo subraya la **urgencia de programas de reentrenamiento y adaptación de habilidades** para la fuerza laboral del sector, a fin de hacer menos severos los efectos del impacto negativo de la automatización en el empleo.

---

#### 3. Gráfico de Barras: Nivel Promedio de Adopción de IA por País en el Sector Financiero

**Justificación Técnica:**
*   **Tipo de Gráfico:** Se seleccionó un gráfico de barras (`sns.barplot`/`plt.pie`). Este es adecuado para **comparar magnitudes entre diferentes categorías discretas** (en este caso, países).
*   **Métrica Representada:** Se visualizó el promedio de `ai_adoption_level` por `country`. La agrupación y ordenación (`sort_values(ascending=False)`) permite identificar rápidamente a los países líderes y rezagados en adopción de IA.


**Interpretación:**
*   El gráfico de barras muestra una **comparativa clara del nivel promedio de adopción de la Inteligencia Artificial** en el sector financiero entre los distintos países. India, USA y Alemania se posicionan como líderes con los niveles más altos de adopción de IA, mientras que Singapur y el Reino Unido se encuentran en los niveles más bajos de este grupo.
*   Las diferencias observadas pueden reflejar diversos factores como **políticas gubernamentales de innovación, inversión en tecnología, infraestructura digital, o la demanda específica de eficiencia** en sus mercados financieros.
*   Estos datos son cruciales para entender **dónde se están implementando las tecnologías de IA más rápidamente** y, por extensión, dónde podrían surgir primero las oportunidades o desafíos relacionados con la IA en el empleo financiero.





### Conclusiones de la Fase IV: Reflexión Crítica (Anti-LLM)

Las siguientes conclusiones se derivan estrictamente de los hallazgos obtenidos a través del procesamiento y análisis de los datos:


---

1.  **¿Existe evidencia de que la IA esté "empobreciendo" los roles tradicionales de finanzas?**

    *   **Conclusión basada en datos:** Los datos presentan una imagen compleja. Si bien inicialmente (2020-2022) se observó un 'premio salarial' para los roles 'Después de la IA', las tendencias salariales (tanto 'Antes' como 'Después' de la IA) muestran una **disminución después de 2022**. Más significativamente, la **mayor varianza en los salarios 'Después de la IA'** indica una mayor dispersión e inestabilidad en la compensación. Esta creciente volatilidad y las tendencias decrecientes en el salario promedio sugieren que, aunque no todos los roles están siendo directamente 'empobrecidos', la IA está generando una **mayor incertidumbre salarial y una posible devaluación para ciertos segmentos o roles tradicionales** que no se adaptan, aumentando la brecha entre los mejor y peor pagados dentro del sector.

---

2.  **Según sus datos, ¿la factibilidad de trabajo remoto protege o expone más al trabajador financiero frente al reemplazo por IA?**

    *   **Conclusión basada en datos:** Basado en el análisis de correlación, se encontró una **correlación débil o nula (-0.01)** entre la `remote_feasibility_score` (factibilidad de trabajo remoto) y la `ai_replacement_score` (puntuación de reemplazo por IA). Esto sugiere que, según los datos disponibles en este conjunto, **la factibilidad de trabajar de forma remota no protege ni expone significativamente más al trabajador financiero frente al riesgo de ser reemplazado por la IA**. No hay una relación lineal directa observada que permita inferir un efecto protector o de exposición en este contexto.