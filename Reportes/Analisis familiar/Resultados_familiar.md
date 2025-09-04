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

## Análisis de Hijos

### Distribución absoluta
| Tiene Hijos | Frecuencia |
|-------------|------------|
| Sí          | 3669       |
| No          | 2754       |

### Interpretación
- La mayoría del personal encuestado **tiene hijos (3669 personas, ~57%)**.  
- Un **43% no tiene hijos (2754 personas)**, lo que muestra una proporción relativamente equilibrada, aunque predominan quienes sí tienen hijos.  


 ## Análisis de Convivencia Familiar




### Análisis Chi-cuadrado: Asociación entre Tener Hijos y convivencia familiar

**Hipótesis:**

- **H₀ (Hipótesis nula):** No existe asociación entre tener hijos y convivir con la familia. Es decir, las variables **HIJOS** y **HABITA_VIVIENDA_FAMILIAR** son independientes.
- **H₁ (Hipótesis alternativa):** Existe una asociación entre tener hijos y convivir con la familia. Las variables no son independientes.

**Resultado del test:**

- Estadístico Chi-cuadrado: **χ² = 68.58**
- Valor-p: **p < 0.001**

**Conclusión:**

Dado que el valor-p es menor a 0.05, se **rechaza la hipótesis nula**. Por lo tanto, se concluye que existe una **asociación estadísticamente significativa** entre tener hijos y la convivencia familiar.





### Tabla de contingencia (frecuencias absolutas)
| Hijos | No habita con familia | Sí habita con familia | Total |
|-------|------------------------|------------------------|-------|
| No    | 2118                  | 636                    | 2754  |
| Sí    | 3120                  | 549                    | 3669  |
| **Total** | **5238**              | **1185**                | **6423** |

### Tabla de porcentajes por fila
| Hijos | No habita con familia | Sí habita con familia |
|-------|------------------------|------------------------|
| No    | 76.91%                | 23.09%                |
| Sí    | 85.03%                | 14.97%                |

### Interpretación
- Entre quienes **no tienen hijos**, el **23.09% convive con su familia**, frente a un **76.91% que no lo hace**.  
- Entre quienes **sí tienen hijos**, solo el **14.97% habita con su familia**, mientras que la gran mayoría (**85.03%**) no convive con ella.  





## Analisis hijos vivienda propia

###  Análisis Chi-cuadrado: Asociación entre Tener Hijos y Vivienda Propia

**Hipótesis:**

- **H₀ (Hipótesis nula):** No existe asociación entre tener hijos y la tenencia de vivienda propia. Es decir, las variables **HIJOS** y **VIVIENDA_PROPIA** son independientes.
- **H₁ (Hipótesis alternativa):** Existe una asociación entre tener hijos y la tenencia de vivienda propia. Las variables no son independientes.

**Resultado del test:**

- Estadístico Chi-cuadrado: **χ² = 604.73**
- Valor-p: **p < 0.001**

**Conclusión:**

Dado que el valor-p es menor a 0.05, se **rechaza la hipótesis nula**. Por lo tanto, se concluye que existe una **asociación estadísticamente significativa** entre tener hijos y la posesión de vivienda propia.

Este hallazgo sugiere que la decisión o posibilidad de adquirir vivienda puede estar relacionada con la condición de ser padre o madre, lo cual puede tener implicaciones en políticas de vivienda, planificación familiar y desarrollo social.

