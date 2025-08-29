# Informe de Resultados Obtenidos  

**Base de Datos:** Fuerza Aérea Colombiana (FAC)  
**Responsable:**  
- Ángela Rico: Análisis de demografía básica.  
- Ángela Tatiana Orjuela: Análisis de estructura familiar.  
- Karen Juliana Suárez Cruz: Calidad de datos  
**Fecha:** 29/08/2025  

---

# Calidad de Datos

## 1. ¿Qué columnas tienen más datos faltantes?  

Tras el **re-análisis post-limpieza**, las columnas con mayor número de vacíos son:  

| Columna                                | Datos Faltantes | % |
|----------------------------------------|-----------------|----|
| NUMERO_PERSONAS_APORTE_SOSTENIMIENTO2  | 3928            | 61.16% |
| NUMERO_HABITAN_VIVIENDA2               | 3808            | 59.29% |
| NUMERO_HIJOS                           | 463             | 7.21% |
| HIJOS_EN_HOGAR                         | 446             | 6.94% |
| EDAD_RANGO_PADRE                       | 142             | 2.21% |
| EDAD_PADRE                             | 142             | 2.21% |
| EDAD_RANGO_MADRE                       | 139             | 2.16% |
| EDAD_MADRE                             | 135             | 2.10% |
| EDAD2                                  | 13              | 0.20% |
| EDAD_RANGO                             | 13              | 0.20% |

Es importante resaltar que, en el caso de **NUMERO_HABITAN_VIVIENDA2**, el **96% de los vacíos corresponden a registros donde los participantes habían marcado previamente "No responde" en una columna asociada**. Esto evidencia que los faltantes no son errores de captura, sino consecuencia lógica de la respuesta previa.  

---

## 2. ¿Hay registros duplicados?  

No se encontraron registros duplicados en la base de datos.  
Esto asegura que **cada fila corresponde a un individuo único**, aumentando la confiabilidad del análisis posterior.  

---

## 3. ¿Qué problemas de encoding se detectan?  

Durante la revisión se identificaron inconsistencias en la codificación de caracteres en variables categóricas, por ejemplo:  

- `"TECNOLÃ“GICO"` en lugar de `"TECNOLÓGICO"`.  

Estos errores pueden generar categorías redundantes y afectar los análisis de frecuencia.  
Para solucionarlo se aplicó un proceso de **normalización de texto**, estandarizando acentos y eliminando caracteres especiales.  

---

## Conclusiones  

1. La depuración permitió reducir los vacíos genuinos en variables clave, mejorando la calidad de la base.  
2. Los faltantes detectados en variables como *NUMERO_HABITAN_VIVIENDA2* no son aleatorios, sino coherentes con respuestas previas de “No responde”.  
3. La ausencia de duplicados garantiza que cada registro corresponde a un individuo único.  
4. La corrección de problemas de encoding aumenta la consistencia de las variables categóricas.  

---

---


# Análisis Familiar 

Este proyecto realiza un análisis exploratorio de datos (EDA) centrado en variables sociodemográficas y familiares.  
El objetivo es identificar patrones y relaciones relevantes sobre **estado civil, hijos, convivencia familiar, maltrato intrafamiliar, vivienda propia y relaciones de pareja**, con el fin de comprender mejor el bienestar familiar y las dinámicas familiares dentro de la población estudiada.  
Se incluyen visualizaciones que facilitan la interpretación de los resultados y permiten detectar tendencias y asociaciones clave de manera rápida.

## Estado Civil

### Distribución absoluta y porcentual
| Estado Civil | Frecuencia | Porcentaje |
|--------------|------------|------------|
| Casado       | 3889       | 60.55%     |
| Soltero/a    | 2084       | 32.45%     |
| Divorciado   | 250        | 3.89%      |
| Separado     | 161        | 2.51%      |
| Viudo/a      | 39         | 0.61%      |


