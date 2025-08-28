
# ==============================================================
# PASO 1: IMPORTAR LIBRERÍAS
# ==============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ==============================================================
# PASO 2: CARGAR EL ARCHIVO DE DATOS
# ==============================================================

archivo = '../JEFAB_2024_corregido.xlsx'
df = pd.read_excel(archivo)

print("El archivo se cargó con éxito. Primeras 5 filas:")
print(df.head())
print("\nInformación general del DataFrame:")
df.info()


# ==============================================================
# PASO 3: EXPLORACIÓN INICIAL DE LOS DATOS
# ==============================================================

print("\nDimensiones del DataFrame (filas, columnas):")
print(df.shape)

print("\nEstadísticas descriptivas de las columnas numéricas:")
print(df.describe())

print("\nConteo de valores nulos por columna:")
print(df.isnull().sum())

print("=== INFORMACIÓN GENERAL ===")
print(f"Total de registros: {len(df)}")
print(f"Total de columnas: {len(df.columns)}")

# ==============================================================
# PASO 4: CONFIGURACIÓN PARA VISUALIZACIONES
# ==============================================================

sns.set_theme(style="whitegrid")


# ==============================================================
# FUNCIONES AUXILIARES
# ==============================================================

# Función para agregar etiquetas numéricas a las barras
def agregar_valores(ax, orient="v"):
    if orient == "v":  # barras verticales
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}',
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=9)
    else:  # barras horizontales
        for p in ax.patches:
            ax.annotate(f'{int(p.get_width())}',
                        (p.get_width(), p.get_y() + p.get_height() / 2.),
                        ha='left', va='center', fontsize=9)


# ==============================================================
# GRÁFICOS UNIVARIADOS
# ==============================================================

# Gráfico 1: Distribución de Edad
plt.figure(figsize=(10, 6))
sns.histplot(df['EDAD2'], bins=20, kde=True, color='dodgerblue')
plt.title('Distribución de la Edad del Personal', fontsize=16, fontweight='bold')
plt.xlabel('Edad (años)')
plt.ylabel('Frecuencia')
plt.savefig('grafico_distribucion_edad.png')

# Análisis de edad
print("\n=== ANÁLISIS DE EDAD ===")
print(f"Edad promedio: {df['EDAD2'].mean():.1f} años")
print(f"Edad mínima: {df['EDAD2'].min()} años")
print(f"Edad máxima: {df['EDAD2'].max()} años")

# Gráfico 2: Distribución de Género
plt.figure(figsize=(8, 6))
ax = sns.countplot(x='SEXO', data=df, order=df['SEXO'].value_counts().index, palette='viridis')
plt.title('Distribución por Género', fontsize=16, fontweight='bold')
plt.xlabel('Género')
plt.ylabel('Cantidad')
agregar_valores(ax, orient="v")
plt.savefig('grafico_distribucion_genero.png')

# Análisis de género
print("\n=== ANÁLISIS DE GÉNERO ===")
print(df['GENERO'].value_counts())


