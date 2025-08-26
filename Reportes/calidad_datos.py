# calidad_datos.py
import pandas as pd
import numpy as np

# Leer los datos
df = pd.read_excel('datos/JEFAB_2024.xlsx')

# Análisis de datos faltantes
print("=== ANÁLISIS DE DATOS FALTANTES ===")
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

# Identificar columnas problemáticas
print(f"\n=== COLUMNAS CON CARACTERES ESPECIALES ===")
problematic_columns = [col for col in df.columns if 'Ã' in col or 'â' in col]
print(f"Columnas con encoding problemático: {len(problematic_columns)}")
for col in problematic_columns[:5]:
    print(f" - {col}")   # ahora bien indentado

# -----------------------------
# Corrección de caracteres mal leídos
# -----------------------------
reemplazos = {
    "Ã¡": "á", "Ã©": "é", "Ã­": "í", "Ã³": "ó", "Ãº": "ú",
    "Ã": "Á", "Ã‰": "É", "Ã": "Í", "Ã“": "Ó", "Ãš": "Ú",
    "Ã±": "ñ", "Ã‘": "Ñ", "Ã¼": "ü", "Ãœ": "Ü"
}

def limpiar_texto(texto):
    if isinstance(texto, str):
        for mal, bien in reemplazos.items():
            texto = texto.replace(mal, bien)
    return texto

# Crear copia corregida
df_corregido = df.copy()
for col in df_corregido.select_dtypes(include=['object']).columns:
    df_corregido[col] = df_corregido[col].apply(limpiar_texto)

# -----------------------------
# Diccionario de parentescos
# -----------------------------
mapa_keywords = {
    # --- Singular ---
    "madre|mamá|mama": "Madre",
    "padre|papá|papa": "Padre",
    "abuela|abuelita|nona": "Abuela",
    "abuelo|abuelito": "Abuelo",
    "tío|tio": "Tío",
    "tía|tia": "Tía",
    "hermano|hermanito": "Hermano",
    "hermana|hermanita": "Hermana",
    "primo": "Primo",
    "prima": "Prima",
    "suegro": "Suegro",
    "suegra": "Suegra",
    "esposo|esposa|pareja|compañero": "Pareja",
    "hijo|hija|hij@": "Hijo",
    "nieto": "Nieto",
    "nieta": "Nieta",
    "sobrino": "Sobrino",
    "sobrina": "Sobrina",
    "cuñado": "Cuñado",
    "cuñada": "Cuñada",
    "padrastro": "Padrastro",
    "madrastra": "Madrastra",
    "bisabuelo": "Bisabuelo",
    "bisabuela": "Bisabuela",
    "padrino": "Padrino",
    "madrina": "Madrina",
    "ex pareja|expareja": "Ex Pareja",

    # --- Plural (se respetan tal cual) ---
    "abuelos": "Abuelos",
    "padres": "Padres",
    "hijos": "Hijos",
    "suegros": "Suegros",
    "hermanos": "Hermanos",
    "hermanas": "Hermanas",
    "primos": "Primos",
    "primas": "Primas",
    "nietos": "Nietos",
    "nietas": "Nietas",
    "sobrinos": "Sobrinos",
    "sobrinas": "Sobrinas",
    "cuñados": "Cuñados"
}

# -----------------------------
# Función de estandarización
# -----------------------------
def estandarizar_parentesco(texto):
    if not isinstance(texto, str):
        return texto
    
    limpio = texto.lower()
    categorias = []
    for patron, categoria in mapa_keywords.items():
        if re.search(rf"\b{patron}\b", limpio):
            categorias.append(categoria)
    
    if categorias:
        return ", ".join(sorted(set(categorias)))
    return texto  # deja el valor original si no coincide

# -----------------------------
# Aplicar a toda la base
# -----------------------------
for col in df_corregido.select_dtypes(include=["object"]).columns:
    df_corregido[col] = df_corregido[col].apply(estandarizar_parentesco)

# -----------------------------
# Guardar resultado limpio
# -----------------------------
df_corregido.to_excel("datos/JEFAB_2024_limpio.xlsx", index=False)
print(" Base corregida y guardada como 'JEFAB_2024_limpio.xlsx'")
