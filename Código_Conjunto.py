# ================================================================
# Script: Codigo_conjunto.py
# Autor: 
- Ángela Rico: Análisis de demografía básica.  
- Ángela Tatiana Orjuela: Análisis de estructura familiar.  
- Karen Juliana Suárez Cruz: Calidad de datos  
# Descripción: 
#   Este script realiza un proceso completo de calidad y depuración 
#   sobre la base de datos de la Fuerza Aérea Colombiana (FAC).
#   Incluye:
#   - Carga de datos
#   - Análisis exploratorio inicial
#   - Identificación de faltantes, duplicados y encoding defectuoso
#   - Normalización y estandarización de texto
#   - Imputación lógica en variables familiares
#   - Exportación de dataset corregido
# ================================================================

# ==============================================================
# CALIDAD DE DATOS
# ==============================================================

# ================================================================
# Script: calidad_datos.py
# Autor: Karen Juliana Suárez Cruz
# Descripción: 
#   Este script realiza un proceso completo de calidad y depuración 
#   sobre la base de datos de la Fuerza Aérea Colombiana (FAC).
#   Incluye:
#   - Carga de datos
#   - Análisis exploratorio inicial
#   - Identificación de faltantes, duplicados y encoding defectuoso
#   - Normalización y estandarización de texto
#   - Imputación lógica en variables familiares
#   - Exportación de dataset corregido
# ================================================================

# ================== 0. IMPORTACIÓN DE LIBRERÍAS ==================
import pandas as pd
import numpy as np
import unicodedata
import re

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.experimental import enable_iterative_imputer  # habilita IterativeImputer
from sklearn.impute import IterativeImputer, KNNImputer

# ================== 1. CARGA DE DATOS ==================
# Se lee la base de datos desde Excel
df = pd.read_excel('datos/JEFAB_2024.xlsx')

# Se imprime información básica del dataset
print(f"\n=== INFORMACIÓN GENERAL ===")
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

# ================== 2. ANÁLISIS INICIAL ==================
# ---- Datos faltantes ----
print("=== ANÁLISIS DE DATOS FALTANTES ===")
missing_data = df.isnull().sum()                    # Conteo de valores nulos
missing_percent = (missing_data / len(df)) * 100    # Porcentaje de nulos
missing_info = pd.DataFrame({                       # DataFrame resumen
    'Columna': missing_data.index,
    'Datos_Faltantes': missing_data.values,
    'Porcentaje': missing_percent.values
}).sort_values('Datos_Faltantes', ascending=False)
print("Top 10 columnas con más datos faltantes:")
print(missing_info.head(10))

# ---- Registros duplicados ----
print(f"\n=== ANÁLISIS DE DUPLICADOS ===")
print(f"Registros duplicados: {df.duplicated().sum()}")

# ---- Tipos de datos ----
print(f"\n=== TIPOS DE DATOS ===")
print(df.dtypes.value_counts())

# ---- Problemas de encoding en nombres de columnas ----
print(f"\n=== COLUMNAS CON CARACTERES ESPECIALES ===")
problematic_columns = [col for col in df.columns if 'Ã' in col or 'â' in col]
print(f"Columnas con encoding problemático: {len(problematic_columns)}")
for col in problematic_columns[:5]:   # Se listan solo las primeras 5
    print(f" - {col}")

# ================== 3. FUNCIONES DE LIMPIEZA ==================
# Diccionario de reemplazos para corregir errores comunes de codificación
reemplazos = {
    "Ã¡": "á", "Ã©": "é", "Ã­": "í", "Ã³": "ó", "Ãº": "ú",
    "Ã": "Á", "Ã‰": "É", "Ã": "Í", "Ã“": "Ó", "Ãš": "Ú",
    "Ã±": "ñ", "Ã‘": "Ñ", "Ã¼": "ü", "Ãœ": "Ü"
}

def corregir_encoding(s: str) -> str:
    """Corrige caracteres mal codificados en un string."""
    if not isinstance(s, str):   # Si no es texto, lo deja igual
        return s
    for k, v in reemplazos.items():
        s = s.replace(k, v)
    return s