# Gráfico 3: Distribución por Categoría Militar
plt.figure(figsize=(12, 7))
ax = sns.countplot(y='CATEGORIA', data=df, order=df['CATEGORIA'].value_counts().index, palette='plasma')
plt.title('Distribución por Categoría Militar', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad')
plt.ylabel('Categoría')
agregar_valores(ax, orient="h")
plt.savefig('grafico_distribucion_categoria.png')

# Gráfico 4: Distribución por Grado Militar (sin "No responde")
df_grado = df[df['GRADO'].str.lower() != "no responde"]
plt.figure(figsize=(12, 10))
ax = sns.countplot(y='GRADO', data=df_grado, order=df_grado['GRADO'].value_counts().index, palette='magma')
plt.title('Distribución por Grado Específico', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad')
plt.ylabel('Grado')
agregar_valores(ax, orient="h")
plt.tight_layout()
plt.savefig('grafico_distribucion_grado.png')

# Gráfico 5: Distribución por Estado Civil
plt.figure(figsize=(12, 7))
ax = sns.countplot(y='ESTADO_CIVIL', data=df, order=df['ESTADO_CIVIL'].value_counts().index, palette='cividis')
plt.title('Distribución por Estado Civil', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad')
plt.ylabel('Estado Civil')
agregar_valores(ax, orient="h")
plt.savefig('grafico_distribucion_estado_civil.png')

# Gráfico 6: Distribución por Nivel Educativo
plt.figure(figsize=(12, 8))
ax = sns.countplot(y='NIVEL_EDUCATIVO', data=df,
                   order=df['NIVEL_EDUCATIVO'].value_counts().index, palette='inferno')
plt.title('Distribución por Nivel Educativo', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad')
plt.ylabel('Nivel Educativo')
agregar_valores(ax, orient="h")
plt.tight_layout()
plt.savefig('grafico_distribucion_nivel_educativo.png')


# ==============================================================
# GRÁFICOS BIVARIADOS
# ==============================================================

# Gráfico 7: Edad por Categoría Militar
plt.figure(figsize=(10, 7))
sns.boxplot(x='CATEGORIA', y='EDAD2', data=df, palette='muted')
plt.title('Distribución de Edad por Categoría Militar', fontsize=16, fontweight='bold')
plt.xlabel('Categoría')
plt.ylabel('Edad (años)')
plt.savefig('grafico_edad_por_categoria.png')

# Gráfico 8: Estado Civil por Género
plt.figure(figsize=(12, 8))
ax = sns.countplot(y='ESTADO_CIVIL', hue='SEXO', data=df,
                   order=df['ESTADO_CIVIL'].value_counts().index, palette='coolwarm')
plt.title('Distribución de Estado Civil por Género', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad')
plt.ylabel('Estado Civil')
plt.legend(title='Género')
for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='edge', fontsize=8)
plt.savefig('grafico_estado_civil_por_genero.png')

# Gráfico 9: Grado Militar por Género (sin "No responde")
plt.figure(figsize=(12, 8))
ax = sns.countplot(y='GRADO', hue='SEXO', data=df_grado,
                   order=df_grado['GRADO'].value_counts().index, palette='coolwarm')
plt.title('Distribución de Grado Militar por Género', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad')
plt.ylabel('Grado')
plt.legend(title='Género')
for container in ax.containers:
    ax.bar_label(container, fmt='%d', label_type='edge', fontsize=8)
plt.tight_layout()
plt.savefig('grafico_grado_por_genero.png')

# Gráfico 10: Relación entre Nivel Educativo y Grado Militar (sin "No responde")

# Filtrar datos quitando "No responde" en GRADO y NIVEL_EDUCATIVO
df_rel = df[
    (df['GRADO'].str.lower() != "no responde") &
    (df['NIVEL_EDUCATIVO'].str.lower() != "no responde")
]

plt.figure(figsize=(14, 10))
ax = sns.countplot(
    y='GRADO', hue='NIVEL_EDUCATIVO',
    data=df_rel,
    order=df_rel['GRADO'].value_counts().index,
    palette='Spectral'
)

plt.title('Relación entre Nivel Educativo y Grado Militar', fontsize=16, fontweight='bold')
plt.xlabel('Cantidad')
plt.ylabel('Grado Militar')
plt.legend(title='Nivel Educativo', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('grafico_nivel_educativo_por_grado.png')

# ==============================================================
# RESPUESTAS A LAS 3 PREGUNTAS 
# ==============================================================

# Pregunta 1: Rango de edad más común
rango_edad = pd.cut(df['EDAD2'], bins=10).value_counts().idxmax()
print("\nPregunta 1 - Rango de edad más común:", rango_edad)

# Pregunta 2: Diferencias por género
conteo_genero = df['SEXO'].value_counts()
print("\nPregunta 2 - Distribución por género:")
print(conteo_genero)

# Pregunta 3: Grado militar más frecuente (sin 'No responde')
grado_mas_frecuente = df_grado['GRADO'].mode()[0]
print("\nPregunta 3 - Grado militar más frecuente:", grado_mas_frecuente)


# Mostrar todos los gráficos
plt.show()