- La mayoría de las personas están **casadas (60.55%)** o **solteras/as (32.45%)**.  
- Los estados de **divorciado, separado y viudo/a** son minoritarios.  
- Los **viudos/as** presentan el porcentaje más alto de vivienda propia (47.56%), mientras que los **solteros/as** tienen el porcentaje más bajo (30.22%).

## Hijos

| Tiene Hijos | Frecuencia |
|-------------|------------|
| Sí          | 3669       |
| No          | 2754       |


- La mayoría del personal **tiene hijos (3669 personas, ~57%)**.  
- Tener hijos está asociado a **mayor probabilidad de vivienda propia**, aunque **no implica necesariamente mayor convivencia con la familia**.

## Convivencia Familiar y Maltrato intrafamiliar

![Relación entre Habitar Vivienda Familiar y Maltrato Intrafamiliar](https://github.com/user-attachments/assets/96d24380-3647-45fb-936c-ca44bf9fab31)

- La gran mayoría **no habita con su familia (81.56%)**, y solo un 18.44% convive con ella.  
- El **maltrato intrafamiliar ocurre tanto en quienes habitan como en quienes no habitan con la familia**, aunque la mayoría de los casos está entre quienes no conviven con la familia.

## Relaciones Familiares y de Pareja

![Relación entre Hijos y Tener Pareja Estable](https://github.com/Suarez5479/Analisis-datos-fac-equipo-X-/blob/main/Reportes/Analisis%20familiar/Relacion%20entre%20Hijos%20y%20Tener%20Pareja%20Estable.png?raw=true)

### Porcentajes de HIJOS vs RELACION_PAREJA_ESTABLE

| HIJOS | RELACION_PAREJA_ESTABLE: No (%) | RELACION_PAREJA_ESTABLE: Sí (%) | Total |
|-------|---------------------------------|--------------------------------|-------|
| no    | 41.0                            | 59.0                           | 2754  |
| sí    | 15.0                            | 85.0                           | 3669  |
| All   | 26.1                            | 73.9                           | 6423  |

- Tener hijos está **fuertemente asociado a tener una relación de pareja estable**.  
- La mayoría de las personas **tienen madre viva**, independientemente de tener hijos.  
- Entre quienes **tienen hijos**, hay más personas cuyo **padre ha fallecido** comparado con quienes no tienen hijos.

## Fallecimiento de los Padres

![Relación entre Hijos y si Madre o Padre Vive](https://github.com/Suarez5479/Analisis-datos-fac-equipo-X-/blob/main/Reportes/Analisis%20familiar/Relacion%20entre%20Hijos%20y%20si%20Madre%20o%20Padre%20Vive.png?raw=true)

- La presencia de **madre viva** es alta en todos los grupos, y no se observa una diferencia importante entre quienes tienen o no hijos.  
- En cambio, la presencia de **padre vivo** varía: quienes tienen hijos presentan un número significativamente mayor de padres fallecidos comparado con quienes no tienen hijos.  
- Esto indica que, dentro de la población con hijos, la situación del padre es más diversa y podría influir en la dinámica familiar.

## analisis categoria y maltrato intrafamiliar

![Relación entre categoría y maltrato intrafamiliar](https://github.com/Suarez5479/Analisis-datos-fac-equipo-X-/blob/main/Reportes/Analisis%20familiar/categoria%20y%20maltrato.png?raw=true)


### Porcentajes por categoría

| CATEGORIA   | No (%) | Sí (%) |
|------------|--------|--------|
| civil      | 92.6   | 7.4    |
| oficial    | 96.8   | 3.2    |
| suboficial | 96.3   | 3.7    |


Los casos de maltrato intrafamiliar son mucho más frecuentes en la categoría civil que en las categorías oficial y suboficial .

Las categorías oficiales y suboficiales tienen una baja incidencia de maltrato intrafamiliar en comparación con la categoría civil .