def normalizar_texto(s):
    """Normaliza texto: corrige encoding, elimina acentos y pasa a minúsculas."""
    if pd.isna(s):
        return s
    s = str(s)
    s = corregir_encoding(s)
    # Se eliminan acentos con unicodedata
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) 
                if not unicodedata.combining(c))
    return s.strip().lower()

# Diccionario de categorías equivalentes (singulares, plurales, variantes con acento)
map_categorias = {
    "Madre": ["mama", "mamá", "madre"],
    "Padre": ["papa", "papá", "padre"],
    "Tio": ["tio", "tío"],
    "Tia": ["tia", "tía"],
    "Primo": ["primo"],
    "Prima": ["prima"],
    "Abuelo": ["abuelo"],
    "Abuela": ["abuela"],
    "Madres": ["mamas", "mamás", "madres"],
    "Padres": ["papas", "papás", "padres"],
    "Tios": ["tios", "tíos"],
    "Tias": ["tias", "tías"],
    "Primos": ["primos"],
    "Primas": ["primas"],
    "Abuelos": ["abuelos"],
    "Abuelas": ["abuelas"]
}

# Invertir el diccionario: de variante -> categoría canónica
canon_map = {}
for canon, variantes in map_categorias.items():
    for v in variantes:
        canon_map[normalizar_texto(v)] = canon

# ================== 4. AGRUPAMIENTO DE VARIANTES ==================
# Se agrupan valores equivalentes en columnas de texto
text_cols = df.select_dtypes(include=['object']).columns
agrupamientos = {}
for col in text_cols:
    valores = df[col].dropna().astype(str).unique()
    agrupados = {}
    for val in valores:
        norm = normalizar_texto(val)
        canon = canon_map.get(norm, val)   # Si existe, lo reemplaza por su categoría
        agrupados.setdefault(canon, []).append(val)
    # Solo se reportan agrupamientos con más de una variante
    agrupamientos[col] = {k: v for k, v in agrupados.items() if len(v) > 1}

# Reporte de agrupamientos detectados
print("\n=== AGRUPAMIENTO DE VARIANTES (Singular/Plural/Género) ===")
for col, grupos in agrupamientos.items():
    if grupos:
        print(f"\nColumna: {col}")
        for canon, variantes in grupos.items():
            print(f"  → {canon}: {variantes}")

# ================== 5. CREAR DATASET CORREGIDO ==================
df_corregido = df.copy()

for col in text_cols:
    # Normalización básica
    df_corregido[col] = df_corregido[col].astype(str).apply(lambda x: normalizar_texto(x) if x != 'nan' else np.nan)
    # Limpieza de separadores en listas (ej: "madre ; padre")
    df_corregido[col] = df_corregido[col].str.replace(r'\s*;\s*', ';', regex=True)
    # Reemplazo por categorías canónicas
    df_corregido[col] = df_corregido[col].apply(
        lambda x: canon_map.get(x, x) if isinstance(x, str) else x
    )

# ================== 6. DEPURACIÓN CON IMPUTACIÓN LÓGICA ==================
# --- Relación HIJOS vs NUMERO_HIJOS ---
if 'HIJOS' in df_corregido.columns and 'NUMERO_HIJOS' in df_corregido.columns:
    cambios = ((df_corregido['HIJOS'] == "no") & (df_corregido['NUMERO_HIJOS'].isna())).sum()
    print(f"\n=== IMPUTACIÓN LÓGICA: HIJOS vs NUMERO_HIJOS ===")
    print(f"Registros a corregir: {cambios}")
    # Se imputan 0 hijos cuando la persona dijo explícitamente que no tiene
    df_corregido.loc[
        (df_corregido['HIJOS'] == "no") & (df_corregido['NUMERO_HIJOS'].isna()), 
        'NUMERO_HIJOS'
    ] = 0
    print(f"Corrección aplicada.")

