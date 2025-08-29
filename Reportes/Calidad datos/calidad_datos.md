
# Informe de Calidad de Datos  
**Base de Datos: Fuerza Aérea Colombiana (FAC)**  
**Responsable: Karen Juliana Suárez Cruz_Calidad de datos**  
**Fecha: 29-08/2025**

---

## 1. Introducción
El presente informe expone de manera detallada el análisis de calidad y depuración de datos efectuado sobre la base de información suministrada por la Fuerza Aérea Colombiana (FAC), específicamente contenida en el archivo JEFAB_2024.xlsx.

El propósito central de este ejercicio fue evaluar el estado inicial de la base de datos, identificar las principales limitaciones en términos de calidad y aplicar procesos de transformación y depuración que permitan garantizar la coherencia, consistencia y confiabilidad de los registros. La calidad de la información constituye un requisito indispensable, dado que esta base de datos será empleada en etapas posteriores de análisis estadístico, construcción de modelos y apoyo a la toma de decisiones estratégicas orientadas a los objetivos institucionales de la FAC.

---

## 2.Diagnóstico inicial de la base de datos

#### 2.1 Datos faltantes

En el análisis exploratorio de la base, se identificaron altos porcentajes de valores nulos en distintas variables. Las diez columnas con mayor afectación se presentan en la siguiente tabla:.


| Columna                                  | Datos Faltantes | %      |
| ---------------------------------------- | --------------- | ------ |
| NUMERO\_PERSONAS\_APORTE\_SOSTENIMIENTO2 | 3928            | 61.16% |
| NUMERO\_HABITAN\_VIVIENDA2               | 3808            | 59.29% |
| NUMERO\_HIJOS                            | 3217            | 50.09% |
| HIJOS\_EN\_HOGAR                         | 3200            | 49.82% |
| EDAD\_RANGO\_PADRE                       | 1939            | 30.19% |
| EDAD\_PADRE                              | 1939            | 30.19% |
| EDAD\_RANGO\_MADRE                       | 889             | 13.84% |
| EDAD\_MADRE                              | 885             | 13.78% |
| EDAD2                                    | 13              | 0.20%  |
| EDAD\_RANGO                              | 13              | 0.20%  |

#### 2.2 Duplicados

No se identificaron registros duplicados, lo cual asegura que la base no presenta redundancias directas en sus observaciones.

#### 2.3 Tipos de datos

En cuanto a los tipos de variables, se observa que la mayor parte corresponde a datos numéricos enteros (153 variables), seguidos por variables categóricas de texto (66) y un menor número de variables numéricas decimales (12). Esta distribución refleja la predominancia de información cuantitativa en la base.

#### 2.4 Problemas de codificación

No se detectaron columnas con errores de codificación en los nombres de las variables. Sin embargo, se identificaron inconsistencias en los valores de texto dentro de algunas categorías, lo que será objeto de depuración en etapas posteriores.



---

## 3. Limpieza de variables categóricas

Durante la depuración de la base se identificaron inconsistencias en las variables categóricas asociadas a cadenas de texto. Estas inconsistencias estaban relacionadas con el uso de acentos, mayúsculas, caracteres especiales y variaciones en la escritura, lo que generaba un aumento artificial del número de categorías.

### Proceso de limpieza

#### Normalización de cadenas
- Conversión de todos los valores a minúsculas.  
- Eliminación de tildes y caracteres extraños producto de errores de codificación.  
- Estandarización de espacios en blanco y símbolos innecesarios.  

#### Unificación de categorías equivalentes
- Se detectaron registros que, aunque distintos en su escritura, correspondían a la misma categoría.  
- Estos se homologaron bajo un valor canónico único, reduciendo la dispersión de categorías y garantizando mayor coherencia.  

### Resultados de la depuración
- Reducción significativa de categorías redundantes.  
- Mayor uniformidad en la clasificación de registros.  
- Preparación de las variables categóricas para análisis posteriores sin sesgos por errores de digitación o codificación.  

---

## 4. Imputaciones lógicas

Se aplicaron reglas de consistencia entre variables relacionadas con el fin de reducir incoherencias internas en los registros.

### Reglas aplicadas

- **HIJOS y NUMERO_HIJOS**  
  - Cuando `HIJOS = "no"` y `NUMERO_HIJOS = NA`, se imputó con **0**.  
  - **2.754 registros corregidos.**

- **HIJOS y HIJOS_EN_HOGAR**  
  - Misma regla anterior.  
  - **2.754 registros corregidos.**

- **MADRE_VIVE y EDAD_MADRE / RANGO_EDAD_MADRE**  
  - Cuando la madre estaba fallecida y la edad no estaba registrada, se imputó con **0**.  
  - **750 registros corregidos.**

- **PADRE_VIVE y EDAD_PADRE / RANGO_EDAD_PADRE**  
  - Mismo criterio aplicado.  
  - **1.797 registros corregidos.**

### Resultados

- Eliminación de gran parte de la incoherencia interna en la base de datos.  
- Variables familiares más consistentes y listas para análisis posteriores.  

