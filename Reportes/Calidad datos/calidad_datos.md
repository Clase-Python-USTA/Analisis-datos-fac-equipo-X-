
# Informe de Calidad de Datos  
**Base de Datos: Fuerza Aérea Colombiana (FAC)**  
**Responsable: Karen Juliana Suárez Cruz_Calidad de datos**  
**Fecha: 29-08/2025**

---

## 1. Introducción
El presente informe corresponde al análisis y depuración de la base de datos de la **Fuerza Aérea Colombiana (FAC)**, específicamente del archivo `JEFAB_2024_corregido.xlsx`.  
El objetivo principal es garantizar la **calidad de la información** para que pueda ser utilizada en posteriores procesos de análisis estadístico, modelamiento y toma de decisiones estratégicas.  

Durante el proceso se detectaron datos faltantes, inconsistencias lógicas entre variables y se aplicaron imputaciones razonadas basadas en reglas de negocio y coherencia interna.

---

## 2. Revisión Inicial de la Base de Datos
- **Tamaño de la base:** 6423 registros y 231 columnas.  
- **Problema principal:** presencia de **valores faltantes (NaN)** en varias columnas críticas.  
- **Reto adicional:** coexistencia de variables redundantes que permitieron establecer reglas de corrección.

---

## 3. Procesos de Limpieza e Imputación Lógica
Se aplicaron reglas específicas para mejorar la consistencia de los datos:

### 3.1. HIJOS vs NUMERO_HIJOS
- Problema detectado: La columna **NUMERO_HIJOS** presentaba valores vacíos, mientras que la columna **HIJOS** registraba `"no"`.  
- Acción: Se imputaron ceros (0) en **NUMERO_HIJOS** cuando el registro indicaba que la persona **no tenía hijos**.  

### 3.2. HIJOS vs HIJOS_EN_HOGAR
- Problema detectado: Casos donde **HIJOS = "no"** y **HIJOS_EN_HOGAR** estaba vacío.  
- Acción: Se imputaron ceros (0) en **HIJOS_EN_HOGAR** para mantener la coherencia.  

### 3.3. MADRE_VIVE vs EDADES
- Problema detectado: En registros donde **MADRE_VIVE = "no"**, las columnas **EDAD_MADRE** y **EDAD_RANGO_MADRE** estaban vacías.  
- Acción: Se imputaron ceros (0) en dichas columnas, pues no aplica registrar la edad de una madre fallecida.  

### 3.4. PADRE_VIVE vs EDADES
- Problema detectado: Situación análoga a la anterior, pero con las variables del padre (**PADRE_VIVE**, **EDAD_PADRE**, **EDAD_RANGO_PADRE**).  
- Acción: Se imputaron ceros (0) en esas columnas cuando **PADRE_VIVE = "no"**.  

---

## 4. Beneficios de las Correcciones
- **Mayor coherencia interna** entre variables relacionadas.  
- **Reducción de datos faltantes** mediante imputación lógica, sin necesidad de eliminar registros.  
- **Consistencia semántica:** ahora los ceros reflejan explícitamente ausencia de hijos o padres fallecidos, en lugar de valores vacíos.  
- **Preparación para análisis posteriores**, garantizando que los modelos estadísticos no se vean afectados por vacíos injustificados.  

---

## 5. Conclusiones
La depuración de la base de datos de la **Fuerza Aérea Colombiana** permitió transformar un conjunto de datos con inconsistencias en una fuente de información más sólida y confiable.  

- Se implementaron reglas de imputación **basadas en lógica y contexto**, no en simples técnicas automáticas.  
- El archivo resultante `JEFAB_2024_corregido.xlsx` constituye una **versión limpia y validada**, lista para análisis avanzados.  
- Este proceso garantiza que la información pueda ser utilizada en **investigaciones estadísticas, planeación estratégica y apoyo a la toma de decisiones** en la FAC.  