# --- Relación HIJOS vs HIJOS_EN_HOGAR ---
if 'HIJOS' in df_corregido.columns and 'HIJOS_EN_HOGAR' in df_corregido.columns:
    cambios = ((df_corregido['HIJOS'] == "no") & (df_corregido['HIJOS_EN_HOGAR'].isna())).sum()
    print(f"\n=== IMPUTACIÓN LÓGICA: HIJOS vs HIJOS_EN_HOGAR ===")
    print(f"Registros a corregir: {cambios}")
    df_corregido.loc[
        (df_corregido['HIJOS'] == "no") & (df_corregido['HIJOS_EN_HOGAR'].isna()), 
        'HIJOS_EN_HOGAR'
    ] = 0
    print("Corrección aplicada.")

# --- Relación MADRE_VIVE vs EDAD_MADRE ---
if 'MADRE_VIVE' in df_corregido.columns:
    cambios_madre = ((df_corregido['MADRE_VIVE'] == "no") & (df_corregido['EDAD_MADRE'].isna())).sum()
    df_corregido.loc[(df_corregido['MADRE_VIVE'] == "no") & (df_corregido['EDAD_MADRE'].isna()), 'EDAD_MADRE'] = 0
    print(f"\n=== IMPUTACIÓN LÓGICA: MADRE_VIVE vs EDAD_MADRE ===")
    print(f"Registros corregidos: {cambios_madre}")

    cambios_rango_madre = ((df_corregido['MADRE_VIVE'] == "no") & (df_corregido['EDAD_RANGO_MADRE'].isna())).sum()
    df_corregido.loc[(df_corregido['MADRE_VIVE'] == "no") & (df_corregido['EDAD_RANGO_MADRE'].isna()), 'EDAD_RANGO_MADRE'] = 0
    print(f"Registros corregidos en rango madre: {cambios_rango_madre}")

# --- Relación PADRE_VIVE vs EDAD_PADRE ---
if 'PADRE_VIVE' in df_corregido.columns:
    cambios_padre = ((df_corregido['PADRE_VIVE'] == "no") & (df_corregido['EDAD_PADRE'].isna())).sum()
    df_corregido.loc[(df_corregido['PADRE_VIVE'] == "no") & (df_corregido['EDAD_PADRE'].isna()), 'EDAD_PADRE'] = 0
    print(f"\n=== IMPUTACIÓN LÓGICA: PADRE_VIVE vs EDAD_PADRE ===")
    print(f"Registros corregidos: {cambios_padre}")

    cambios_rango_padre = ((df_corregido['PADRE_VIVE'] == "no") & (df_corregido['EDAD_RANGO_PADRE'].isna())).sum()
    df_corregido.loc[(df_corregido['PADRE_VIVE'] == "no") & (df_corregido['EDAD_RANGO_PADRE'].isna()), 'EDAD_RANGO_PADRE'] = 0
    print(f"Registros corregidos en rango padre: {cambios_rango_padre}")

# ============================================================
# PASO 7: Imputación avanzada de variables
# ============================================================

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import matplotlib.pyplot as plt

# --- 7A. Preparamos columnas numéricas ---
num_cols = df_corregido.select_dtypes(include=["int64", "float64"]).columns
df_temp = df_corregido[num_cols].copy()

# --- 7B. Convertir ceros en NaN SOLO si el padre/madre está vivo ---
mask_padre_vivo = df_corregido["PADRE_VIVE"] == 1
mask_madre_vivo = df_corregido["MADRE_VIVE"] == 1

for col in ["EDAD_PADRE", "EDAD_RANGO_PADRE"]:
    if col in df_temp.columns:
        df_temp.loc[mask_padre_vivo & (df_temp[col] == 0), col] = np.nan

for col in ["EDAD_MADRE", "EDAD_RANGO_MADRE"]:
    if col in df_temp.columns:
        df_temp.loc[mask_madre_vivo & (df_temp[col] == 0), col] = np.nan

# --- 7C. Aplicamos MICE ---
imputer = IterativeImputer(max_iter=10, random_state=42)
df_imputado = imputer.fit_transform(df_temp)

# Convertimos a DataFrame para mantener nombres y control
df_imputado = pd.DataFrame(df_imputado, columns=num_cols, index=df_temp.index)

# --- 🚨 7Cbis: Evitar negativos en TODAS las columnas numéricas ---
df_imputado = df_imputado.clip(lower=0)