---

## 5. Re-análisis post-limpieza

Después de las correcciones, los porcentajes de datos faltantes se redujeron significativamente:

| Columna                              | Datos Faltantes | Porcentaje |
|--------------------------------------|----------------|------------|
| NUMERO_PERSONAS_APORTE_SOSTENIMIENTO2 | 3928           | 61.16%     |
| NUMERO_HABITAN_VIVIENDA2             | 3808           | 59.29%     |
| NUMERO_HIJOS                          | 463            | 7.21%      |
| HIJOS_EN_HOGAR                        | 446            | 6.94%      |
| EDAD_RANGO_PADRE                      | 142            | 2.21%      |
| EDAD_PADRE                            | 142            | 2.21%      |
| EDAD_RANGO_MADRE                      | 139            | 2.16%      |
| EDAD_MADRE                            | 135            | 2.10%      |

En particular, el caso de la columna **NUMERO_PERSONAS_APORTE_SOSTENIMIENTO2** fue el más relevante, pues presenta un nivel de vacíos superior al 61%. Al no existir información complementaria que permitiera reconstruir los datos de manera confiable, la variable perdió valor analítico. Además, en la discusión con el equipo de trabajo se concluyó que esta columna no sería necesaria para los análisis posteriores, por lo que no se optó por ningún proceso de imputación.

Por otro lado, en la columna **NUMERO_HABITAN_VIVIENDA2** el porcentaje de datos faltantes alcanzó el 59%. Aunque en la base se encontraron algunas variables relacionadas (como aquellas que indican si la persona vive con hermanos mediante respuestas binarias de 1 o 0), estas no ofrecían información suficiente para estimar el número real de personas en la vivienda. De hecho, intentar una imputación con base en estas variables generaría inconsistencias y errores metodológicos. A esto se suma que, tras revisar los casos marcados como “no responde”, se evidenció que corresponden al 96% de los vacíos, lo que confirmó la baja confiabilidad de este campo.

En consecuencia, tanto en **NUMERO_PERSONAS_APORTE_SOSTENIMIENTO2** como en **NUMERO_HABITAN_VIVIENDA2** se decidió no aplicar estrategias de imputación. El alto nivel de vacíos, la falta de información auxiliar y el riesgo de introducir sesgos en el análisis justifican esta decisión. Estas variables fueron descartadas en la etapa de preprocesamiento, priorizando la calidad de la información que sí cuenta con una base sólida para su análisis estadístico.

---
## 6. Estadísticas descriptivas 
### 6.1 (variables numéricas)

Entre las variables numéricas, se observa que la edad promedio de los participantes es de 36.7 años, con un rango entre 18 y 69 años, mientras que el número promedio de hijos es bajo (0.94), lo que refleja una población mayoritariamente joven-adulta con pocos dependientes directos. Los indicadores binarios como MADRE_VIVE y PADRE_VIVE muestran que la mayoría de los padres están vivos, pero aún persisten vacíos en la edad de los padres, especialmente en EDAD_MADRE debido a registros faltantes o inconsistentes.



| Variable            | Conteo | Media    | Std Dev  | Mínimo | 25%  | 50%  | 75%  | Máximo |
|--------------------|--------|----------|----------|--------|------|------|------|--------|
| ID                 | 6423   | 3212.0   | 1854.30  | 1      | 1606 | 3212 | 4817 | 6423   |
| EDAD2              | 6410   | 36.72    | 10.12    | 18     | 29   | 35   | 43   | 69     |
| ESTRATO            | 6423   | 2.80     | 0.82     | 1      | 2    | 3    | 3    | 6      |
| MADRE_VIVE_SI      | 6423   | 0.88     | 0.32     | 0      | 1    | 1    | 1    | 1      |
| MADRE_VIVE_NO      | 6423   | 0.12     | 0.32     | 0      | 0    | 0    | 0    | 1      |
| EDAD_MADRE         | 6288   | 55.09    | 72.86    | 0      | 50   | 59   | 67   | 5456   |
| PADRE_VIVE_SI      | 6423   | 0.72     | 0.45     | 0      | 0    | 1    | 1    | 1      |
| PADRE_VIVE_NO      | 6423   | 0.28     | 0.45     | 0      | 0    | 0    | 1    | 1      |
| EDAD_PADRE         | 6281   | 45.33    | 29.99    | 0      | 0    | 58   | 67   | 97     |
| NUMERO_HIJOS       | 5960   | 0.94     | 1.06     | 0      | 0    | 1    | 2    | 5      |
| HIJOS_EN_HOGAR     | 5977   | 0.69     | 0.86     | 0      | 0    | 0    | 1    | 5      |

---

### 6.2 (variables categóricas)

En cuanto a las variables categóricas, la mayor frecuencia se concentra en categorías como suboficial, hombre, tecnológico y casado, lo que indica tendencias claras en la estructura sociodemográfica y educativa de la muestra. La diversidad en unidades, grados y cuerpos muestra la heterogeneidad organizacional, mientras que las categorías binarias como HIJOS o MADRE_VIVE permiten identificar relaciones familiares y de cuidado predominantes.

