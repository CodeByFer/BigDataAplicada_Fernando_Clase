# Análisis Académico – Tarea 1: Primera Inspección de los Datos

## Objetivo

El objetivo de esta tarea es realizar una primera inspección de los ficheros CSV del proyecto de Análisis Académico con el fin de evaluar su calidad, estructura y posibles problemas antes de iniciar cualquier proceso de limpieza o transformación. Esta fase es clave para desarrollar un criterio crítico sobre los datos.

---

## Ficheros Analizados

- Alumnos.csv
- Calificaciones.csv
- Cursos.csv
- Grupos.csv
- Horas.csv
- Modulos.csv
- Lineas.csv
- Procesos.csv
- Objetivos.csv
- Indicadores_Finales.csv

---

## Análisis General de los Ficheros

### Separador de columnas

En todos los ficheros analizados se observa el uso del separador punto y coma (`;`), lo cual es habitual en configuraciones regionales españolas.

---

### Encabezados

Todos los ficheros contienen una primera fila con nombres de columnas. En general, los encabezados son descriptivos y permiten identificar correctamente el contenido de cada campo, aunque en algunos casos podrían mejorarse para estandarizar nomenclaturas (por ejemplo, uso consistente de `id_`).

---

### Inspección visual de los datos

Tras revisar las primeras filas de cada fichero se observan los siguientes patrones generales:

- Presencia de valores vacíos en algunos campos.
- Uso de valores como `N/A` o celdas en blanco.
- Campos numéricos almacenados como texto.
- Posibles inconsistencias en formatos (especialmente fechas o códigos).

Estos problemas justifican la necesidad de una fase posterior de limpieza en la capa Plata.

---

## Identificación de Claves e Identificadores

Durante la inspección se han identificado campos que actúan como claves y permiten relacionar los distintos conjuntos de datos:

- **Alumnos.csv**
  - `id_alumno`

- **Calificaciones.csv**
  - `id_alumno`
  - `id_modulo`
  - `id_curso`

- **Modulos.csv**
  - `id_modulo`

- **Cursos.csv**
  - `id_curso`

- **Grupos.csv**
  - `id_grupo`

- **Indicadores_Finales.csv**
  - Identificadores temporales y de curso para comparativas anuales

Estas claves serán fundamentales para el diseño del Data Warehouse en tareas posteriores.

---

## Problemas de Calidad Detectados

Los principales problemas detectados en esta primera inspección son:

- Valores nulos o ausentes en campos relevantes.
- Falta de validación en rangos numéricos (por ejemplo, notas).
- Inconsistencias en el tipo de dato esperado.
- Ausencia de restricciones que garanticen integridad referencial.

---

## Conclusión

Esta primera inspección permite entender el estado real de los datos académicos y justifica la necesidad de una arquitectura de procesamiento por capas. Los hallazgos de esta tarea servirán como base para definir las transformaciones de la capa Plata, el diseño del Data Warehouse y las políticas de calidad y gobernanza del dato en el resto del proyecto.

----

# Tarea 2

### Estrutuca de data prevista

```
Carpetas/
|-- bronce/
|   |-- carga de datos [enesimo archivo]
|   |-- Filtro.py --> capa Plata[enesimo filtro]
|
|
|-- plata/
|   |-- Año/
|          |--Curso/
|                  |--notas
|
|
|-- Oro/
|   |-- PowerBI

```

Primero llegan los datos a la capa bronce, estos son procesados por el Filtro.py y luego enviado a carpeta Plata a sus respectivos lugares

# Análisis Académico – Tarea 2: Arquitectura Data Lakehouse (Medallón)

## Objetivo

Definir una arquitectura de datos basada en el patrón **Medallón (Bronce, Plata y Oro)** para el proyecto de Análisis Académico, teniendo en cuenta la frecuencia de actualización de los datos, la necesidad de conservar históricos y su posterior explotación analítica.

La arquitectura se implementa conceptualmente sobre **AWS S3**, utilizando distintos niveles de procesamiento para garantizar calidad, trazabilidad y eficiencia analítica.

---

## Contexto del Proyecto

- Los **datos académicos** (calificaciones, alumnos, cursos, etc.) se actualizan **tras cada evaluación** (tres veces al año).
- Los **indicadores académicos** se actualizan **una vez al año**, al final del curso.
- Los informes utilizados por la dirección requieren **comparativas históricas entre cursos académicos**.

