import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# Función para seleccionar un archivo CSV utilizando el diálogo de archivo
def select_csv_file():
    root = Tk()
    root.withdraw()
    csv_path = filedialog.askopenfilename(title="Seleccionar archivo CSV", filetypes=[("Archivos CSV", "*.csv")])
    return csv_path

# Función para leer los datos desde un archivo CSV
def read_csv_data(csv_path):
    try:
        data = pd.read_csv(csv_path)
        return data
    except Exception as e:
        print("Error al cargar el archivo CSV:", e)
        return None

# Generar gráfico de barras para la distribución de género
def generate_gender_bar_chart(data):
    # Filtrar los valores "-" en la columna ESTU_GENERO
    gender_counts = data[data['ESTU_GENERO'] != '-']['ESTU_GENERO'].value_counts()
    # Crear y mostrar el gráfico de barras con los conteos de género
    gender_counts.plot(kind='bar', title='Distribución de Género')
    plt.savefig('genero.png')  # Guardar el gráfico como imagen
    plt.show()  # Mostrar el gráfico

# Generar gráfico de pastel para la educación de los padres
def generate_parent_education_pie_chart(data):
    # Filtrar los valores "-" en la columna FAMI_EDUCACIONPADRE
    education_counts = data[data['FAMI_EDUCACIONPADRE'] != '-']['FAMI_EDUCACIONPADRE'].value_counts()
    # Crear y mostrar el gráfico de pastel con los conteos de educación de los padres
    education_counts.plot(kind='pie', autopct='%1.1f%%', title='Educación de los Padres')
    plt.axis('equal')  # Hacer que el gráfico sea circular
    plt.savefig('educacion_padres.png')  # Guardar el gráfico como imagen
    plt.show()  # Mostrar el gráfico

# Generar gráfico de barras para el promedio de PUNT_GLOBAL por departamento
def generate_department_avg_bar_chart(data):
    # Filtrar los valores "-" en la columna PUNT_GLOBAL
    depto_avg = data[data['PUNT_GLOBAL'] != '-']
    # Convertir los valores de 'PUNT_GLOBAL' a numéricos (ignorando los '-')
    depto_avg['PUNT_GLOBAL'] = pd.to_numeric(depto_avg['PUNT_GLOBAL'], errors='coerce')
    # Calcular el promedio de PUNT_GLOBAL agrupado por departamento y ordenar los valores
    depto_avg = depto_avg.groupby('ESTU_DEPTO_RESIDE')['PUNT_GLOBAL'].mean().sort_values()

    # Identificar los departamentos con el promedio más alto y más bajo
    max_dept = depto_avg.idxmax()
    min_dept = depto_avg.idxmin()

    # Calcular el promedio general de PUNT_GLOBAL
    overall_avg = depto_avg.mean()

    # Colores para resaltar los departamentos con promedio más alto/bajo
    colors = ['green' if dept == max_dept else 'red' if dept == min_dept else 'blue' for dept in depto_avg.index]
    # Crear y mostrar el gráfico de barras con el promedio de PUNT_GLOBAL por departamento
    plt.bar(depto_avg.index, depto_avg.values, color=colors)
    # Agregar línea horizontal para el promedio general
    plt.axhline(y=overall_avg, color='gray', linestyle='--', label=f'Promedio General ({overall_avg:.2f})')
    plt.title('Promedio PUNT_GLOBAL por Departamento de Residencia')
    plt.xlabel('Departamento de Residencia')
    plt.ylabel('Promedio PUNT_GLOBAL')
    plt.xticks(rotation=90)
    plt.legend()  # Mostrar la leyenda
    plt.tight_layout()  # Ajustar el diseño
    plt.savefig('promedio_departamentos.png')  # Guardar el gráfico como imagen
    plt.show()  # Mostrar el gráfico

# Función para guardar datos en un archivo CSV
def save_to_csv(data, filename):
    try:
        data.to_csv(filename, index=True)
        print(f"Datos guardados en {filename}")
    except Exception as e:
        print("Error al guardar los datos en el archivo CSV:", e)

if __name__ == "__main__":
    csv_path = select_csv_file()  # Seleccionar un archivo CSV
    if csv_path:
        students_data = read_csv_data(csv_path)  # Leer datos desde el archivo CSV
        if students_data is not None:
            generate_gender_bar_chart(students_data)  # Generar y mostrar el gráfico de género
            generate_parent_education_pie_chart(students_data)  # Generar y mostrar el gráfico de educación de padres
            generate_department_avg_bar_chart(students_data)  # Generar y mostrar el gráfico de promedio por departamento

            # Guardar conteos y promedios en archivos CSV
            save_to_csv(students_data[students_data['ESTU_GENERO'] != '-']['ESTU_GENERO'].value_counts(), 'genero_counts.csv')
            save_to_csv(students_data[students_data['FAMI_EDUCACIONPADRE'] != '-']['FAMI_EDUCACIONPADRE'].value_counts(), 'educacion_padres_counts.csv')
            save_to_csv(students_data[students_data['PUNT_GLOBAL'] != '-'].groupby('ESTU_DEPTO_RESIDE')['PUNT_GLOBAL'].mean(), 'promedio_departamentos.csv')


#Gráfica 1 de Distribución de Género:

#Esta gráfica muestra la proporción de estudiantes por género utilizando barras para representar las categorías 
#femenino y masculino. Los valores que no están disponibles se excluyen para una representación precisa de la 
#distribución de género en el conjunto de datos.


#Gráfica 2 de Educación de los Padres:

#Esta gráfica utiliza un gráfico de pastel para mostrar la composición de los niveles educativos de los padres de 
#los estudiantes. Los valores faltantes se omiten para presentar claramente las proporciones relativas de diferentes 
#niveles educativos.


#Gráfica 3 de Promedio PUNT_GLOBAL por Departamento:

#Esta gráfica de barras presenta los promedios de los puntajes globales de los estudiantes en cada departamento. 
#Incluye una línea horizontal que muestra el promedio general. Los departamentos se ordenan y se utilizan colores 
#para resaltar aquellos con los promedios más altos y más bajos.