# Redondear a enteros
df_imputado = np.round(df_imputado).astype(int)

# Reemplazamos en la base corregida
df_corregido[num_cols] = df_imputado

# --- 7D. Restaurar ceros para padres/madres fallecidos ---
df_corregido.loc[df_corregido["PADRE_VIVE"] == 0, ["EDAD_PADRE", "EDAD_RANGO_PADRE"]] = 0
df_corregido.loc[df_corregido["MADRE_VIVE"] == 0, ["EDAD_MADRE", "EDAD_RANGO_MADRE"]] = 0

print("\n>>> Imputación MICE aplicada en todas las variables numéricas. Negativos truncados a 0. Cerros preservados en fallecidos.")

# --- 7E. Reconstrucción de rangos después de imputación con MICE ---
# --- Función para asignar rangos ---
def edad_a_rango(edad):
    if pd.isna(edad) or edad == 0:
        return 0   # fallecido o sin dato
    elif 18 <= edad <= 22:
        return "18-22"
    elif 23 <= edad <= 27:
        return "23-27"
    elif 28 <= edad <= 32:
        return "28-32"
    elif 33 <= edad <= 37:
        return "33-37"
    elif 38 <= edad <= 42:
        return "38-42"
    elif 43 <= edad <= 47:
        return "43-47"
    elif 48 <= edad <= 52:
        return "48-52"
    elif 53 <= edad <= 57:
        return "53-57"
    elif 58 <= edad <= 62:
        return "58-62"
    else:
        return "Otro"

# --- Asignar rangos para madres vivas ---
df_corregido.loc[df_corregido["MADRE_VIVE"] == 1, "EDAD_RANGO_MADRE"] = (
    df_corregido.loc[df_corregido["MADRE_VIVE"] == 1, "EDAD_MADRE"].apply(edad_a_rango)
)

# --- Asignar rangos para padres vivos ---
df_corregido.loc[df_corregido["PADRE_VIVE"] == 1, "EDAD_RANGO_PADRE"] = (
    df_corregido.loc[df_corregido["PADRE_VIVE"] == 1, "EDAD_PADRE"].apply(edad_a_rango)
)

# --- Asegurar ceros en fallecidos ---
df_corregido.loc[df_corregido["MADRE_VIVE"] == 0, ["EDAD_MADRE","EDAD_RANGO_MADRE"]] = 0
df_corregido.loc[df_corregido["PADRE_VIVE"] == 0, ["EDAD_PADRE","EDAD_RANGO_PADRE"]] = 0



print("\n>>> Reconstrucción de rangos de edad realizada correctamente.")


#  ================== 8. GUARDAR RESULTADO ==================
df_corregido.to_excel("datos/JEFAB_2024_corregido.xlsx", index=False)
print("\n>>> Dataset corregido guardado como 'datos/JEFAB_2024_corregido.xlsx'")


# ==============================================================
# ANALISIS FAMILIAR
# ==============================================================

# -*- coding: utf-8 -*-
"""Análisis de Datos FAC familiar

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pBDJJeWRsua4-iPxqszbNrs_tH_lNb0Q
"""

# analisis_familiar.py
import pandas as pd #Pandas sirve para leer, limpiar y analizar datos en tablas (DataFrames)
import matplotlib.pyplot as plt # Se usa para hacer gráficas
# Leer los datos
df = pd.read_excel("/content/JEFAB_2024_corregido.xlsx")

print(df.columns.tolist()) # para ver las columnas
# Unificar categorías
df["ESTADO_CIVIL"] = df["ESTADO_CIVIL"].replace({
    "divorciado": "divorciado/separado",
    "separado": "divorciado/separado"
})

# Verificar cambios
print(df["ESTADO_CIVIL"].value_counts())

"""Analisis estado civil"""

# Análisis de estado civil
print("=== ANÁLISIS ESTADO CIVIL ===")
print(df['ESTADO_CIVIL'].value_counts()) # cuenta cuántas veces aparece cada categoría en esa columna.

