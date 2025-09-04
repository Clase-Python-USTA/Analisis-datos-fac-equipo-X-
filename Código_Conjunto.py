# ================================================================
# Script: Codigo_conjunto.py
# Autor: 
- Angela Rico: Análisis de demografía básica.  
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
# ANALISIS DEMOGRÁFICO
# ==============================================================

#ANÁLISIS DEMOGRÁFICO FAC 2024
# =============================
# Análisis estadístico especializado del personal de la Fuerza Aérea Colombiana


# ==============================================================
# IMPORTACIONES Y CONFIGURACIÓN
# ==============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Configuración de estilo para gráficos
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "axes.titlesize": 16,
    "axes.titleweight": "bold",
    "axes.labelsize": 12,
    "figure.dpi": 100
})

# ==============================================================
# CONSTANTES Y CONFIGURACIÓN
# ==============================================================

# Jerarquía militar - Orden correcto según doctrina
OFICIALES_ORDER_LOW = ['st', 'te', 'ct', 'my', 'tc', 'cr', 'bg', 'mg', 'gr']
SUBOF_ORDER_LOW = ['at', 't4', 't3', 't2', 't1', 'ts', 'tj', 'tjc']

# Etiquetas legibles para gráficos
OFICIALES_LABELS = {
    'st': 'ST — Subteniente',
    'te': 'TE — Teniente', 
    'ct': 'CT — Capitán',
    'my': 'MY — Mayor',
    'tc': 'TC — Teniente Coronel',
    'cr': 'CR — Coronel',
    'bg': 'BG — Brigadier General',
    'mg': 'MG — Mayor General',
    'gr': 'GR — General'
}

SUBOF_LABELS = {
    'at': 'AT — Aspirante Técnico',
    't4': 'T4 — Subof. Técnico Cuarto',
    't3': 'T3 — Subof. Técnico Tercero',
    't2': 'T2 — Subof. Técnico Segundo',
    't1': 'T1 — Subof. Técnico Primero',
    'ts': 'TS — Técnico Subjefe',
    'tj': 'TJ — Técnico Jefe',
    'tjc': 'TJC — Técnico Jefe de Comando'
}


# Grupos etarios estándar
GRUPOS_ETARIOS = ['18-25', '26-35', '36-45', '46-55', '56+']

# Archivo de datos
ARCHIVO_DATOS = '../JEFAB_2024_corregido.xlsx'

# ==============================================================
# CLASE PRINCIPAL: ANALIZADOR DEMOGRÁFICO
# ==============================================================

class AnalizadorDemograficoFAC:
    """
    Clase principal para realizar análisis demográfico del personal FAC
    """
    
    def __init__(self, archivo_path: str = ARCHIVO_DATOS):
        """
        Inicializa el analizador con los datos
        
        Args:
            archivo_path (str): Ruta al archivo Excel con los datos
        """
        self.archivo_path = archivo_path
        self.df = None
        self.resultados = {}
        
    def cargar_datos(self):
        """Carga y preprocesa los datos desde Excel"""
        print("Cargando datos del archivo...")
        try:
            self.df = pd.read_excel(self.archivo_path)
            print(f"Archivo cargado exitosamente: {self.df.shape[0]:,} registros, {self.df.shape[1]} columnas")
            self._preprocesar_datos()
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            raise
            
    def _preprocesar_datos(self):
        """Limpia y normaliza los datos"""
        print("Preprocesando datos...")
        
        # Limpiar espacios en variables categóricas
        categoricas = ['SEXO', 'CATEGORIA', 'GRADO', 'ESTADO_CIVIL', 'NIVEL_EDUCATIVO', 'UNIDAD']
        for col in categoricas:
            if col in self.df.columns and pd.api.types.is_object_dtype(self.df[col]):
                self.df[col] = self.df[col].astype(str).str.strip()
        
        # Crear versiones normalizadas
        self._crear_columnas_normalizadas()
        
        # Asegurar que EDAD2 sea numérico
        if 'EDAD2' in self.df.columns:
            self.df['EDAD2'] = pd.to_numeric(self.df['EDAD2'], errors='coerce')
            
        # Crear grupos etarios
        self._crear_grupos_etarios()
        
        print("Preprocesamiento completado")
        
    def _crear_columnas_normalizadas(self):
        """Crea versiones normalizadas de las columnas para análisis consistente"""
        normalizaciones = {
            'SEXO': 'SEXO_UP',
            'CATEGORIA': 'CATEGORIA_UP', 
            'GRADO': 'GRADO_LOW',
            'NIVEL_EDUCATIVO': 'NIVEL_EDU_LOW',
            'ESTADO_CIVIL': 'ESTADO_CIVIL_UP'
        }
        
        for col_orig, col_norm in normalizaciones.items():
            if col_orig in self.df.columns:
                if col_norm.endswith('_UP'):
                    self.df[col_norm] = self._normalizar_upper(self.df[col_orig])
                else:
                    self.df[col_norm] = self._normalizar_lower(self.df[col_orig])
    
    def _normalizar_upper(self, serie: pd.Series) -> pd.Series:
        """Normaliza serie a mayúsculas sin acentos"""
        return (serie.astype(str)
                .str.normalize('NFKD')
                .str.encode('ascii', 'ignore')
                .str.decode('utf-8')
                .str.upper()
                .str.strip())
    
    def _normalizar_lower(self, serie: pd.Series) -> pd.Series:
        """Normaliza serie a minúsculas sin acentos"""
        return (serie.astype(str)
                .str.normalize('NFKD')
                .str.encode('ascii', 'ignore')
                .str.decode('utf-8')
                .str.lower()
                .str.strip())
    
    def _crear_grupos_etarios(self):
        """Crea grupos etarios estándar"""
        if 'EDAD2' in self.df.columns:

            self.df['GRUPO_ETARIO'] = pd.cut(
                self.df['EDAD2'],
                bins=[0, 25, 35, 45, 55, np.inf],
                labels=GRUPOS_ETARIOS,
                right=True, 
                include_lowest=True
            )
    
    def mostrar_info_general(self):
        """Muestra información general del dataset"""
        print("\n" + "="*60)
        print("INFORMACIÓN GENERAL DEL DATASET")
        print("="*60)
        
        print(f"Total de registros: {len(self.df):,}")
        print(f"Total de columnas: {len(self.df.columns)}")
        
        # Estadísticas básicas de edad
        if 'EDAD2' in self.df.columns:
            edad_stats = self.df['EDAD2'].describe()
            print(f"\nEstadísticas de edad:")
            print(f"   - Promedio: {edad_stats['mean']:.1f} años")
            print(f"   - Mediana: {edad_stats['50%']:.1f} años")
            print(f"   - Rango: {edad_stats['min']:.0f} - {edad_stats['max']:.0f} años")
        
        # Distribución por categoría
        if 'CATEGORIA_UP' in self.df.columns:
            print(f"\nDistribución por categoría:")
            for cat, count in self.df['CATEGORIA_UP'].value_counts().items():
                pct = (count / len(self.df)) * 100
                print(f"   - {cat}: {count:,} ({pct:.1f}%)")

