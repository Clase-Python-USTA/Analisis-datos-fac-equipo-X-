# Analisis familiar Fac

Este script realiza un análisis exploratorio de datos (EDA) sobre información relacionada con el bienestar familiar a partir de una base de datos en Excel. El propósito es identificar patrones, relaciones y distribuciones en variables sociodemográficas y familiares, así como generar visualizaciones que faciliten la interpretación de los resultados.

# Funcionalidades principales

## Estado Civil
- Distribución absoluta y porcentual de los diferentes estados civiles.  
- Gráficos de barras y boxplots relacionando estado civil con la edad promedio.  

## Hijos
- Conteo de personal con y sin hijos.  
- Relación entre hijos y convivencia en vivienda familiar.  
- Cruce entre hijos y vivienda propia, con porcentajes y gráficos.  

## Convivencia Familiar y Vivienda
- Análisis de quién habita en vivienda familiar.  
- Relación entre convivencia y maltrato intrafamiliar.  
- Relación entre hijos y vivienda propia.  

## Categoría y Estado Civil
- Cruce de categorías según estado civil con frecuencias absolutas y porcentuales.  
- Visualización en gráficas de barras comparativas.  

## Relaciones Familiares y de Pareja
- Asociación entre tener hijos y tener una relación de pareja estable.  
- Análisis sobre hijos y situación de padres vivos (madre/padre).  

## Visualizaciones
- Gráficos de barras simples, agrupados y apilados.  
- Boxplots de edad según estado civil.  
- Representaciones porcentuales para facilitar comparaciones.  

---

# Tecnologías utilizadas
- **Pandas** → manipulación y análisis de datos.  
- **Matplotlib** → creación de gráficas y visualizaciones.

# Resultados

## Análisis Estado Civil

### Distribución absoluta y porcentual
| Estado Civil | Frecuencia | Porcentaje |
|--------------|------------|------------|
| Casado       | 3889       | 60.55%     |
| Soltero/a    | 2084       | 32.45%     |
| Divorciado   | 250        | 3.89%      |
| Separado     | 161        | 2.51%      |
| Viudo/a      | 39         | 0.61%      |

### Interpretación
- La mayoría de las personas encuestadas se encuentran **casadas (60.55%)**, seguidas por **solteros/as (32.45%)**.  
- Los estados civiles de **divorciado, separado y viudo/a** tienen una participación mucho menor (menos del 7% en total).  