![Gráfica Hijos vs Vivienda Propia](https://github.com/Suarez5479/Analisis-datos-fac-equipo-X-/blob/main/Reportes/Analisis%20familiar/Relacion%20entre%20Hijos%20y%20Vivienda%20Propia.png?raw=true)



### Interpretación
- Entre quienes **no tienen hijos**, la mayoría no posee vivienda propia (~75%).  
- Más del **55% de quienes tienen hijos sí cuentan con vivienda propia**.  
- Esto indica que **tener hijos está asociado a una mayor probabilidad de adquirir vivienda**.



## Distribución de Categoría por Estado Civil

###  Análisis Chi-cuadrado: Asociación entre Estado Civil y Categoría

**Hipótesis:**

- **H₀ (Hipótesis nula):** No existe asociación entre el estado civil y la categoría laboral. Es decir, las variables **ESTADO_CIVIL** y **CATEGORÍA** son independientes.
- **H₁ (Hipótesis alternativa):** Existe una asociación entre el estado civil y la categoría laboral. Las variables no son independientes.

**Resultado del test:**

- Estadístico Chi-cuadrado: **χ² = 334.94**
- Valor-p: **p < 0.001**

**Conclusión:**

Dado que el valor-p es menor a 0.05, se **rechaza la hipótesis nula**. Se concluye que existe una **asociación estadísticamente significativa** entre el estado civil y la categoría laboral del personal.

Este resultado sugiere que la distribución de las categorías laborales varía según el estado civil, lo que podría reflejar diferencias estructurales o sociales dentro de la organización que merecen mayor análisis.




![categoria por estado civil](https://github.com/Suarez5479/Analisis-datos-fac-equipo-X-/blob/main/Reportes/Analisis%20familiar/Distribucion%20de%20Categoria%20por%20Estado%20Civil.png?raw=true)

- En **casados y divorciados**, predomina la categoría **suboficial**, aunque la categoría civil también tiene un peso importante.  
- En **separados**, la mayoría pertenece a la categoría **civil**, seguida por suboficial.  
- Entre los **viudos/as** predomina ampliamente la categoría **civil (más del 80%)**, mientras que en los **solteros/as** hay mayor equilibrio, destacando **suboficial y oficial**.


## Analisis de estado civil y edad

###  Conclusión del análisis de edad por estado civil 

La prueba de Kruskal-Wallis mostró diferencias estadísticamente significativas en la edad según el estado civil (p < 0.05).  
La prueba post hoc de Dunn (con corrección de Bonferroni) identificó qué grupos presentan diferencias significativas.

####  Edad media por grupo:

| Estado Civil           | Edad media |
|-----------------------|------------|
| Soltero/a             | 30.24      |
| Casado                | 39.71      |
| Divorciado/Separado   | 40.56      |
| Viudo/a               | 47.56      |

#### Comparaciones significativas (Dunn):

| Comparación                    | p-valor  | ¿Significativa? | Interpretación |
|------------------------------|----------|-----------------|----------------|
| Casado vs Soltero/a           | < 0.001  | ✅ Sí           | Solteros/as son significativamente **más jóvenes** que casados |
| Casado vs Viudo/a             | 0.0001   | ✅ Sí           | Viudos/as son significativamente **mayores** que casados |
| Divorciado/Separado vs Soltero/a | < 0.001 | ✅ Sí          | Solteros/as son significativamente **más jóvenes** que divorciados/separados |
| Divorciado/Separado vs Viudo/a   | 0.0041  | ✅ Sí           | Viudos/as son significativamente **mayores** que divorciados/separados |
| Soltero/a vs Viudo/a          | < 0.001  | ✅ Sí           | Viudos/as son significativamente **mayores** que solteros/as |
| Casado vs Divorciado/Separado | 0.115    | ❌ No           | No hay diferencias significativas |

####  Conclusión:

Las edades difieren significativamente entre la mayoría de los grupos de estado civil. En términos generales:

- **Solteros/as** son los más jóvenes.
- **Viudos/as** son los más mayores.
- **Casados** y **divorciados/separados** tienen edades similares entre sí, sin diferencias significativas.

Este patrón es consistente con las etapas de la vida y puede guiar intervenciones enfocadas según el estado civil y edad en bienestar familiar.

## Analisis de maltrato intrafamiliar

![Relación entre Habitar Vivienda Familiar y Maltrato Intrafamiliar](https://github.com/user-attachments/assets/96d24380-3647-45fb-936c-ca44bf9fab31)

**Interpretación:**  
Se observa que la mayoría de las personas no habitan en vivienda familiar y que los casos de maltrato intrafamiliar son menores en comparación con los que no presentan maltrato. Entre quienes sí habitan en vivienda familiar, hay un número menor de casos, pero los casos de maltrato intrafamiliar están presentes. Esto indica que el maltrato intrafamiliar ocurre tanto en quienes habitan como en quienes no habitan en vivienda familiar.




## Relacion entre hijos y tener pareja estable

![Relación entre Hijos y Tener Pareja Estable](https://github.com/Suarez5479/Analisis-datos-fac-equipo-X-/blob/main/Reportes/Analisis%20familiar/Relacion%20entre%20Hijos%20y%20Tener%20Pareja%20Estable.png?raw=true)


**Interpretación:**  
La presencia de hijos está fuertemente asociada a tener una relación de pareja estable. La mayoría de quienes tienen hijos reportan tener pareja estable, mientras que entre quienes no tienen hijos, la distribución entre tener o no pareja estable es más equilibrada.


## Analisis fallecimiento padres


![Relación entre Hijos y si Madre o Padre Vive](https://github.com/Suarez5479/Analisis-datos-fac-equipo-X-/blob/main/Reportes/Analisis%20familiar/Relacion%20entre%20Hijos%20y%20si%20Madre%20o%20Padre%20Vive.png?raw=true)

**Relación entre Hijos y si Madre Vive**

La gran mayoría de personas tienen madre viva, independientemente de si tienen hijos o no. No se observa una diferencia marcada entre tener o no hijos respecto a que la madre viva.

**Relación entre Hijos y si Padre Vive**

Entre quienes tienen hijos, hay un mayor número de personas cuyo padre ha fallecido en comparación con quienes no tienen hijos. Esto indica que, en este grupo, tener hijos está asociado a una mayor frecuencia de no tener padre vivo.

## analisis categoria y maltrato intrafamiliar

![Relación entre categoría y maltrato intrafamiliar](https://github.com/Suarez5479/Analisis-datos-fac-equipo-X-/blob/main/Reportes/Analisis%20familiar/categoria%20y%20maltrato.png?raw=true)




Los casos de maltrato intrafamiliar son mucho más frecuentes en la categoría civil que en las categorías oficial y suboficial .

Las categorías oficiales y suboficiales tienen una baja incidencia de maltrato intrafamiliar en comparación con la categoría civil .



