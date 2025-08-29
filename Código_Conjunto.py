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

# ================== 0. IMPORTACIÓN DE LIBRERÍAS ==================
import pandas as pd       # Manejo de DataFrames
import numpy as np        # Operaciones numéricas y valores NaN
import unicodedata        # Normalización y eliminación de acentos
import re                 # Expresiones regulares (limpieza de strings)

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

# ================== 7. GUARDAR RESULTADO ==================
df_corregido.to_excel("datos/JEFAB_2024_corregido.xlsx", index=False)
print("\n>>> Dataset corregido guardado como 'datos/JEFAB_2024_corregido.xlsx'")