Este contexto justifica el uso de una arquitectura Lakehouse con separación clara entre datos brutos, datos limpios y datos agregados.

---

## Arquitectura Medallón

### 🟤 Capa Bronce (Raw Data)

**Objetivo:**  
Almacenar los datos originales exactamente como se reciben, sin aplicar transformaciones, preservando su estado inicial para auditoría y trazabilidad.

**Características:**

- Formato: CSV
- Datos sin limpiar ni validar
- Conservación de históricos
- Fuente directa de los sistemas académicos

**Datasets almacenados:**

- Alumnos.csv
- Calificaciones.csv
- Cursos.csv
- Grupos.csv
- Horas.csv
- Modulos.csv
- Lineas.csv
- Procesos.csv
- Objetivos.csv
- Indicadores_Finales.csv

**Ejemplo de estructura en S3:**

- s3://academic-datalake/bronze/alumnos/year=2024/
- s3://academic-datalake/bronze/calificaciones/year=2024/
- s3://academic-datalake/bronze/indicadores/year=2024/

**Responsable:**  
Sistema de ingesta (por ejemplo, Apache NiFi o scripts automatizados).

---

### 🥈 Capa Plata (Clean / Curated Data)

**Objetivo:**  
Aplicar procesos de limpieza, validación y normalización sobre los datos procedentes de la capa Bronce para garantizar su calidad y consistencia.

**Transformaciones típicas:**

- Eliminación o tratamiento de valores nulos
- Validación de rangos numéricos (por ejemplo, notas entre 0 y 10)
- Normalización de tipos de datos
- Estandarización de identificadores
- Corrección de inconsistencias detectadas en la Tarea 1

**Formato:**  

- Parquet (formato columnar y comprimido)

**Ejemplo de estructura en S3:**

- s3://academic-datalake/silver/alumnos/
- s3://academic-datalake/silver/calificaciones/
- s3://academic-datalake/silver/cursos/

**Responsable:**  
Ingeniero de Datos.

---

### 🥇 Capa Oro (Business / Analytics)

**Objetivo:**  
Proporcionar datos agregados y optimizados para el análisis académico, informes de dirección y cuadros de mando.

**Procesos aplicados:**

- Agregaciones por curso, módulo o evaluación
- Cálculo de medias, tasas de aprobados y comparativas interanuales
- Preparación de datasets orientados a BI

**Ejemplos de datasets:**

- Rendimiento académico por curso
- Evolución histórica de indicadores
- Comparativas entre evaluaciones

**Formato:**  

- Parquet

**Ejemplo de estructura en S3:**

- s3://academic-datalake/gold/rendimiento_academico/
- s3://academic-datalake/gold/indicadores_anuales/

**Responsable:**  
Analista BI / Científico de Datos.

---

## Relación con la Tarea 1

Los problemas de calidad detectados durante la inspección inicial de los CSV (valores nulos, inconsistencias de formato, falta de validaciones) justifican la existencia de la capa Plata y definen las transformaciones necesarias antes de que los datos puedan ser explotados analíticamente.

---

## Conclusión

La arquitectura Medallón permite estructurar el proyecto de Análisis Académico de forma escalable, trazable y alineada con las buenas prácticas del ecosistema Big Data. La separación por capas garantiza la preservación de los datos originales, mejora la calidad del dato y facilita su explotación para la toma de decisiones académicas.

# Análisis Académico – Tarea 3: Diseño del Data Warehouse (Kimball)

## Objetivo

Diseñar un Data Mart siguiendo la metodología de Kimball mediante un **Esquema en Estrella** para el proyecto de Análisis Académico.

---

## Proceso de negocio

**Evaluación académica / registro de calificaciones**.

---

## Grano (Grain)

**1 fila en la tabla de hechos = 1 calificación de 1 alumno en 1 módulo para una evaluación (trimestre) dentro de un curso académico (y opcionalmente un grupo).**

Este grano permite comparativas históricas y análisis por módulo, evaluación y curso.

---

## Tabla de Hechos: `fact_calificaciones`

### Claves foráneas (FK)

- `tiempo_key` → `dim_tiempo`
- `alumno_key` → `dim_alumno`
- `modulo_key` → `dim_modulo`
- `curso_key` → `dim_curso`
- `grupo_key` → `dim_grupo` (opcional / recomendable)

