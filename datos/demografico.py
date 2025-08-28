# 1. Importar la librería pandas y darle un alias más corto ('pd')
import pandas as pd

print("🐍 Script iniciado...")

# 2. Definir el nombre de tu archivo Excel.
#    Usamos '../' para indicarle que suba a la carpeta anterior a buscar el archivo.
nombre_archivo = '../JEFAB_2024_corregido.xlsx'

# 3. Usar pandas para leer el archivo Excel y cargarlo en una variable.
#    A esta variable (que es como una tabla) comúnmente la llamamos 'df' (DataFrame).
try:
    df = pd.read_excel(nombre_archivo)
    
    # 4. ¡Verificación! Imprimir las primeras 5 filas para confirmar que se leyó correctamente.
    print("\n✅ ¡El archivo se cargó con éxito! Aquí están las primeras 5 filas:")
    print(df.head())

    # 5. (Opcional) Mostrar un resumen de la tabla (tipos de datos y valores no nulos).
    print("\nℹ️  Información general del DataFrame:")
    df.info()

except FileNotFoundError:
    print(f"\n❌ ERROR: No se pudo encontrar el archivo '{nombre_archivo}'.")
    print("Asegúrate de que el archivo esté en la misma carpeta que tu script y que el nombre sea exacto.")

# A partir de aquí, puedes empezar a hacer tu análisis con la variable 'df'.

# --- COMIENZA TU ANÁLISIS AQUÍ ---

# Ver las dimensiones de la tabla (filas, columnas)
print("\nDimensiones de la tabla (filas, columnas):")
print(df.shape)

# Obtener estadísticas descriptivas básicas para las columnas numéricas
# (conteo, media, desviación estándar, mínimo, máximo, etc.)
print("\nEstadísticas descriptivas de las columnas numéricas:")
print(df.describe())

# Revisar si hay valores nulos (vacíos) y cuántos hay por columna
# Esto es CRÍTICO para la limpieza de datos.
print("\nConteo de valores nulos por columna:")
print(df.isnull().sum())

# --- PASO 1: IMPORTAR LIBRERÍAS ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("--- Iniciando Generación de Gráficos Demográficos ---")

# --- PASO 2: CARGA Y PREPARACIÓN DE DATOS ---
sns.set_theme(style="whitegrid")

