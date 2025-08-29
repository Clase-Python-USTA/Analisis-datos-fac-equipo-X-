# calidad_datos.py

# ================== 0. IMPORTACIÓN DE LIBRERÍAS ==================
# Importo las librerías necesarias para trabajar con mi base de datos:
# - pandas: manipulación de datos en DataFrames
# - numpy: operaciones numéricas y manejo de valores NaN
# - unicodedata: para normalizar y eliminar impurecesas de los textos
# - re: para usar expresiones regulares (limpieza de strings)
# ================== 0. IMPORTS ==================
# calidad_datos.py

import pandas as pd
import numpy as np
import unicodedata
import re   # Import necesario para expresiones regulares

# ================== 1. CARGA DE DATOS ==================
df = pd.read_excel('datos/JEFAB_2024.xlsx')

print(f"\n=== INFORMACIÓN GENERAL ===")
print(f"Filas: {df.shape[0]} | Columnas: {df.shape[1]}")

# ================== 2. ANÁLISIS INICIAL ==================
print("=== ANÁLISIS DE DATOS FALTANTES ===")
missing_data = df.isnull().sum()
missing_percent = (missing_data / len(df)) * 100
print("Top 10 columnas con más datos faltantes:")
missing_info = pd.DataFrame({
    'Columna': missing_data.index,
    'Datos_Faltantes': missing_data.values,
    'Porcentaje': missing_percent.values
}).sort_values('Datos_Faltantes', ascending=False)
print("Top 10 columnas con más datos faltantes:")
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
    """Corrige caracteres mal codificados"""
    if not isinstance(s, str):
        return s
    for k, v in reemplazos.items():
        s = s.replace(k, v)
    return s

def normalizar_texto(s):
    """Pasa a minúsculas, corrige encoding y elimina acentos"""
    if pd.isna(s):
        return s
    s = str(s)
    s = corregir_encoding(s)
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) 
                if not unicodedata.combining(c))
    return s.strip().lower()

# Diccionario de agrupamiento
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

# Invertir mapeo (variantes -> canon)
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

print("\n=== AGRUPAMIENTO DE VARIANTES (Singular/Plural/Género) ===")
for col, grupos in agrupamientos.items():
    if grupos:
        print(f"\nColumna: {col}")
        for canon, variantes in grupos.items():
            print(f"  → {canon}: {variantes}")

# ================== 5. CREAR DATASET CORREGIDO ==================
df_corregido = df.copy()

for col in text_cols:
    # Normalizar y limpiar
    df_corregido[col] = df_corregido[col].astype(str).apply(lambda x: normalizar_texto(x) if x != 'nan' else np.nan)
    # Quitar espacios extra en listas separadas por ";"
    df_corregido[col] = df_corregido[col].str.replace(r'\s*;\s*', ';', regex=True)
    # Unificar categorías conocidas
    df_corregido[col] = df_corregido[col].apply(
        lambda x: canon_map.get(x, x) if isinstance(x, str) else x
    )


# ================== 6. DEPURACION ==================
if 'HIJOS' in df_corregido.columns and 'NUMERO_HIJOS' in df_corregido.columns:
    # Cuenta cuántos registros cumplen la condición
    cambios = ((df_corregido['HIJOS'] == "no") & (df_corregido['NUMERO_HIJOS'].isna())).sum()
    
    print(f"\n=== IMPUTACIÓN LÓGICA: HIJOS vs NUMERO_HIJOS ===")
    print(f"Registros a corregir: {cambios}")
    
    # Aplica la corrección: donde HIJOS = "no" y NUMERO_HIJOS está vacío, pone un 0
    df_corregido.loc[
        (df_corregido['HIJOS'] == "no") & (df_corregido['NUMERO_HIJOS'].isna()), 
        'NUMERO_HIJOS'
    ] = 0
    print(f"Corrección aplicada.")

if 'HIJOS' in df_corregido.columns and 'HIJOS_EN_HOGAR' in df_corregido.columns:
    # Cuenta cuántos registros cumplen la condición
    cambios = ((df_corregido['HIJOS'] == "no") & (df_corregido['HIJOS_EN_HOGAR'].isna())).sum()
    
    print(f"\n=== IMPUTACIÓN LÓGICA: HIJOS vs HIJOS_EN_HOGAR ===")
    print(f"Registros a corregir: {cambios}")
    
    # Aplica la corrección: donde HIJOS = "no" y HIJOS_EN_HOGAR está vacío, pone un 0
    df_corregido.loc[
        (df_corregido['HIJOS'] == "no") & (df_corregido['HIJOS_EN_HOGAR'].isna()), 
        'HIJOS_EN_HOGAR'
    ] = 0
    
    print("Corrección aplicada.")

# --- IMPUTACIÓN MADRE ---
if 'MADRE_VIVE' in df_corregido.columns:
    # EDAD_MADRE
    cambios_madre = ((df_corregido['MADRE_VIVE'] == "no") & (df_corregido['EDAD_MADRE'].isna())).sum()
    df_corregido.loc[(df_corregido['MADRE_VIVE'] == "no") & (df_corregido['EDAD_MADRE'].isna()), 'EDAD_MADRE'] = 0
    print(f"\n=== IMPUTACIÓN LÓGICA: MADRE_VIVE vs EDAD_MADRE ===")
    print(f"Registros corregidos: {cambios_madre}")

    # EDAD_RANGO_MADRE
    cambios_rango_madre = ((df_corregido['MADRE_VIVE'] == "no") & (df_corregido['EDAD_RANGO_MADRE'].isna())).sum()
    df_corregido.loc[(df_corregido['MADRE_VIVE'] == "no") & (df_corregido['EDAD_RANGO_MADRE'].isna()), 'EDAD_RANGO_MADRE'] = 0
    print(f"\n=== IMPUTACIÓN LÓGICA: MADRE_VIVE vs EDAD_RANGO_MADRE ===")
    print(f"Registros corregidos: {cambios_rango_madre}")

# --- IMPUTACIÓN PADRE ---
if 'PADRE_VIVE' in df_corregido.columns:
    # EDAD_PADRE
    cambios_padre = ((df_corregido['PADRE_VIVE'] == "no") & (df_corregido['EDAD_PADRE'].isna())).sum()
    df_corregido.loc[(df_corregido['PADRE_VIVE'] == "no") & (df_corregido['EDAD_PADRE'].isna()), 'EDAD_PADRE'] = 0
    print(f"\n=== IMPUTACIÓN LÓGICA: PADRE_VIVE vs EDAD_PADRE ===")
    print(f"Registros corregidos: {cambios_padre}")

    # EDAD_RANGO_PADRE
    cambios_rango_padre = ((df_corregido['PADRE_VIVE'] == "no") & (df_corregido['EDAD_RANGO_PADRE'].isna())).sum()
    df_corregido.loc[(df_corregido['PADRE_VIVE'] == "no") & (df_corregido['EDAD_RANGO_PADRE'].isna()), 'EDAD_RANGO_PADRE'] = 0
    print(f"\n=== IMPUTACIÓN LÓGICA: PADRE_VIVE vs EDAD_RANGO_PADRE ===")
    print(f"Registros corregidos: {cambios_rango_padre}")


# ================== 7. GUARDAR RESULTADO ==================
df_corregido.to_excel("datos/JEFAB_2024_corregido.xlsx", index=False)
print("\n>>> Dataset corregido guardado como 'datos/JEFAB_2024_corregido.xlsx'")