# Gráfico de estado civil
plt.figure(figsize=(10, 6)) # define el tamaño en pulgadas (ancho=10, alto=6).
df['ESTADO_CIVIL'].value_counts().plot(kind='bar') # selecciona la columna de estado civil,cuenta cuántas veces aparece cada categoría.
plt.title('Distribución del Estado Civil')
plt.xlabel('Estado Civil')
plt.ylabel('Cantidad')
plt.xticks(rotation=45) # Rota las etiquetas del eje X 45 grados.
plt.tight_layout() # Ajusta automáticamente márgenes y espaciado.
plt.show() # Muestra el grafico

# Porcentaje para estado civil
porcentajes = df['ESTADO_CIVIL'].value_counts(normalize=True) * 100
print(porcentajes)

"""Anaisis de Hijos

"""

# Análisis de hijos
print("\n=== ANÁLISIS DE HIJOS ===")
print(f"Personal con hijos: {df['HIJOS'].value_counts()}")

"""Analisis de convivencia familiar"""

# Análisis de convivencia familiar
print("\n=== ANÁLISIS DE CONVIVENCIA ===")
print(f"Habita con familia: {df['HABITA_VIVIENDA_FAMILIAR'].value_counts()}")

# Cruce entre tener hijos y habitar con familia
print("\n=== CRUCE HIJOS Y CONVIVENCIA ===")
cruce = pd.crosstab(df['HIJOS'], df['HABITA_VIVIENDA_FAMILIAR'])
print(cruce)

# ================================
# HIJOS vs CONVIVENCIA FAMILIAR
# ================================
print("\n=== HIJOS vs CONVIVENCIA FAMILIAR ===")
tabla = pd.crosstab(df['HIJOS'], df['HABITA_VIVIENDA_FAMILIAR'])
print(tabla)

# Chi-cuadrado
chi2, p, dof, expected = chi2_contingency(tabla)
print("\nChi-cuadrado Hijos vs Convivencia: chi2 =", round(chi2,2), "p =", round(p,4))
if p < 0.05:
    print(" Existe asociación significativa entre Hijos y Convivencia Familiar")
else:
    print("No se encontró asociación significativa")

"""Analisis de Vivienda propia"""

import matplotlib.pyplot as plt
import pandas as pd

# Tabla de contingencia
tabla_hijos_vivienda = pd.crosstab(df['HIJOS'], df['VIVIENDA_PROPIA'])

print("=== TABLA HIJOS vs VIVIENDA PROPIA ===")
print(tabla_hijos_vivienda)

# Normalizada por fila (porcentaje)
tabla_hijos_vivienda_pct = pd.crosstab(df['HIJOS'], df['VIVIENDA_PROPIA'], normalize='index') * 100
print("\n=== TABLA PORCENTUAL HIJOS vs VIVIENDA PROPIA ===")
print(tabla_hijos_vivienda_pct.round(2))

# ================================
# HIJOS vs VIVIENDA PROPIA
# ================================
print("\n=== HIJOS vs VIVIENDA PROPIA ===")
tabla = pd.crosstab(df['HIJOS'], df['VIVIENDA_PROPIA'])
print(tabla)

# Chi-cuadrado
chi2, p, dof, expected = chi2_contingency(tabla)
print("\nChi-cuadrado Hijos vs Vivienda Propia: chi2 =", round(chi2,2), "p =", round(p,4))
if p < 0.05:
    print("👉 Existe asociación significativa entre Hijos y Vivienda Propia")
else:
    print("👉 No se encontró asociación significativa")

tabla_hijos_vivienda = pd.crosstab(df['HIJOS'], df['VIVIENDA_PROPIA'], normalize='index') * 100

tabla_hijos_vivienda.plot(kind='bar', figsize=(8,6))

