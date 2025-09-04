# ==============================================================
# PASO 1: IMPORTAR LIBRERÍAS
# ==============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency

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
# ANÁLISIS ESTADÍSTICO DEMOGRÁFICO ESPECIALIZADO
# ==============================================================

print("\n" + "="*60)
print("ANÁLISIS ESTADÍSTICO DEMOGRÁFICO ESPECIALIZADO")
print("="*60)

# Función para calcular índices demográficos especializados
def calcular_indices_demograficos():
    """Calcula índices demográficos especializados"""
    
    # Índice de masculinidad
    hombres = len(df[df['SEXO'] == 'HOMBRE'])
    mujeres = len(df[df['SEXO'] == 'MUJER'])
    indice_masculinidad = (hombres / mujeres) * 100
    
    # Índice de dependencia demográfica (adaptado)
    jovenes = len(df[df['EDAD2'] < 30])  # Menores de 30
    adultos_mayores = len(df[df['EDAD2'] >= 50])  # 50 años o más
    poblacion_activa = len(df[(df['EDAD2'] >= 30) & (df['EDAD2'] < 50)])
    indice_dependencia = ((jovenes + adultos_mayores) / poblacion_activa) * 100
    
    # Coeficiente de variación etaria
    cv_edad = (df['EDAD2'].std() / df['EDAD2'].mean()) * 100
    
    # Mediana de edad por categoría
    edad_mediana_categoria = df.groupby('CATEGORIA')['EDAD2'].median()
    
    print("\n ÍNDICES DEMOGRÁFICOS ESPECIALIZADOS:")
    print(f"  Índice de Masculinidad: {indice_masculinidad:.1f} hombres por cada 100 mujeres")
    print(f"  Índice de Dependencia Demográfica: {indice_dependencia:.1f}%")
    print(f"  Coeficiente de Variación Etaria: {cv_edad:.1f}%")
    print(f"  Edad mediana OFICIAL: {edad_mediana_categoria.get('OFICIAL', 'N/A'):.1f} años")
    print(f"  Edad mediana SUBOFICIAL: {edad_mediana_categoria.get('SUBOFICIAL', 'N/A'):.1f} años")
    print(f"  Edad mediana CIVIL: {edad_mediana_categoria.get('CIVIL', 'N/A'):.1f} años")
    
    return indice_masculinidad, indice_dependencia, cv_edad

# Función para análisis de estructura etaria
def analizar_estructura_etaria():
    """Análisis especializado de estructura etaria"""
    
    # Grupos etarios estándar demográficos
    df['GRUPO_ETARIO'] = pd.cut(df['EDAD2'], 
                               bins=[0, 25, 35, 45, 55, 100], 
                               labels=['18-25', '26-35', '36-45', '46-55', '56+'])
    
    distribucion_etaria = df['GRUPO_ETARIO'].value_counts().sort_index()
    porcentajes_etaria = (distribucion_etaria / len(df) * 100).round(1)
    
    print("\n ESTRUCTURA ETARIA DEMOGRÁFICA:")
    for grupo, count in distribucion_etaria.items():
        pct = porcentajes_etaria[grupo]
        print(f"  {grupo} años: {count:4d} personas ({pct:4.1f}%)")
    
    # Concentración etaria (% en grupo modal)
    grupo_modal = distribucion_etaria.idxmax()
    concentracion = porcentajes_etaria[grupo_modal]
    print(f"\n  Grupo etario modal: {grupo_modal} ({concentracion:.1f}%)")
    
    return distribucion_etaria, grupo_modal

# Función para análisis de asociaciones demográficas
def analizar_asociaciones_demograficas():
    """Análisis de asociaciones entre variables demográficas clave"""
    
    print("\n ASOCIACIONES DEMOGRÁFICAS (Test Chi-cuadrado):")
    
    # Asociaciones clave para análisis demográfico
    asociaciones = [
        ('SEXO', 'CATEGORIA'),
        ('GRUPO_ETARIO', 'CATEGORIA'),
        ('ESTADO_CIVIL', 'SEXO'),
        ('NIVEL_EDUCATIVO', 'CATEGORIA')
    ]
    
    resultados = {}
    
    for var1, var2 in asociaciones:
        # Crear tabla de contingencia
        tabla = pd.crosstab(df[var1], df[var2])
        
        # Test chi-cuadrado
        chi2, p_val, dof, expected = chi2_contingency(tabla)
        
        # V de Cramér (fuerza de asociación)
        n = tabla.sum().sum()
        cramer_v = np.sqrt(chi2 / (n * (min(tabla.shape) - 1)))
        
        # Interpretación demográfica
        if p_val < 0.01:
            significancia = "Muy significativa"
        elif p_val < 0.05:
            significancia = "Significativa"
        else:
            significancia = "No significativa"
        
        fuerza = "Fuerte" if cramer_v > 0.3 else "Moderada" if cramer_v > 0.1 else "Débil"
        
        print(f"  {var1} × {var2}:")
        print(f"    Chi² = {chi2:.2f}, p = {p_val:.4f} ({significancia})")
        print(f"    V de Cramér = {cramer_v:.3f} (Asociación {fuerza})")
        
        resultados[f"{var1}×{var2}"] = {'chi2': chi2, 'p_val': p_val, 'cramer_v': cramer_v}
    
    return resultados