| Variable                     | Conteo | Categorías Únicas | Categoría Más Frecuente | Frecuencia |
|-------------------------------|--------|-----------------|-------------------------|------------|
| UNIDAD                        | 6423   | 25              | cdo-fac                 | 1021       |
| CATEGORIA                     | 6423   | 3               | suboficial              | 2650       |
| GRADO                         | 6423   | 18              | no responde             | 1929       |
| CUERPO                        | 6423   | 8               | no responde             | 1929       |
| SEXO                          | 6423   | 2               | hombre                  | 4470       |
| GENERO                        | 6423   | 4               | masculino               | 4451       |
| NIVEL_EDUCATIVO               | 6423   | 8               | tecnologico             | 2085       |
| MADRE_VIVE                    | 6423   | 2               | si                      | 5673       |
| PADRE_VIVE                    | 6423   | 2               | si                      | 4626       |
| ESTADO_CIVIL                  | 6423   | 5               | casado                  | 3889       |
| HIJOS                          | 6423   | 2               | si                      | 3669       |

---

### 6.3 Detección de outliers (IQR)

| Variable                        | Total Outliers | % Outliers | Min Outlier | Max Outlier |
|---------------------------------|----------------|------------|-------------|-------------|
| SERV_EDU_NO_CONOCE               | 1572           | 24.47%     | 1           | 1           |
| BENEFICIO_VIVIENDA_FISCAL_SI     | 1547           | 24.09%     | 1           | 1           |
| MIEMB_COMP_VIV_ESPOSO            | 1519           | 23.65%     | 1           | 1           |
| EVENT_SIGN_FAM_CEL_ACAD           | 1505           | 23.43%     | 1           | 1           |
| ACT_FAM_TIEMPO_APREND            | 1491           | 23.21%     | 1           | 1           |
| SERV_EDU_UBICACION               | 1488           | 23.17%     | 1           | 1           |
| PERS_A_CARG_AMBOS_PADRE          | 1453           | 22.62%     | 1           | 1           |
| EVENT_SIGN_FAM_CEL_RELIG         | 1354           | 21.08%     | 1           | 1           |
| PERS_APOYO_FAM                   | 1313           | 20.44%     | 1           | 1           |
| MIEMB_COMP_VIV_HIJOS             | 1270           | 19.77%     | 1           | 1           |


La detección de outliers mediante el rango intercuartílico (IQR) reveló variables con una proporción significativa de valores atípicos, especialmente en indicadores relacionados con servicios educativos, beneficios de vivienda y composición familiar. Por ejemplo:

- **SERV_EDU_NO_CONOCE (24.47%)** y **BENEFICIO_VIVIENDA_FISCAL_SI (24.09%)** muestran que cerca de una cuarta parte de los registros presentan respuestas que difieren notablemente de la mayoría, lo cual puede reflejar casos excepcionales o registros incompletos.  
- **MIEMB_COMP_VIV_ESPOSO (23.65%)** y **MIEMB_COMP_VIV_HIJOS (19.77%)** indican que existen hogares con composiciones familiares fuera de lo esperado según la tendencia central de la muestra.  
- Variables como **EVENT_SIGN_FAM_CEL_ACAD** y **ACT_FAM_TIEMPO_APREND**, con más del 23% de outliers, sugieren heterogeneidad en la participación familiar y el seguimiento académico.

Estos outliers no necesariamente representan errores de captura, sino que reflejan la diversidad real de la población estudiada. Su identificación es clave para:

1. Evaluar si ciertos valores extremos pueden sesgar medidas de tendencia central como la media.  
2. Determinar la necesidad de aplicar transformaciones o análisis robustos que minimicen el impacto de estos casos en los modelos estadísticos.  
3. Comprender mejor los grupos minoritarios dentro de la muestra, que podrían ser relevantes para análisis segmentados o políticas focalizadas.

## 7. Conclusiones

- La base de datos presentaba inicialmente altos niveles de incompletitud, especialmente en variables relacionadas con información familiar y del hogar.

- Mediante imputaciones lógicas y la normalización de texto en variables categóricas, se logró reducir significativamente los datos faltantes y unificar categorías equivalentes, mejorando la coherencia del dataset.

- Persisten variables críticas con más del 50% de información ausente (por ejemplo, `NUMERO_PERSONAS_APORTE_SOSTENIMIENTO2` y `NUMERO_HABITAN_VIVIENDA2`), lo que limita su uso en análisis estadísticos o modelos predictivos.

- Se identificaron outliers extremos en variables de edad, los cuales requieren depuración manual o la aplicación de reglas adicionales de validación antes de análisis posteriores.

- El dataset corregido (`JEFAB_2024_corregido.xlsx`) se encuentra ahora en condiciones más estables, garantizando mayor confiabilidad para análisis exploratorios y estadísticos subsecuentes.