plt.title("Relación entre Hijos y Vivienda Propia")
plt.ylabel("Porcentaje (%)")
plt.xlabel("Tiene Hijos")
plt.xticks(rotation=0)
plt.legend(title="Vivienda Propia", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

"""Analisis de categoria"""

# Cruce de Estado Civil y Categoría
print("\n=== CRUCE ESTADO CIVIL vs CATEGORIA ===")

tabla_cat = pd.crosstab(df['ESTADO_CIVIL'], df['CATEGORIA'])
print("\nFrecuencias absolutas:")
print(tabla_cat)

tabla_cat_pct = pd.crosstab(df['ESTADO_CIVIL'], df['CATEGORIA'], normalize='index') * 100
print("\nPorcentajes (% por fila):")
print(tabla_cat_pct.round(2))

tabla_estado_categoria = pd.crosstab(df['ESTADO_CIVIL'], df['CATEGORIA'], normalize='index') * 100

tabla_estado_categoria.plot(kind='bar', figsize=(10,6))

plt.title("Distribución de Categoría por Estado Civil")
plt.ylabel("Porcentaje (%)")
plt.xlabel("Estado Civil")
plt.xticks(rotation=45)
plt.legend(title="Categoría", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact, f_oneway, kruskal


# ================================
# ESTADO CIVIL vs CATEGORIA
# ================================
print("\n=== ESTADO CIVIL vs CATEGORIA ===")
tabla = pd.crosstab(df['ESTADO_CIVIL'], df['CATEGORIA'])
print(tabla)

# Chi-cuadrado
chi2, p, dof, expected = chi2_contingency(tabla)
print("\nChi-cuadrado Estado Civil vs Categoría: chi2 =", round(chi2,2), "p =", round(p,4))
if p < 0.05:
    print(" Existe asociación significativa entre Estado Civil y Categoría")
else:
    print(" No se encontró asociación significativa")

"""Relacion entre estado civil y edad"""

print(df.groupby("ESTADO_CIVIL")["EDAD2"].mean())

# ================================
# ESTADO CIVIL vs EDAD
# ================================
print("\n=== ESTADO CIVIL vs EDAD ===")
print(df.groupby("ESTADO_CIVIL")["EDAD2"].mean())

from scipy.stats import shapiro

print("\n=== PRUEBA DE NORMALIDAD (Shapiro-Wilk) ===")

for estado, grupo in df.groupby("ESTADO_CIVIL"):
    datos = grupo["EDAD2"].dropna()
    stat, p = shapiro(datos)
    print(f"{estado}: p = {round(p,4)}")
    if p < 0.05:
        print(" No hay normalidad")
    else:
        print("Normalidad aceptada")


# Agrupar por estado civil
grupos = [grupo["EDAD2"].dropna().values for _, grupo in df.groupby("ESTADO_CIVIL")]



# Kruskal-Wallis
kruskal_test = kruskal(*grupos)
print("Kruskal-Wallis H =", round(kruskal_test.statistic,2), "p =", round(kruskal_test.pvalue,4))

#!pip install scikit-posthocs
# Prueba de Dunn
import scikit_posthocs as sp

posthoc = sp.posthoc_dunn(df, val_col="EDAD2", group_col="ESTADO_CIVIL", p_adjust="bonferroni")
print(posthoc)

df.groupby("ESTADO_CIVIL")["EDAD2"].mean().plot(kind="bar")
plt.show()

plt.figure(figsize=(10,6))
df.boxplot(column="EDAD2", by="ESTADO_CIVIL", grid=False)
plt.title("Distribución de la edad según Estado Civil")
plt.suptitle("")  # elimina título extra de pandas
plt.xlabel("Estado Civil")
plt.ylabel("Edad")
plt.xticks(rotation=45)
plt.show()

#Hace un boxplot de la columna EDAD2 (edad).

#Separa los datos por cada categoría de ESTADO_CIVIL.

# grid=False quita las líneas de la cuadrícula de fondo.

"""Analisis de maltrato intrafamiliar"""

# Tabla de contingencia
cruce = pd.crosstab(df['HABITA_VIVIENDA_FAMILIAR'], df['MALTRATO_INTRAFAMILIAR'], margins=True)
print("\n=== Cruce HABITA_VIVIENDA_FAMILIAR vs MALTRATO_INTRAFAMILIAR ===")
print(cruce)

import matplotlib.pyplot as plt

# Gráfico de barras agrupadas
cruce_graf = pd.crosstab(df['HABITA_VIVIENDA_FAMILIAR'], df['MALTRATO_INTRAFAMILIAR'])
cruce_graf.plot(kind="bar", figsize=(8,5))

plt.title("Relación entre Habitar Vivienda Familiar y Maltrato Intrafamiliar")
plt.xlabel("Habita Vivienda Familiar")
plt.ylabel("Número de Personas")
plt.xticks(rotation=0)
plt.legend(title="Maltrato Intrafamiliar")
plt.show()

"""Analisis de relacion estable"""

# Tabla de contingencia
cruce_hijos_pareja = pd.crosstab(df['HIJOS'], df['RELACION_PAREJA_ESTABLE'], margins=True)
print("\n=== Cruce HIJOS vs RELACION_PAREJA_ESTABLE ===")
print(cruce_hijos_pareja)

# ================================
# HIJOS vs RELACION PAREJA ESTABLE
# ================================
print("\n=== HIJOS vs RELACION PAREJA ESTABLE ===")
tabla = pd.crosstab(df['HIJOS'], df['RELACION_PAREJA_ESTABLE'])
print(tabla)

# Fisher Exacto (para tablas 2x2)
oddsratio, p = fisher_exact(tabla)
print("Test exacto de Fisher p =", round(p,4))
if p < 0.05:
    print(" Existe asociación significativa entre Hijos y Relación de Pareja Estable")
else:
    print(" No se encontró asociación significativa")

# Gráfico de barras agrupadas
cruce_hijos_pareja_graf = pd.crosstab(df['HIJOS'], df['RELACION_PAREJA_ESTABLE'])
cruce_hijos_pareja_graf.plot(kind="bar", figsize=(8,5))

plt.title("Relación entre Hijos y Tener Pareja Estable")
plt.xlabel("¿Tiene Hijos?")
plt.ylabel("Número de Personas")
plt.xticks(rotation=0)
plt.legend(title="Pareja Estable")
plt.show()

"""Analisis fallecimiento padres"""

# Hijos con Madre Vive
cruce_hijos_madre = pd.crosstab(df['HIJOS'], df['MADRE_VIVE'], margins=True)
print("\n=== Cruce HIJOS vs MADRE_VIVE ===")
print(cruce_hijos_madre)

# Hijos con Padre Vive
cruce_hijos_padre = pd.crosstab(df['HIJOS'], df['PADRE_VIVE'], margins=True)
print("\n=== Cruce HIJOS vs PADRE_VIVE ===")
print(cruce_hijos_padre)

import matplotlib.pyplot as plt

# Cruces
madre = pd.crosstab(df['HIJOS'], df['MADRE_VIVE'])
padre = pd.crosstab(df['HIJOS'], df['PADRE_VIVE'])

# Unimos los dataframes para graficar juntos
cruce = pd.concat({"Madre Vive": madre, "Padre Vive": padre}, axis=1)

# Gráfico de barras apiladas
cruce.plot(kind="bar", figsize=(9,6))
plt.title("Relación entre Hijos y si Madre o Padre Vive")
plt.xlabel("¿Tiene Hijos?")
plt.ylabel("Número de Personas")
plt.xticks(rotation=0)
plt.show()

"""Relacion entre categoria y maltrato intrafamiliar"""

import matplotlib.pyplot as plt
import pandas as pd

# Gráfico de barras agrupadas por CATEGORIA
cruce_graf = pd.crosstab(df['CATEGORIA'], df['MALTRATO_INTRAFAMILIAR'])
cruce_graf.plot(kind="bar", figsize=(8,5))

plt.title("Relación entre Categoría y Maltrato Intrafamiliar")
plt.xlabel("Categoría")
plt.ylabel("Número de Personas")
plt.xticks(rotation=0)
plt.legend(title="Maltrato Intrafamiliar")
plt.show()

import pandas as pd

# Tabla de contingencia
cruce_graf = pd.crosstab(df['CATEGORIA'], df['MALTRATO_INTRAFAMILIAR'])

# Calcular porcentajes por fila
cruce_pct = cruce_graf.div(cruce_graf.sum(axis=1), axis=0) * 100

# Mostrar tabla de porcentajes
print("Porcentajes por categoría:")
print(cruce_pct.round(1))  # redondea a 1 decimal

# ==============================================================
# ANALISIS DEMOGRAFICO
# ==============================================================

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
