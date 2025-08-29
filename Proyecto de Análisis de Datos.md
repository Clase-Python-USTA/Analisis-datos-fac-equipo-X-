# Proyecto de Análisis de Datos — JEFAB_2024

  ### 1. Objetivo

El objetivo de este proyecto es analizar la base de datos JEFAB_2024, identificando problemas de calidad de datos, vacíos de información y patrones relevantes en las dimensiones demográficas, familiares y socioeconómicas.
Además, se busca aplicar herramientas de programación en Python y control de versiones con GitHub para trabajar de manera colaborativa en la depuración y análisis de la información.

La base de datos cuenta con 6.423 registros y 231 variables, que abarcan múltiples dimensiones: identificación, ubicación, educación, condiciones familiares, vivienda, salud y características sociodemográficas.

### 2. Descripción de los datos

La base JEFAB_2024 incluye información sobre:

- Identificación y ubicación.
- Condiciones familiares y del hogar.
- Educación y situación laboral.
- Salud y características sociodemográficas.

### 3. Principales hallazgos preliminares
#### 3.1 Completitud y valores faltantes

Se observó un buen nivel de completitud en la información esencial de identificación y clasificación. No obstante, en dimensiones familiares y económicas aparecen vacíos significativos.

#### Top 10 columnas con más datos faltantes

| Nº  | Columna                                | Datos Faltantes | Porcentaje |
|-----|----------------------------------------|-----------------|------------|
| 1   | NUMERO_PERSONAS_APORTE_SOSTENIMIENTO2  | 3928            | 61.16%     |
| 2   | NUMERO_HABITAN_VIVIENDA2               | 3808            | 59.29%     |
| 3   | NUMERO_HIJOS                           | 3217            | 50.09%     |
| 4   | HIJOS_EN_HOGAR                         | 3200            | 49.82%     |
| 5   | EDAD_RANGO_PADRE                       | 1939            | 30.19%     |
| 6   | EDAD_PADRE                             | 1939            | 30.19%     |
| 7   | EDAD_RANGO_MADRE                       | 889             | 13.84%     |
| 8   | EDAD_MADRE                             | 885             | 13.78%     |
| 9   | EDAD2                                  | 13              | 0.20%      |
| 10  | EDAD_RANGO                             | 13              | 0.20%      |

En general, la base combina un alto nivel de completitud en la información esencial con importantes vacíos en aspectos clave para comprender a fondo las condiciones y características de los hogares.

#### 3.2 Inconsistencias de codificación

Se detectaron errores de codificación de caracteres, como el valor “TECNOLÃ“GICO” en lugar de “TECNOLÓGICO”. Estos problemas no eliminan la información, pero sí generan variantes innecesarias que pueden distorsionar los análisis.

#### 3.3 Sesgo en respuestas

En variables sensibles aparecen con frecuencia categorías como “No responde”. Esto puede introducir sesgos en la interpretación, especialmente en temas como sostenimiento económico, número de hijos o condiciones de vivienda.

### 4. Diccionario para la base Fuerza Aeroespacial Colombiana

Uno de los principales retos fue la ausencia de un diccionario oficial de las variables. Para resolverlo, el equipo buscó información complementaria y llegó a consensos sobre el significado e interpretación de las variables dadas en la base de datos.

Un ejemplo fue la variable GRADO, donde las siglas correspondían a rangos militares. Tras la revisión, se establecieron las siguientes equivalencias:

| Sigla | Grado completo             | Categoría  |
| ----- | -------------------------- | ---------- |
| T4    | Suboficial Técnico Cuarto  | Suboficial |
| T3    | Suboficial Técnico Tercero | Suboficial |
| T2    | Suboficial Técnico Segundo | Suboficial |
| T1    | Suboficial Técnico Primero | Suboficial |
| TS    | Técnico Subjefe            | Suboficial |
| TJ    | Técnico Jefe               | Suboficial |
| TJC   | Técnico Jefe de Comando    | Suboficial |
| ST    | Subteniente                | Oficial   |
| TE    | Teniente                   | Oficial   |
| CT    | Capitán                    | Oficial   |
| MY    | Mayor                      | Oficial   |
| TC    | Teniente Coronel           | Oficial   |
| CR    | Coronel                    | Oficial   |
| BG    | Brigadier General          | Oficial   |
| MG    | Mayor General              | Oficial   |
| GR    | General                    | Oficial   |

### 5.Metodología y trabajo en equipo

Este proyecto se desarrolló de manera colaborativa por nuestro equipo de tres estudiantes, quienes nos organizamos en los siguientes roles:

  - Ángela Rico: Análisis de demografía básica.
  - Ángela Tatiana Orjuela: Análisis de estructura familiar.
  - Karen Juliana Suárez Cruz: Calidad de datos

Cada integrante realizó un reporte individual y, posteriormente, se integraron en un informe general con los resultados obtenidos en conjunto y las conclusiones finales. La colaboración se gestionó a través de GitHub, utilizando ramas, commits y pull requests.