### Métricas

- `nota` (decimal)
- `aprobado` (0/1, derivado de nota)
- `count_calificaciones` (1 por fila)

---

## Dimensiones

### `dim_tiempo`

- `tiempo_key` (PK, surrogate)
- `anio`
- `curso_academico`
- `evaluacion` / `trimestre`

### `dim_alumno`

- `alumno_key` (PK, surrogate)
- `id_alumno` (business key)
- atributos descriptivos disponibles (según Alumnos.csv)

### `dim_modulo`

- `modulo_key` (PK, surrogate)
- `id_modulo` (business key)
- `nombre_modulo`
- atributos disponibles (según Modulos.csv)

### `dim_curso`

- `curso_key` (PK, surrogate)
- `id_curso` (business key)
- `curso_academico`
- atributos disponibles (según Cursos.csv)

### `dim_grupo` (si aplica)

- `grupo_key` (PK, surrogate)
- `id_grupo` (business key)
- nombre/código de grupo

---

## Consideración adicional: Indicadores anuales

Dado que los indicadores se actualizan una vez al año, se recomienda un segundo Data Mart:

- `fact_indicadores` (hechos anuales)
- Dimensiones: `dim_tiempo`, `dim_linea`, `dim_proceso`, `dim_objetivo`

Esto separa el análisis de calificaciones (trimestral) del análisis de indicadores (anual) y facilita comparativas históricas.

# Análisis Académico – Tarea 4: De CSV a Parquet con Python y Pandas

## Objetivo

Convertir los ficheros CSV limpios del proyecto de Análisis Académico a formato Parquet utilizando Python y Pandas, aplicando transformaciones de limpieza, validación de calidad y agregación, con el fin de dejar los datos preparados para su uso en entornos Big Data.

---

## Dataset utilizado

- Calificaciones.csv

---

## Transformaciones aplicadas

### Transformación 1 – Limpieza

Se eliminan los registros con valores nulos en el campo de nota, detectados durante la inspección inicial de los datos.

### Transformación 2 – Validación de calidad

Se valida que las notas estén dentro del rango permitido (0 a 10) y se asegura su correcto tipo numérico.

### Agregación final

Se calcula la nota media y el número de alumnos por curso y módulo, generando un dataset orientado a análisis académico.

---

## Conversión a Parquet

El resultado final se almacena en formato Parquet, un formato columnar y comprimido, adecuado para procesamiento analítico y herramientas Big Data.

---

## Resultado

- Fichero generado: `calificaciones_oro.parquet`
- Capa Medallón: Oro
- Uso previsto: análisis BI y comparativas académicas

# Análisis Académico – Tarea 5: Gobernanza y Calidad del Dato

## Objetivo

Definir los mecanismos de gobernanza del dato del proyecto de Análisis Académico mediante la creación de un Catálogo de Datos y la documentación del linaje del dato, garantizando trazabilidad, calidad y comprensión del ciclo de vida de la información.

---

## Data Catalog

El Data Catalog recoge todos los datasets del Data Lakehouse, indicando su capa Medallón, formato, frecuencia de actualización y responsable. Este catálogo permite identificar rápidamente qué datos existen y cuál es su uso previsto.

El catálogo se mantiene en el fichero `DATA_CATALOG.xlsx`.

---

## Data Lineage

El Data Lineage documenta el flujo completo de los datos desde su origen en la capa Bronce hasta su consumo analítico en la capa Oro. Para cada transformación se indican las reglas aplicadas y el responsable de la misma.

El linaje se mantiene en el fichero `DATA_LINEAGE.xlsx`.

---

## Calidad del Dato

Durante la capa Plata se aplican reglas de calidad orientadas a garantizar la fiabilidad de los datos académicos, especialmente sobre la nota numérica:

- Eliminación de valores nulos
- Validación de tipo numérico
- Validación de rango permitido (0–10)

Estas reglas aseguran que los datos consumidos en la capa Oro sean consistentes y aptos para análisis e informes de dirección.

---

## Conclusión

La gobernanza del dato permite asegurar la trazabilidad, calidad y control del ciclo de vida de los datos académicos. El uso de Data Catalog y Data Lineage facilita la auditoría, el mantenimiento y la evolución futura del proyecto.
