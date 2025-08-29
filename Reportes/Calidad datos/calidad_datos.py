# calidad_datos.py

# ================== 0. IMPORTACIÓN DE LIBRERÍAS ==================
# Importo las librerías necesarias para trabajar con mi base de datos:
# - pandas: manipulación de datos en DataFrames
# - numpy: operaciones numéricas y manejo de valores NaN
# - unicodedata: para normalizar y eliminar impurecesas de los textos
# - re: para usar expresiones regulares (limpieza de strings)
# calidad_datos.py

import pandas as pd
import numpy as np
import unicodedata
import re
from pathlib import Path

# ================== 1. CARGA DE DATOS ==================
df = pd.read_excel('datos/JEFAB_2024.xlsx')

print(f"\n=== INFORMACIÓN GENERAL ===")
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

# ================== 2. ANÁLISIS INICIAL ==================
print("\n=== ANÁLISIS DE DATOS FALTANTES ===")
missing_data = df.isnull().sum()
missing_percent = (missing_data / len(df)) * 100
print("Top 10 columnas con más datos faltantes:")
missing_info = pd.DataFrame({
    'Columna': missing_data.index,
    'Datos_Faltantes': missing_data.values,
    'Porcentaje': missing_percent.values
}).sort_values('Datos_Faltantes', ascending=False)
print(missing_info.head(10))

# Análisis de duplicados
print(f"\n=== ANÁLISIS DE DUPLICADOS ===")
print(f"Registros duplicados: {df.duplicated().sum()}")

# Análisis de tipos de datos
print(f"\n=== TIPOS DE DATOS ===")
print(df.dtypes.value_counts())

# Columnas con caracteres especiales
print(f"\n=== COLUMNAS CON CARACTERES ESPECIALES ===")
problematic_columns = [col for col in df.columns if 'Ã' in col or 'â' in col]
print(f"Columnas con encoding problemático: {len(problematic_columns)}")
for col in problematic_columns[:5]:
    print(f" - {col}")

# ================== 3. FUNCIONES DE LIMPIEZA ==================
reemplazos = {
    "Ã¡": "á", "Ã©": "é", "Ã­": "í", "Ã³": "ó", "Ãº": "ú",
    "Ã": "Á", "Ã‰": "É", "Ã": "Í", "Ã“": "Ó", "Ãš": "Ú",
    "Ã±": "ñ", "Ã‘": "Ñ", "Ã¼": "ü", "Ãœ": "Ü"
}

def corregir_encoding(s: str) -> str:
    if not isinstance(s, str):
        return s
    for k, v in reemplazos.items():
        s = s.replace(k, v)
    return s

def normalizar_texto(s):
    if pd.isna(s):
        return s
    s = str(s)
    s = corregir_encoding(s)
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) 
                if not unicodedata.combining(c))
    return s.strip().lower()

# Diccionario de agrupamiento (ejemplo familiar)
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

# Invertir mapeo
canon_map = {}
for canon, variantes in map_categorias.items():
    for v in variantes:
        canon_map[normalizar_texto(v)] = canon

# ================== 4. AGRUPAMIENTO DE VARIANTES ==================
text_cols = df.select_dtypes(include=['object']).columns
agrupamientos = {}
for col in text_cols:
    valores = df[col].dropna().astype(str).unique()
    agrupados = {}
    for val in valores:
        norm = normalizar_texto(val)
        canon = canon_map.get(norm, val)
        agrupados.setdefault(canon, []).append(val)
    agrupamientos[col] = {k: v for k, v in agrupados.items() if len(v) > 1}

print("\n=== AGRUPAMIENTO DE VARIANTES ===")
for col, grupos in agrupamientos.items():
    if grupos:
        print(f"\nColumna: {col}")
        for canon, variantes in grupos.items():
            print(f"  → {canon}: {variantes}")

