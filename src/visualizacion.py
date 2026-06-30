import matplotlib.pyplot as plt
from src.eda import agrupar_promedio

 #EN EL MAIN COLOCAS grafico_funcion_A(df,'anio_registro','salario_antes_ia','salario_despues_ia')
def grafico_funcion_A(df, nombre_grupo, nombre1, nombre2):
    print("========== GRAFICO FUNCION A =========")
    salario_antes_promedio = agrupar_promedio(df, nombre_grupo, nombre1)
    salario_despues_promedio = agrupar_promedio(df, nombre_grupo, nombre2)

    plt.plot( salario_antes_promedio.index, salario_antes_promedio.values, marker='o', color='green', label=nombre1)
    plt.plot( salario_despues_promedio.index, salario_despues_promedio.values, marker='o', color='red', label=nombre2)

    plt.title('Evolución del salario promedio en Finanzas')
    plt.xlabel('Año')
    plt.ylabel('Salario promedio')
    plt.grid(True)
    plt.legend()
    plt.show()


#EN EL MAIN COLOCAS grafico_funcion_torta(df,'categoria_riesgo')
def grafico_funcion_torta(df,nombre):
    print('========== GRAFICO FUNCION TORTA =========')
    categorias = df[nombre].value_counts()
    plt.pie(categorias.values,labels = categorias.index,autopct='%1.2f%%' )
    #plt.show()

#EN EL MAIN COLOCAS grafico_barras(df,'pais','nivel_adopcion_ia')
def grafico_barras(df,nombre_grupo,nombre):
    print('========== GRAFICO FUNCION BARRAS =========')
    adopcion  = agrupar_promedio(df, nombre_grupo, nombre).sort_values(ascending=False)
    plt.figure(figsize=(12,6))

    plt.bar(adopcion.index, adopcion.values)
    plt.ylim(bottom = 40)

    plt.title("Nivel promedio de adopción de ia por país (Finanzas)")
    plt.xlabel("País")
    plt.ylabel("Nivel de adopción de ia")

    plt.xticks(rotation=45)
    plt.grid(axis="y")

    #plt.show()