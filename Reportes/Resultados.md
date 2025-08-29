# Informe de Resultados Obtenidos  

**Base de Datos:** Fuerza Aérea Colombiana (FAC)  
**Responsable:**  
- Ángela Rico: Análisis de demografía básica.  
- Ángela Tatiana Orjuela: Análisis de estructura familiar.  
- Karen Juliana Suárez Cruz: Calidad de datos  
**Fecha:** 29/08/2025  

---

# Calidad de Datos

## 1. ¿Cuál es el porcentaje de datos vacíos en la base de datos?  

El análisis muestra que la base de datos presenta un **59.29% de vacíos**. Sin embargo, es importante precisar que el **96% de estos registros vacíos corresponden a casos en los que los participantes habían seleccionado previamente la opción “No responde” en una columna asociada**, lo que evidencia que no se trata necesariamente de omisiones aleatorias, sino de una consecuencia directa de la lógica de las preguntas.  

---

## 2. ¿Dónde se concentran los datos faltantes?  

La mayor concentración de datos faltantes se encuentra en las variables asociadas a las preguntas condicionales. Es decir, cuando un participante selecciona “No responde” en una pregunta de filtro, automáticamente se generan vacíos en la(s) pregunta(s) siguiente(s) vinculadas a esa condición. Esto indica que los vacíos no siempre corresponden a errores de diligenciamiento, sino al diseño de la encuesta.  

---

## 3. ¿Qué implicaciones tiene la presencia de estos vacíos?  

La alta proporción de vacíos debe interpretarse con cautela. Por un lado, refleja la existencia de saltos lógicos en la encuesta que pueden inducir la ausencia de información. Por otro, puede afectar los análisis posteriores si no se distingue entre **vacíos reales** (omisiones de respuesta) y **vacíos esperados** (derivados de la selección de “No responde”).  

---

## 4. ¿Qué recomendaciones se proponen?  

1. Diferenciar claramente en la base de datos los vacíos que corresponden a **omisiones** de aquellos que son **producto del diseño de la encuesta**.  
2. En análisis posteriores, considerar los “No responde” como una categoría válida y no como un vacío.  
3. Evaluar si es necesario ajustar el diseño de la encuesta para reducir la generación automática de vacíos.  
4. Documentar de manera explícita en los informes el motivo por el cual se generan los vacíos, con el fin de evitar interpretaciones erróneas en análisis futuros.  

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




Los casos de maltrato intrafamiliar son mucho más frecuentes en la categoría civil que en las categorías oficial y suboficial .

Las categorías oficiales y suboficiales tienen una baja incidencia de maltrato intrafamiliar en comparación con la categoría civil .