# ==============================================================
# MÓDULO: ANÁLISIS ESTADÍSTICO DEMOGRÁFICO
# ==============================================================

class AnalisisEstadisticoFAC:
    """
    Módulo especializado en análisis estadísticos demográficos
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.resultados = {}
    
    def calcular_indices_demograficos(self):
        """Calcula índices demográficos especializados"""
        print("\nCALCULANDO ÍNDICES DEMOGRÁFICOS...")
        
        # Índice de masculinidad
        hombres = (self.df['SEXO_UP'] == 'HOMBRE').sum() if 'SEXO_UP' in self.df else 0
        mujeres = (self.df['SEXO_UP'] == 'MUJER').sum() if 'SEXO_UP' in self.df else 0
        indice_masculinidad = np.nan if mujeres == 0 else (hombres/mujeres)*100
        
        # Índice de dependencia demográfica
        if 'EDAD2' in self.df.columns:
            edad = self.df['EDAD2'].dropna()
            jovenes = (edad < 30).sum()
            adultos_mayores = (edad >= 50).sum()
            poblacion_activa = ((edad >= 30) & (edad < 50)).sum()
            indice_dependencia = np.nan if poblacion_activa == 0 else ((jovenes + adultos_mayores)/poblacion_activa)*100
            
            # Coeficiente de variación etaria
            cv_edad = np.nan
            if len(edad) > 1 and float(edad.mean()) != 0.0:
                cv_edad = (edad.std(ddof=1) / edad.mean()) * 100
        else:
            indice_dependencia = np.nan
            cv_edad = np.nan
        
        # Mediana de edad por categoría
        edad_mediana_categoria = pd.Series(dtype=float)
        if 'CATEGORIA_UP' in self.df.columns and 'EDAD2' in self.df.columns:
            edad_mediana_categoria = self.df.groupby('CATEGORIA_UP', dropna=False)['EDAD2'].median()
        
        # Almacenar resultados
        self.resultados['indices'] = {
            'indice_masculinidad': indice_masculinidad,
            'indice_dependencia': indice_dependencia,
            'cv_edad': cv_edad,
            'edad_mediana_oficial': edad_mediana_categoria.get('OFICIAL', np.nan),
            'edad_mediana_suboficial': edad_mediana_categoria.get('SUBOFICIAL', np.nan),
            'edad_mediana_civil': edad_mediana_categoria.get('CIVIL', np.nan)
        }
        
        self._imprimir_indices()
        return self.resultados['indices']
    
    def analizar_estructura_etaria(self):
        """Analiza la estructura etaria de la población"""
        if 'GRUPO_ETARIO' not in self.df.columns:
            print("No se pueden analizar grupos etarios - columna no disponible")
            return None, None
            
        distribucion_etaria = self.df['GRUPO_ETARIO'].value_counts().reindex(GRUPOS_ETARIOS, fill_value=0)
        porcentajes_etaria = (distribucion_etaria / len(self.df) * 100).round(1)
        
        grupo_modal = distribucion_etaria.idxmax() if distribucion_etaria.sum() > 0 else np.nan
        
        print(f"\nESTRUCTURA ETARIA:")
        for grupo in GRUPOS_ETARIOS:
            count = int(distribucion_etaria[grupo])
            pct = porcentajes_etaria[grupo]
            print(f"   - {grupo} años: {count:4d} personas ({pct:4.1f}%)")
        
        if pd.notna(grupo_modal):
            print(f"\nGrupo etario modal: {grupo_modal} ({porcentajes_etaria[grupo_modal]:.1f}%)")
        
        self.resultados['estructura_etaria'] = {
            'distribucion': distribucion_etaria,
            'porcentajes': porcentajes_etaria,
            'grupo_modal': grupo_modal
        }
        
        return distribucion_etaria, grupo_modal
    
    def analizar_asociaciones_demograficas(self):
        """Analiza asociaciones entre variables demográficas usando Chi-cuadrado"""
        print(f"\nANÁLISIS DE ASOCIACIONES DEMOGRÁFICAS:")
        
        # Pares de variables para analizar
        asociaciones = []
        variables_disponibles = set(self.df.columns)
        
        pares_interes = [
            ('SEXO_UP', 'CATEGORIA_UP'),
            ('GRUPO_ETARIO', 'CATEGORIA_UP'),
            ('ESTADO_CIVIL_UP', 'SEXO_UP'),
            ('NIVEL_EDU_LOW', 'CATEGORIA_UP')
        ]
        
        # Filtrar solo pares con ambas variables disponibles
        asociaciones = [(v1, v2) for v1, v2 in pares_interes if v1 in variables_disponibles and v2 in variables_disponibles]
        
        resultados_asociaciones = {}
        
        for var1, var2 in asociaciones:
            resultado = self._test_chi_cuadrado(var1, var2)
            if resultado:
                resultados_asociaciones[f"{var1}×{var2}"] = resultado
        
        self.resultados['asociaciones'] = resultados_asociaciones
        return resultados_asociaciones
    
    def _test_chi_cuadrado(self, var1: str, var2: str):
        """Ejecuta test de Chi-cuadrado entre dos variables"""
        tabla = pd.crosstab(self.df[var1], self.df[var2])
        
        if tabla.size == 0 or tabla.shape[0] < 2 or tabla.shape[1] < 2:
            return None
            
        chi2, p_val, dof, expected = chi2_contingency(tabla)
        n = tabla.values.sum()
        cramer_v = np.sqrt(chi2 / (n * (min(tabla.shape) - 1)))
        
        # Interpretación
        significancia = self._interpretar_significancia(p_val)
        fuerza_asociacion = self._interpretar_cramer_v(cramer_v)
        
        print(f"    {var1} × {var2}:")
        print(f"      Chi² = {chi2:.2f}, p = {p_val:.4f} ({significancia})")
        print(f"      V de Cramér = {cramer_v:.3f} (Asociación {fuerza_asociacion})")
        
        return {
            'chi2': chi2,
            'p_val': p_val,
            'cramer_v': cramer_v,
            'significancia': significancia,
            'fuerza': fuerza_asociacion
        }
    
    def analizar_diferencias_subgrupos(self):
        """Analiza diferencias de edad entre subgrupos"""
        print(f"\nDIFERENCIAS DE EDAD POR SUBGRUPOS:")
        
        resultados = {}
        
        # Test t para diferencias por sexo
        if {'SEXO_UP', 'EDAD2'}.issubset(self.df.columns):
            resultado_t = self._test_t_sexo()
            resultados['test_t_sexo'] = resultado_t
        
        # ANOVA por categoría
        if {'CATEGORIA_UP', 'EDAD2'}.issubset(self.df.columns):
            resultado_anova = self._test_anova_categoria()
            resultados['anova_categoria'] = resultado_anova
        
        self.resultados['diferencias_subgrupos'] = resultados
        return resultados
    
    def _test_t_sexo(self):
        """Test t de Student para diferencias de edad entre sexos"""
        edad_h = self.df.loc[self.df['SEXO_UP'] == 'HOMBRE', 'EDAD2'].dropna()
        edad_m = self.df.loc[self.df['SEXO_UP'] == 'MUJER', 'EDAD2'].dropna()
        
        if len(edad_h) <= 1 or len(edad_m) <= 1:
            print("   No hay datos suficientes para test t")
            return None
        
        t_stat, p_val = stats.ttest_ind(edad_h, edad_m, equal_var=False, nan_policy='omit')
        diferencia_media = edad_h.mean() - edad_m.mean()
        
        significancia = self._interpretar_significancia(p_val)
        
        print(f"    Diferencia H-M en edad promedio: {diferencia_media:.1f} años")
        print(f"    Test t: t = {t_stat:.3f}, p = {p_val:.4f} ({significancia})")
        
        return {
            't_stat': t_stat,
            'p_val': p_val,
            'diferencia_media': diferencia_media,
            'significancia': significancia
        }
    
    def _test_anova_categoria(self):
        """ANOVA para diferencias de edad entre categorías"""
        grupos = [g.dropna() for _, g in self.df.groupby('CATEGORIA_UP')['EDAD2']]
        grupos = [g for g in grupos if len(g) > 1]
        
        if len(grupos) < 2:
            print("   No hay datos suficientes para ANOVA")
            return None
        
        f_stat, p_val = stats.f_oneway(*grupos)
        significancia = self._interpretar_significancia(p_val)
        
        print(f"   Variación de edad entre categorías:")
        print(f"   ANOVA: F = {f_stat:.3f}, p = {p_val:.4f} ({significancia})")
        
        return {
            'f_stat': f_stat,
            'p_val': p_val,
            'significancia': significancia
        }
    
    def _interpretar_significancia(self, p_val: float) -> str:
        """Interpreta el valor p"""
        if p_val < 0.01:
            return "Muy significativa"
        elif p_val < 0.05:
            return "Significativa"
        else:
            return "No significativa"
    
    def _interpretar_cramer_v(self, cramer_v: float) -> str:
        """Interpreta el valor de V de Cramér"""
        if cramer_v > 0.3:
            return "Fuerte"
        elif cramer_v > 0.1:
            return "Moderada"
        else:
            return "Débil"
    
    def _imprimir_indices(self):
        """Imprime los índices demográficos calculados"""
        indices = self.resultados['indices']
        
        print(f"\nÍNDICES DEMOGRÁFICOS ESPECIALIZADOS:")
        print(f"   - Índice de Masculinidad: {self._format_numero(indices['indice_masculinidad'], 1)} hombres por cada 100 mujeres")
        print(f"   - Índice de Dependencia: {self._format_numero(indices['indice_dependencia'], 1)}%")
        print(f"   - Coeficiente de Variación Etaria: {self._format_numero(indices['cv_edad'], 1)}%")
        print(f"   - Edad mediana OFICIAL: {self._format_numero(indices['edad_mediana_oficial'], 1)} años")
        print(f"   - Edad mediana SUBOFICIAL: {self._format_numero(indices['edad_mediana_suboficial'], 1)} años")
        print(f"   - Edad mediana CIVIL: {self._format_numero(indices['edad_mediana_civil'], 1)} años")
    
    def _format_numero(self, x, decimales=1, default="N/A"):
        """Formatea números de forma segura"""
        try:
            if x is None or (isinstance(x, (float, int)) and not np.isfinite(x)):
                return default
            return f"{float(x):.{decimales}f}"
        except:
            return default

# ==============================================================
# MÓDULO: GENERADOR DE GRÁFICOS
# ==============================================================

class GeneradorGraficosFAC:
    """
    Módulo especializado en generación de gráficos demográficos
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.figuras_creadas = []
    
    def generar_graficos_univariados(self):
        """Genera gráficos de análisis univariado"""
        print("\nGENERANDO GRÁFICOS UNIVARIADOS...")
        
        # 1. Distribución de edad
        self._grafico_edad_distribucion()
        
        # 2. Distribución por categoría
        self._grafico_categoria_barras()
        
        # 3. Distribución por grado
        self._grafico_grado_barras()
        
        # 4. Estado civil
        self._grafico_estado_civil()
        
        # 5. Nivel educativo
        self._grafico_nivel_educativo()
        
        print(f"{len(self.figuras_creadas)} gráficos univariados generados")
    
    def generar_graficos_bivariados(self):
        """Genera gráficos de análisis bivariado"""
        print("\nGENERANDO GRÁFICOS BIVARIADOS...")
        
        # 1. Pirámide etaria
        self._grafico_piramide_etaria()
        
        # 2. Edad por categoría
        self._grafico_edad_categoria()
        
        # 3. Sexo por categoría
        self._grafico_sexo_categoria()
        
        # 4. Nivel educativo por categoría
        self._grafico_educacion_categoria()
        
        print(f"Gráficos bivariados generados")
    
    def generar_graficos_jerarquicos(self):
        """Genera gráficos específicos por jerarquía militar"""
        print("\nGENERANDO GRÁFICOS JERÁRQUICOS...")
        
        # Gráficos para oficiales
        self._graficos_oficiales()
        
        # Gráficos para suboficiales
        self._graficos_suboficiales()
        
        print("Gráficos jerárquicos generados")
    
    def _grafico_edad_distribucion(self):
        """Histograma de distribución de edad"""
        if 'EDAD2' not in self.df.columns:
            return
            
        plt.figure(figsize=(12, 6))
        edad_clean = self.df['EDAD2'].dropna()
        
        sns.histplot(edad_clean, bins=25, kde=True, alpha=0.7)
        plt.title('Distribución de Edad del Personal FAC', fontsize=16, fontweight='bold')
        plt.xlabel('Edad (años)')
        plt.ylabel('Frecuencia')
        
        # Agregar estadísticas
        media = edad_clean.mean()
        mediana = edad_clean.median()
        plt.axvline(media, color='red', linestyle='--', alpha=0.7, label=f'Media: {media:.1f}')
        plt.axvline(mediana, color='orange', linestyle='--', alpha=0.7, label=f'Mediana: {mediana:.1f}')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('01_distribucion_edad.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('01_distribucion_edad.png')
    
    def _grafico_categoria_barras(self):
        """Gráfico de barras por categoría"""
        if 'CATEGORIA' not in self.df.columns:
            return
            
        plt.figure(figsize=(10, 6))
        orden_cat = self.df['CATEGORIA'].value_counts().index.tolist()
        
        ax = sns.countplot(y='CATEGORIA', data=self.df, order=orden_cat, color='steelblue')
        self._agregar_valores_barras(ax, orientacion="horizontal")
        
        plt.title('Distribución por Categoría Militar')
        plt.xlabel('Cantidad')
        plt.ylabel('Categoría')
        
        plt.tight_layout()
        plt.savefig('02_distribucion_categoria.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('02_distribucion_categoria.png')
    
    def _grafico_grado_barras(self):
        """Gráfico de barras por grado (excluyendo 'no responde')"""
        if not {'GRADO', 'GRADO_LOW'}.issubset(self.df.columns):
            return
            
        df_grado = self.df[self.df['GRADO_LOW'] != "no responde"].copy()
        if df_grado.empty:
            return
            
        plt.figure(figsize=(12, 10))
        orden_grado = df_grado['GRADO'].value_counts().index.tolist()
        
        ax = sns.countplot(y='GRADO', data=df_grado, order=orden_grado, color='darkgreen')
        self._agregar_valores_barras(ax, orientacion="horizontal")
        
        plt.title('Distribución por Grado Militar')
        plt.xlabel('Cantidad')
        plt.ylabel('Grado')
        
        plt.tight_layout()
        plt.savefig('03_distribucion_grado.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('03_distribucion_grado.png')
    
    def _grafico_estado_civil(self):
        """Gráfico de barras por estado civil"""
        if 'ESTADO_CIVIL' not in self.df.columns:
            return
            
        plt.figure(figsize=(10, 6))
        orden_ec = self.df['ESTADO_CIVIL'].value_counts().index.tolist()
        
        ax = sns.countplot(y='ESTADO_CIVIL', data=self.df, order=orden_ec, color='coral')
        self._agregar_valores_barras(ax, orientacion="horizontal")
        
        plt.title('Distribución por Estado Civil')
        plt.xlabel('Cantidad')
        plt.ylabel('Estado Civil')
        
        plt.tight_layout()
        plt.savefig('04_distribucion_estado_civil.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('04_distribucion_estado_civil.png')
    
    def _grafico_nivel_educativo(self):
        """Gráfico de barras por nivel educativo"""
        if 'NIVEL_EDUCATIVO' not in self.df.columns:
            return
            
        plt.figure(figsize=(12, 8))
        orden_ne = self.df['NIVEL_EDUCATIVO'].value_counts().index.tolist()
        
        ax = sns.countplot(y='NIVEL_EDUCATIVO', data=self.df, order=orden_ne, color='purple')
        self._agregar_valores_barras(ax, orientacion="horizontal")
        
        plt.title('Distribución por Nivel Educativo')
        plt.xlabel('Cantidad')
        plt.ylabel('Nivel Educativo')
        
        plt.tight_layout()
        plt.savefig('05_distribucion_nivel_educativo.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('05_distribucion_nivel_educativo.png')
    
    def _grafico_piramide_etaria(self):
        """Crea pirámide etaria por sexo y grupos etarios"""
        if not {'GRUPO_ETARIO', 'SEXO_UP'}.issubset(self.df.columns):
            return
            
        plt.figure(figsize=(12, 8))
        
        # Crear tabla cruzada
        tabla = self.df.groupby(['GRUPO_ETARIO', 'SEXO_UP'], observed=False).size().unstack(fill_value=0)
        tabla = tabla.reindex(index=GRUPOS_ETARIOS, fill_value=0)
        tabla_pct = (tabla.div(len(self.df)) * 100)
        
        # Obtener datos por sexo
        hombres = tabla_pct['HOMBRE'] if 'HOMBRE' in tabla_pct.columns else pd.Series(0, index=GRUPOS_ETARIOS)
        mujeres = tabla_pct['MUJER'] if 'MUJER' in tabla_pct.columns else pd.Series(0, index=GRUPOS_ETARIOS)
        
        # Crear pirámide
        y_pos = np.arange(len(GRUPOS_ETARIOS))
        plt.barh(y_pos, -hombres.values, align='center', alpha=0.8, label='Hombres', color='steelblue')
        plt.barh(y_pos, mujeres.values, align='center', alpha=0.8, label='Mujeres', color='pink')
        
        plt.yticks(y_pos, GRUPOS_ETARIOS)
        plt.xlabel('Porcentaje de población (%)')
        plt.ylabel('Grupos etarios')
        plt.title('Pirámide Etaria del Personal FAC 2024', fontsize=16, fontweight='bold')
        plt.legend()
        plt.axvline(0, color='black', linewidth=0.8)
        
        # Convertir etiquetas negativas a positivas para mejor lectura
        ax = plt.gca()
        ticks = ax.get_xticks()
        ax.set_xticks(ticks)
        ax.set_xticklabels([f'{abs(x):.1f}' for x in ticks])
        
        plt.tight_layout()
        plt.savefig('06_piramide_etaria.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('06_piramide_etaria.png')
    
    def _grafico_edad_categoria(self):
        """Boxplot de edad por categoría"""
        if not {'CATEGORIA', 'EDAD2'}.issubset(self.df.columns):
            return
            
        plt.figure(figsize=(10, 7))
        sns.boxplot(x='CATEGORIA', y='EDAD2', data=self.df, color='lightblue', showfliers=False)
        plt.title('Distribución de Edad por Categoría Militar', fontsize=16, fontweight='bold')
        plt.xlabel('Categoría')
        plt.ylabel('Edad (años)')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('07_edad_por_categoria.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('07_edad_por_categoria.png')
    
    def _grafico_sexo_categoria(self):
        """Heatmap de sexo por categoría"""
        if not {'SEXO_UP', 'CATEGORIA_UP'}.issubset(self.df.columns):
            return
            
        plt.figure(figsize=(10, 6))
        tabla = pd.crosstab(self.df['SEXO_UP'], self.df['CATEGORIA_UP'])
        tabla_pct = (tabla / tabla.sum(axis=0)).fillna(0) * 100
        
        sns.heatmap(tabla_pct.round(1), annot=True, fmt='.1f', cmap='Blues',
                   linewidths=0.5, cbar_kws={'label': '% dentro de categoría'})
        plt.title('Distribución de Sexo por Categoría (%)', fontsize=16, fontweight='bold')
        plt.xlabel('Categoría')
        plt.ylabel('Sexo')
        
        plt.tight_layout()
        plt.savefig('08_sexo_por_categoria.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('08_sexo_por_categoria.png')
    
    def _grafico_educacion_categoria(self):
        """Heatmap de nivel educativo por categoría"""
        if not {'NIVEL_EDU_LOW', 'CATEGORIA_UP'}.issubset(self.df.columns):
            return
            
        plt.figure(figsize=(12, 8))
        tabla = pd.crosstab(self.df['NIVEL_EDU_LOW'], self.df['CATEGORIA_UP'])
        tabla_pct = (tabla / tabla.sum(axis=0)).fillna(0) * 100
        
        sns.heatmap(tabla_pct.round(1), annot=True, fmt='.1f', cmap='Greens',
                   linewidths=0.5, cbar_kws={'label': '% dentro de categoría'})
        plt.title('Distribución de Nivel Educativo por Categoría (%)', fontsize=16, fontweight='bold')
        plt.xlabel('Categoría')
        plt.ylabel('Nivel Educativo')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig('09_educacion_por_categoria.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append('09_educacion_por_categoria.png')
    
    def _graficos_oficiales(self):
        """Genera gráficos específicos para oficiales"""
        if not self._tiene_datos_jerarquicos('OFICIAL', OFICIALES_ORDER_LOW):
            return
            
        df_oficiales = self.df[(self.df['CATEGORIA_UP'] == 'OFICIAL') & 
                              (self.df['GRADO_LOW'].isin(OFICIALES_ORDER_LOW))].copy()
        
        # Solo gráfico de distribución por grado
        self._grafico_distribucion_grado(df_oficiales, OFICIALES_ORDER_LOW, OFICIALES_LABELS, 
                                        'oficiales', 'Oficiales')
    
    def _graficos_suboficiales(self):
        """Genera gráficos específicos para suboficiales"""
        if not self._tiene_datos_jerarquicos('SUBOFICIAL', SUBOF_ORDER_LOW):
            return
            
        df_suboficiales = self.df[(self.df['CATEGORIA_UP'] == 'SUBOFICIAL') & 
                                 (self.df['GRADO_LOW'].isin(SUBOF_ORDER_LOW))].copy()
        
        # Solo gráfico de distribución por grado
        self._grafico_distribucion_grado(df_suboficiales, SUBOF_ORDER_LOW, SUBOF_LABELS,
                                        'suboficiales', 'Suboficiales')
    
    def _grafico_distribucion_grado(self, df_sub, order_low, labels_map, categoria, titulo_cat):
        """Crea gráfico de barras bivariado por grado y sexo"""
        if df_sub.empty or not {'GRADO_LOW', 'SEXO_UP'}.issubset(df_sub.columns):
            return
            
        orden_jerarquico = self._construir_orden_jerarquico(df_sub, order_low)
        if not orden_jerarquico:
            return
        
        # Crear tabla cruzada de grado por sexo
        tabla = pd.crosstab(df_sub['GRADO_LOW'], df_sub['SEXO_UP'])
        tabla = tabla.loc[[g for g in orden_jerarquico if g in tabla.index]]
        
        if tabla.empty or tabla.sum().sum() == 0:
            return
        
        # Cambiar índices a etiquetas legibles
        tabla.index = [labels_map.get(g, g.upper()) for g in tabla.index]
        
        # Reordenar columnas para que aparezca primero HOMBRE, luego MUJER
        columnas_ordenadas = []
        if 'HOMBRE' in tabla.columns:
            columnas_ordenadas.append('HOMBRE')
        if 'MUJER' in tabla.columns:
            columnas_ordenadas.append('MUJER')
        # Agregar otras columnas si existen
        for col in tabla.columns:
            if col not in columnas_ordenadas:
                columnas_ordenadas.append(col)
        
        tabla = tabla[columnas_ordenadas]
        
        # --- CORRECCIÓN: crear fig/ax y pasar ax=ax al plot para evitar figuras en blanco ---
        fig, ax = plt.subplots(figsize=(12, max(6, 0.4 * len(tabla))))
        ax = tabla.plot(kind='barh', stacked=False, width=0.8, 
                        color=['steelblue', 'pink'][:len(tabla.columns)], ax=ax)
        # ------------------------------------------------------------------------------------
        
        # Agregar valores a las barras
        for container in ax.containers:
            ax.bar_label(container, fmt='%d', label_type='edge', padding=3)
        
        plt.title(f'Distribución por Grado y Sexo ({titulo_cat})', fontsize=16, fontweight='bold')
        plt.xlabel('Cantidad')
        plt.ylabel(f'Grado ({titulo_cat})')
        plt.legend(title='Sexo', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        plt.savefig(f'10_{categoria}_distribucion_grado_sexo.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append(f'10_{categoria}_distribucion_grado_sexo.png')
        
    
    def _tiene_datos_jerarquicos(self, categoria, grados_orden):
        """Verifica si hay datos suficientes para análisis jerárquico"""
        if not {'CATEGORIA_UP', 'GRADO_LOW'}.issubset(self.df.columns):
            return False
            
        df_filtrado = self.df[(self.df['CATEGORIA_UP'] == categoria) & 
                             (self.df['GRADO_LOW'].isin(grados_orden))]
        return not df_filtrado.empty
    
    def _construir_orden_jerarquico(self, df_sub, orden_conocido):
        """Construye orden jerárquico basado en los datos presentes"""
        presentes = df_sub['GRADO_LOW'].dropna().unique().tolist()
        ordenado = [g for g in orden_conocido if g in presentes]
        
        # Agregar otros grados por frecuencia
        restantes = [g for g in presentes if g not in ordenado]
        if restantes:
            freq = df_sub['GRADO_LOW'].value_counts().index.tolist()
            ordenado += [g for g in freq if g in restantes]
            
        return ordenado
    
    def _agregar_valores_barras(self, ax, orientacion="vertical"):
        """Agrega valores numéricos a las barras"""
        if orientacion == "vertical":
            for p in ax.patches:
                height = p.get_height()
                if np.isfinite(height):
                    ax.annotate(f'{int(height)}', 
                               (p.get_x() + p.get_width()/2., height),
                               ha='center', va='bottom', fontsize=9)
        else:  # horizontal
            for p in ax.patches:
                width = p.get_width()
                if np.isfinite(width):
                    ax.annotate(f'{int(width)}', 
                               (width, p.get_y() + p.get_height()/2.),
                               ha='left', va='center', fontsize=9)

# ==============================================================
# MÓDULO: GENERADOR DE REPORTES
# ==============================================================

class GeneradorReportes:
    """
    Módulo para generar reportes de análisis demográfico
    """
    
    def __init__(self, analizador, estadistico):
        self.analizador = analizador
        self.estadistico = estadistico
        self.df = analizador.df
    
    def generar_resumen_ejecutivo(self):
        """Genera resumen ejecutivo de hallazgos"""
        print("\n" + "="*70)
        print("RESUMEN EJECUTIVO - ANÁLISIS DEMOGRÁFICO FAC 2024")
        print("="*70)
        
        # Datos básicos de población
        self._seccion_poblacion_general()
        
        # Estructura demográfica
        self._seccion_estructura_demografica()
        
        # Hallazgos estadísticos clave
        self._seccion_hallazgos_estadisticos()
        
        # Recomendaciones
        self._seccion_recomendaciones()
        
        print("="*70)
    
    def generar_respuestas_clave(self):
        """Genera respuestas a preguntas clave del análisis"""
        print("\n" + "="*50)
        print("RESPUESTAS A PREGUNTAS CLAVE")
        print("="*50)
        
        # Pregunta 1: Rango de edad más común
        self._respuesta_rango_edad()
        
        # Pregunta 2: Distribución por género
        self._respuesta_distribucion_genero()
        
        # Pregunta 3: Grado más frecuente
        self._respuesta_grado_frecuente()
        
        # Pregunta 4: Categoría predominante
        self._respuesta_categoria_predominante()
    
    def _seccion_poblacion_general(self):
        """Información general de la población"""
        total = len(self.df)
        
        # Edad promedio y mediana
        edad_stats = self.df['EDAD2'].describe() if 'EDAD2' in self.df.columns else None
        
        print(f"\nPERFIL POBLACIONAL:")
        print(f"   - Total de efectivos: {total:,}")
        
        if edad_stats is not None:
            print(f"   - Edad promedio: {edad_stats['mean']:.1f} años")
            print(f"   - Edad mediana: {edad_stats['50%']:.1f} años")
            print(f"   - Rango etario: {edad_stats['min']:.0f} - {edad_stats['max']:.0f} años")
    
    def _seccion_estructura_demografica(self):
        """Estructura demográfica de la institución"""
        print(f"\nESTRUCTURA DEMOGRÁFICA:")
        
        # Distribución por categoría
        if 'CATEGORIA_UP' in self.df.columns:
            cat_dist = self.df['CATEGORIA_UP'].value_counts()
            for categoria, cantidad in cat_dist.items():
                porcentaje = (cantidad / len(self.df)) * 100
                print(f"   - {categoria}: {cantidad:,} efectivos ({porcentaje:.1f}%)")
        
        # Índices demográficos si están calculados
        if hasattr(self.estadistico, 'resultados') and 'indices' in self.estadistico.resultados:
            indices = self.estadistico.resultados['indices']
            print(f"\nÍNDICES DEMOGRÁFICOS:")
            print(f"   - Índice de Masculinidad: {self._format_safe(indices['indice_masculinidad'])}")
            print(f"   - Índice de Dependencia: {self._format_safe(indices['indice_dependencia'])}%")
    
    def _seccion_hallazgos_estadisticos(self):
        """Hallazgos estadísticos más relevantes"""
        print(f"\nHALLAZGOS ESTADÍSTICOS CLAVE:")
        
        if hasattr(self.estadistico, 'resultados'):
            # Grupo etario modal
            if 'estructura_etaria' in self.estadistico.resultados:
                grupo_modal = self.estadistico.resultados['estructura_etaria'].get('grupo_modal')
                if pd.notna(grupo_modal):
                    print(f"   - Grupo etario predominante: {grupo_modal}")
            
            # Asociaciones significativas
            if 'asociaciones' in self.estadistico.resultados:
                asociaciones = self.estadistico.resultados['asociaciones']
                asociaciones_significativas = [
                    (nombre, datos) for nombre, datos in asociaciones.items() 
                    if datos['p_val'] < 0.05
                ]
                
                if asociaciones_significativas:
                    print(f"   - Asociaciones significativas encontradas:")
                    for nombre, datos in asociaciones_significativas[:3]:  # Top 3
                        print(f"     - {nombre}: V de Cramér = {datos['cramer_v']:.3f}")
            
            # Diferencias por subgrupos
            if 'diferencias_subgrupos' in self.estadistico.resultados:
                diferencias = self.estadistico.resultados['diferencias_subgrupos']
                if 'test_t_sexo' in diferencias and diferencias['test_t_sexo']:
                    test_t = diferencias['test_t_sexo']
                    print(f"   - Diferencia de edad H-M: {test_t['diferencia_media']:.1f} años ({test_t['significancia']})")
    
    def _seccion_recomendaciones(self):
        """Recomendaciones basadas en los hallazgos"""
        print(f"\nRECOMENDACIONES ESTRATÉGICAS:")
        
        # Recomendaciones basadas en estructura etaria
        if hasattr(self.estadistico, 'resultados') and 'estructura_etaria' in self.estadistico.resultados:
            grupo_modal = self.estadistico.resultados['estructura_etaria'].get('grupo_modal')
            if grupo_modal in ['46-55', '56+']:
                print("   - Considerar programas de rejuvenecimiento institucional")
                print("   - Planificar sucesión de liderazgo para los próximos años")
            elif grupo_modal in ['26-35', '36-45']:
                print("   - Aprovechar el bono demográfico actual")
                print("   - Implementar programas de desarrollo profesional")
        
        # Recomendaciones de género
        if 'SEXO_UP' in self.df.columns:
            dist_genero = self.df['SEXO_UP'].value_counts(normalize=True)
            if 'MUJER' in dist_genero and dist_genero['MUJER'] < 0.3:
                print("   - Fortalecer políticas de equidad de género")
                print("   - Revisar barreras para la participación femenina")
    
    def _respuesta_rango_edad(self):
        """Responde sobre el rango de edad más común"""
        if 'EDAD2' not in self.df.columns:
            print("Pregunta 1 - Rango de edad más común: No disponible")
            return
            
        # Crear rangos de 5 años para análisis más granular
        rangos_edad = pd.cut(self.df['EDAD2'].dropna(), bins=range(18, 70, 5))
        rango_modal = rangos_edad.value_counts().idxmax()
        
        print(f"Pregunta 1 - Rango de edad más común: {rango_modal}")
    
    def _respuesta_distribucion_genero(self):
        """Responde sobre la distribución por género"""
        if 'SEXO_UP' not in self.df.columns:
            print("Pregunta 2 - Distribución por género: No disponible")
            return
            
        dist_genero = self.df['SEXO_UP'].value_counts()
        print("Pregunta 2 - Distribución por género:")
        for genero, cantidad in dist_genero.items():
            porcentaje = (cantidad / len(self.df)) * 100
            print(f"   - {genero}: {cantidad:,} ({porcentaje:.1f}%)")
    
    def _respuesta_grado_frecuente(self):
        """Responde sobre el grado más frecuente"""
        if 'GRADO' not in self.df.columns:
            print("Pregunta 3 - Grado más frecuente: No disponible")
            return
            
        # Excluir 'no responde' si existe
        df_grados = self.df.copy()
        if 'GRADO_LOW' in df_grados.columns:
            df_grados = df_grados[df_grados['GRADO_LOW'] != 'no responde']
        
        if not df_grados.empty:
            grado_frecuente = df_grados['GRADO'].mode().iloc[0]
            cantidad = (df_grados['GRADO'] == grado_frecuente).sum()
            print(f"Pregunta 3 - Grado más frecuente: {grado_frecuente} ({cantidad:,} efectivos)")
        else:
            print("Pregunta 3 - Grado más frecuente: No disponible")
    
    def _respuesta_categoria_predominante(self):
        """Responde sobre la categoría predominante"""
        if 'CATEGORIA_UP' not in self.df.columns:
            print("Pregunta 4 - Categoría predominante: No disponible")
            return
            
        categoria_pred = self.df['CATEGORIA_UP'].mode().iloc[0]
        cantidad = (self.df['CATEGORIA_UP'] == categoria_pred).sum()
        porcentaje = (cantidad / len(self.df)) * 100
        
        print(f"Pregunta 4 - Categoría predominante: {categoria_pred} ({cantidad:,} efectivos, {porcentaje:.1f}%)")
    
    def _format_safe(self, valor, decimales=1, default="N/A"):
        """Formatea valores de forma segura"""
        try:
            if valor is None or (isinstance(valor, (float, int)) and not np.isfinite(valor)):
                return default
            return f"{float(valor):.{decimales}f}"
        except:
            return default

# ==============================================================
# FUNCIÓN PRINCIPAL DE EJECUCIÓN
# ==============================================================

def ejecutar_analisis_completo(archivo_path: str = ARCHIVO_DATOS):
    """
    Ejecuta el análisis demográfico completo
    
    Args:
        archivo_path (str): Ruta al archivo de datos Excel
    """
    print("INICIANDO ANÁLISIS DEMOGRÁFICO FAC 2024")
    print("="*60)
    
    try:
        # 1. Inicializar y cargar datos
        analizador = AnalizadorDemograficoFAC(archivo_path)
        analizador.cargar_datos()
        analizador.mostrar_info_general()
        
        # 2. Análisis estadístico
        estadistico = AnalisisEstadisticoFAC(analizador.df)
        estadistico.calcular_indices_demograficos()
        estadistico.analizar_estructura_etaria()
        estadistico.analizar_asociaciones_demograficas()
        estadistico.analizar_diferencias_subgrupos()
        
        # 3. Generación de gráficos
        graficador = GeneradorGraficosFAC(analizador.df)
        graficador.generar_graficos_univariados()
        graficador.generar_graficos_bivariados()
        graficador.generar_graficos_jerarquicos()
        
        # 4. Generación de reportes
        reporteador = GeneradorReportes(analizador, estadistico)
        reporteador.generar_resumen_ejecutivo()
        reporteador.generar_respuestas_clave()
        
        print(f"\nANÁLISIS COMPLETADO EXITOSAMENTE")
        print(f"Gráficos generados: {len(graficador.figuras_creadas)}")
        print(f"Archivos creados en el directorio actual")
        
        return analizador, estadistico, graficador, reporteador
        
    except Exception as e:
        print(f"ERROR EN EL ANÁLISIS: {e}")
        raise

# ==============================================================
# PUNTO DE ENTRADA PRINCIPAL
# ==============================================================

if __name__ == "__main__":
    # Ejecutar análisis completo
    analizador, estadistico, graficador, reporteador = ejecutar_analisis_completo()
    
    print("\nPara ejecutar componentes individuales:")
    print("   - analizador.mostrar_info_general()")
    print("   - estadistico.calcular_indices_demograficos()")
    print("   - graficador.generar_graficos_univariados()")
    print("   - reporteador.generar_resumen_ejecutivo()")

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
