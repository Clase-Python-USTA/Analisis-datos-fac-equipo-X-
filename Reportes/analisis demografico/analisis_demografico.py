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
        plt.savefig(f'11_suboficial_distribucion_grado_sexo.png', dpi=300, bbox_inches='tight')
        self.figuras_creadas.append(f'11_suboficial_distribucion_grado_sexo.png')
    
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

    plt.show()  # Mostrar todos los gráficos generados