try:
    # Cargar el archivo CSV desde la carpeta principal (un nivel arriba).
    print(f"✅ Datos cargados exitosamente.")

    # --- PASO 3: GRÁFICOS DE VARIABLES INDIVIDUALES (UNIVARIADOS) ---
    
    # Gráfico 1: Distribución de Edad (Histograma)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['EDAD2'], bins=20, kde=True, color='dodgerblue')
    plt.title('Distribución de la Edad del Personal', fontsize=16, fontweight='bold')
    plt.xlabel('Edad (años)', fontsize=12)
    plt.ylabel('Frecuencia', fontsize=12)
    plt.savefig('grafico_distribucion_edad.png')
    print("💾 Gráfico 'grafico_distribucion_edad.png' guardado.")

    # Gráfico 2: Distribución de Género (Barras)
    plt.figure(figsize=(8, 6))
    sns.countplot(x='SEXO', data=df, palette='viridis', order=df['SEXO'].value_counts().index)
    plt.title('Distribución por Género', fontsize=16, fontweight='bold')
    plt.xlabel('Género', fontsize=12)
    plt.ylabel('Cantidad', fontsize=12)
    plt.savefig('grafico_distribucion_genero.png')
    print("💾 Gráfico 'grafico_distribucion_genero.png' guardado.")

    # Gráfico 3: Distribución de Categoría (Barras Horizontales)
    plt.figure(figsize=(12, 7))
    sns.countplot(y='CATEGORIA', data=df, palette='plasma', order=df['CATEGORIA'].value_counts().index)
    plt.title('Distribución por Categoría Militar', fontsize=16, fontweight='bold')
    plt.xlabel('Cantidad', fontsize=12)
    plt.ylabel('Categoría', fontsize=12)
    plt.savefig('grafico_distribucion_categoria.png')
    print("💾 Gráfico 'grafico_distribucion_categoria.png' guardado.")

    # Gráfico 4: Distribución de Grado (Barras Horizontales)
    plt.figure(figsize=(12, 10))
    sns.countplot(y='GRADO', data=df, palette='magma', order=df['GRADO'].value_counts().index)
    plt.title('Distribución por Grado Específico', fontsize=16, fontweight='bold')
    plt.xlabel('Cantidad', fontsize=12)
    plt.ylabel('Grado', fontsize=12)
    plt.tight_layout()
    plt.savefig('grafico_distribucion_grado.png')
    print("💾 Gráfico 'grafico_distribucion_grado.png' guardado.")

    # Gráfico 5: Distribución de Estado Civil (Barras Horizontales)
    plt.figure(figsize=(12, 7))
    sns.countplot(y='ESTADO_CIVIL', data=df, palette='cividis', order=df['ESTADO_CIVIL'].value_counts().index)
    plt.title('Distribución por Estado Civil', fontsize=16, fontweight='bold')
    plt.xlabel('Cantidad', fontsize=12)
    plt.ylabel('Estado Civil', fontsize=12)
    plt.savefig('grafico_distribucion_estado_civil.png')
    print("💾 Gráfico 'grafico_distribucion_estado_civil.png' guardado.")

    # Gráfico 6: Distribución de Nivel Educativo (Barras Horizontales)
    plt.figure(figsize=(12, 8))
    sns.countplot(y='NIVEL_EDUCATIVO', data=df, palette='inferno', order=df['NIVEL_EDUCATIVO'].value_counts().index)
    plt.title('Distribución por Nivel Educativo', fontsize=16, fontweight='bold')
    plt.xlabel('Cantidad', fontsize=12)
    plt.ylabel('Nivel Educativo', fontsize=12)
    plt.tight_layout()
    plt.savefig('grafico_distribucion_nivel_educativo.png')
    print("💾 Gráfico 'grafico_distribucion_nivel_educativo.png' guardado.")

    # --- PASO 4: GRÁFICOS DE VARIABLES CRUZADAS (BIVARIADOS) ---

    # Gráfico 7: Distribución de Edad por Categoría (Cajas)
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='CATEGORIA', y='EDAD2', data=df, palette='muted')
    plt.title('Distribución de Edad por Categoría Militar', fontsize=16, fontweight='bold')
    plt.xlabel('Categoría', fontsize=12)
    plt.ylabel('Edad (años)', fontsize=12)
    plt.savefig('grafico_edad_por_categoria.png')
    print("💾 Gráfico 'grafico_edad_por_categoria.png' guardado.")

    # Gráfico 8: Estado Civil por Género (Barras Agrupadas)
    plt.figure(figsize=(12, 8))
    sns.countplot(y='ESTADO_CIVIL', hue='SEXO', data=df, palette='coolwarm', order=df['ESTADO_CIVIL'].value_counts().index)
    plt.title('Distribución de Estado Civil por Género', fontsize=16, fontweight='bold')
    plt.xlabel('Cantidad', fontsize=12)
    plt.ylabel('Estado Civil', fontsize=12)
    plt.legend(title='Género')
    plt.savefig('grafico_estado_civil_por_genero.png')
    print("💾 Gráfico 'grafico_estado_civil_por_genero.png' guardado.")

except FileNotFoundError:
    print("❌ ERROR: No se encontró el archivo '../JEFAB_2024_corregido.xlsx - Sheet1.csv'.")
    print("Asegúrate de que el archivo de datos esté en la carpeta principal del proyecto.")
except KeyError as e:
    print(f"❌ ERROR de columna: No se encontró la columna {e}. Revisa los nombres en el archivo.")

print("\n--- Proceso de generación de gráficos finalizado ---")