# ================== 5. ANÁLISIS DETALLADO EXTRA ==================
print("\n=== TABLA RESUMEN DE VARIABLES ===")
col_summary = pd.DataFrame({
    "Tipo": df.dtypes.astype(str),
    "Faltantes": df.isna().sum(),
    "Porcentaje": round(df.isna().sum()/len(df)*100,2),
    "Unicos": df.nunique(dropna=False)
}).sort_values("Porcentaje", ascending=False)
print(col_summary.head(10))

# Variables con >10% de missing
print("\n=== VARIABLES CON >10% DE MISSING ===")
print(col_summary[col_summary["Porcentaje"] > 10])

# Estadísticas numéricas
print("\n=== ESTADÍSTICAS NUMÉRICAS ===")
num_df = df.select_dtypes(include=[np.number])
if not num_df.empty:
    print(num_df.describe().T)

    # Outliers
    print("\n=== OUTLIERS DETECTADOS (IQR) ===")
    Q1 = num_df.quantile(0.25)
    Q3 = num_df.quantile(0.75)
    IQR = Q3 - Q1
    for col in num_df.columns:
        outliers = df[(df[col] < (Q1[col] - 1.5*IQR[col])) | (df[col] > (Q3[col] + 1.5*IQR[col]))]
        if not outliers.empty:
            print(f" - {col}: {len(outliers)} outliers ({len(outliers)/len(df)*100:.2f}%)")

# Correlaciones
print("\n=== CORRELACIONES ENTRE VARIABLES NUMÉRICAS ===")
if num_df.shape[1] > 1:
    print(num_df.corr().round(3))

# Análisis de categóricas
print("\n=== ANÁLISIS DE VARIABLES CATEGÓRICAS ===")
for col in text_cols:
    top_vals = df[col].astype(str).fillna("<NA>").value_counts().head(5)
    print(f"\nColumna: {col}\n{top_vals}")

    # Inconsistencias
    if df[col].dropna().astype(str).str.contains(r'^\s+|\s+$').any():
        print("  ⚠ Tiene espacios al inicio/final")
    lowered = df[col].dropna().astype(str).str.lower().unique()
    if len(lowered) < len(df[col].dropna().astype(str).unique()):
        print("  ⚠ Tiene mezcla mayúsc/minúsc")

# ================== 6. CREAR DATASET CORREGIDO ==================
df_corregido = df.copy()

for col in text_cols:
    # Normalizar y limpiar
    df_corregido[col] = df_corregido[col].astype(str).apply(lambda x: normalizar_texto(x) if x != 'nan' else np.nan)
    # Quitar espacios extra en listas separadas por ";"
    df_corregido[col] = df_corregido[col].str.replace(r'\s*;\s*', ';', regex=True)
    df_corregido[col] = df_corregido[col].apply(lambda x: canon_map.get(x, x) if isinstance(x, str) else x)

# ================== 7. GUARDAR RESULTADO ==================
Path("salidas").mkdir(exist_ok=True)

df_corregido.to_excel("salidas/JEFAB_2024_corregido.xlsx", index=False)
col_summary.to_excel("salidas/Resumen_Columnas.xlsx")

with open("salidas/Informe_Calidad_Datos.md","w",encoding="utf-8") as f:
    f.write("# Informe de Calidad de Datos\n")
    f.write(f"- Filas: {df.shape[0]} | Columnas: {df.shape[1]}\n")
    f.write("- Ver tablas auxiliares en Excel generado.\n")
    f.write("\n## Recomendaciones:\n")
    f.write("- Imputar variables con missing >10%\n")
    f.write("- Revisar duplicados aunque sean pocos\n")
    f.write("- Estandarizar categóricas (espacios, mayúsc/minúsc)\n")
    f.write("- Validar outliers antes de eliminarlos\n")

print("\n>>> Dataset corregido guardado como 'salidas/JEFAB_2024_corregido.xlsx'")
print(">>> Resumen de columnas en 'salidas/Resumen_Columnas.xlsx'")
print(">>> Informe generado en 'salidas/Informe_Calidad_Datos.md'")