# Función para análisis de diferencias por subgrupos
def analizar_diferencias_subgrupos():
    """Análisis de diferencias de edad entre subgrupos demográficos"""
    
    print("\n DIFERENCIAS DE EDAD POR SUBGRUPOS:")
    
    # Test t para diferencias por género
    edad_h = df[df['SEXO'] == 'HOMBRE']['EDAD2']
    edad_m = df[df['SEXO'] == 'MUJER']['EDAD2']
    
    t_stat, p_val = stats.ttest_ind(edad_h, edad_m)
    diferencia_media = edad_h.mean() - edad_m.mean()
    
    print(f"  Diferencia H-M en edad promedio: {diferencia_media:+.1f} años")
    print(f"  Test t: t = {t_stat:.3f}, p = {p_val:.4f}")
    print(f"  Resultado: {'Significativa' if p_val < 0.05 else 'No significativa'}")
    
    # ANOVA para diferencias por categoría
    grupos_categoria = [df[df['CATEGORIA'] == cat]['EDAD2'] for cat in df['CATEGORIA'].unique()]
    f_stat, p_anova = stats.f_oneway(*grupos_categoria)
    
    print(f"\n  Variación de edad entre categorías:")
    print(f"  ANOVA: F = {f_stat:.3f}, p = {p_anova:.4f}")
    print(f"  Resultado: {'Significativa' if p_anova < 0.05 else 'No significativa'}")
    
    return t_stat, p_val, f_stat, p_anova

# Ejecutar análisis estadísticos especializados
indice_masc, indice_dep, cv_edad = calcular_indices_demograficos()
dist_etaria, grupo_modal = analizar_estructura_etaria()
asociaciones_result = analizar_asociaciones_demograficas()
t_genero, p_genero, f_categoria, p_categoria = analizar_diferencias_subgrupos()

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
print(df['SEXO'].value_counts())

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
# GRÁFICO ESTADÍSTICO ADICIONAL: PIRÁMIDE ETARIA
# ==============================================================

plt.figure(figsize=(12, 8))

# Crear pirámide etaria por género
grupos_edad = ['18-25', '26-35', '36-45', '46-55', '56+']
df_piramide = df.groupby(['GRUPO_ETARIO', 'SEXO']).size().unstack(fill_value=0)

# Convertir a porcentajes
df_piramide_pct = df_piramide.div(len(df)) * 100

# Crear pirámide
y_pos = range(len(grupos_edad))
hombres = df_piramide_pct.get('HOMBRE', [0]*len(grupos_edad))
mujeres = df_piramide_pct.get('MUJER', [0]*len(grupos_edad))

plt.barh(y_pos, -hombres, align='center', color='steelblue', alpha=0.8, label='Hombres')
plt.barh(y_pos, mujeres, align='center', color='lightcoral', alpha=0.8, label='Mujeres')

plt.yticks(y_pos, grupos_edad)
plt.xlabel('Porcentaje de población (%)')
plt.ylabel('Grupos etarios')
plt.title('Pirámide Etaria del Personal FAC 2024', fontsize=16, fontweight='bold')
plt.legend()

# Agregar línea central
plt.axvline(0, color='black', linewidth=0.8)

# Ajustar etiquetas del eje x para mostrar valores absolutos
ax = plt.gca()
ticks = ax.get_xticks()
ax.set_xticks(ticks)
ax.set_xticklabels([f'{abs(x):.1f}' for x in ticks])

plt.tight_layout()
plt.savefig('grafico_piramide_etaria.png')

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

# ==============================================================
# RESUMEN DEMOGRÁFICO ESTADÍSTICO
# ==============================================================

print("\n" + "="*60)
print("RESUMEN DEMOGRÁFICO ESTADÍSTICO")
print("="*60)

print(f"""
 PERFIL DEMOGRÁFICO INSTITUCIONAL:
• Población total: {len(df):,} efectivos
• Índice de masculinidad: {indice_masc:.1f} (por cada 100 mujeres)
• Edad promedio: {df['EDAD2'].mean():.1f} años
• Grupo etario predominante: {grupo_modal}
• Coeficiente de variación etaria: {cv_edad:.1f}%

 ESTRUCTURA ORGANIZACIONAL:
• Concentración en SUBOFICIALES: {df['CATEGORIA'].value_counts()['SUBOFICIAL']:,} efectivos
• Grado más frecuente: {grado_mas_frecuente}
• Estado civil predominante: {df['ESTADO_CIVIL'].mode()[0]}

 HALLAZGOS ESTADÍSTICOS:
• Diferencia de edad H-M: {'Significativa' if p_genero < 0.05 else 'No significativa'} (p={p_genero:.4f})
• Variación etaria por categoría: {'Significativa' if p_categoria < 0.05 else 'No significativa'} (p={p_categoria:.4f})
• Asociación más fuerte: {max(asociaciones_result.items(), key=lambda x: x[1]['cramer_v'])[0]}
""")

# Mostrar todos los gráficos
plt.show()