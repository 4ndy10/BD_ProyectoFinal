
# Sistema de extracción, limpieza y dashboard de mortalidad en Baja California

Este proyecto implementa un pipeline completo para analizar defunciones en México (INEGI 2023), desde la extracción automatizada, hasta la creación de una base de datos en MySQL y un dashboard interactivo en Streamlit.

Incluye análisis de más de 24,000 registros de defunciones en Baja California, con clasificación por municipio, sexo, edad, ocupación, causa de muerte y tipología de violencia.


## Caracteristicas

Extracción automática desde APIs:
   - API datos.gob.mx
   - API geográfica INEGI
   - Catálogo CIE-10
   - Catálogo de ocupaciones
   - Descarga automatizada por Selenium (archivo DBF Ocupaciones)

Limpieza avanzada:
   - Normalización de claves
   - Corrección de encoding
   - Integración de catálogos
   - Clasificación de edad

Base de datos en MySQL:
   - Tablas creadas automáticamente desde Python
   - Relaciones, llaves foráneas e índices creados manualmente en MySQL

Dashboard interactivo:
   - Mapas Folium
   - Gráficas dinámicas Plotly
   - Filtros avanzados
   - Comparaciones por municipio, sexo, causa y ocupación



## Tech Stack
**Python**
pandas,
requests,
sqlalchemy,
mysql-connector-python,
selenium,
webdriver-manager,
xlrd,
openpyxl,
geopandas,
folium,
streamlit-folium,
plotly,
streamlit,
plotly.express

**MySQL**
Workbench
Conexión mediante mysql-connector-python

## ⚠️ Notas sobre Web Scraping de Ocupaciones y CIE-10

El proyecto incluye dos funciones de web scraping:

**descargar_ocupaciones()**

**descargar_cie10()**

Ambas sí funcionan, pero solo descargan los archivos originales desde INEGI:

- El archivo de ocupaciones se descarga como .xlsx (correcto).

- El archivo de causas CIE-10 se descarga como .zip, y debe extraerse manualmente.

Para evitar problemas de ejecución (como rutas, extracción manual o diferencias entre versiones del archivo), ya incluimos ambos archivos listos para usarse dentro de la carpeta:

**/data**


Por esa razón:
Es totalmente válido omitir o comentar estas líneas en el bloque final del script:

**descargar_ocupaciones()**

**descargar_cie10()**


## MySQL Setup
Antes de ejecutar el proyecto, se debe crear la base de datos vacía:

- CREATE DATABASE base_defunciones;

*Las tablas se generan automáticamente desde Python.*

*Las relaciones, índices y llaves foráneas NO se crean desde Python.*

**Todas las relaciones están contenidas en el archivo:**

*base_defunciones.sql*

Este archivo .sql contiene:
- Estructura final de la base de datos
- Relaciones entre tablas
- Índices
- Llaves foráneas
- Tipos de dato correctos

El archivo se incluye para fines de revisión por el profesor.

## Environment Variables

Debe configurarse la conexión(con sus datos) a MySQL dentro del script:

user = "root"    

password = "root"

server = "localhost"

name_bd = "base_defunciones"





## Pasos para ejecutar el proyecto

1.- Instalar dependencias

```bash
  py -m pip install -r requerimientos.txt

```

2.- Crear la base de datos en MySQL 

Abrir MySQL Workbench o la terminal y ejecutar:

  **CREATE DATABASE base_defunciones;**

No crear tablas manualmente.
El script las genera automáticamente.


3.- Ejecutar el pipeline de extracción y limpieza

**proyecto_final.py**
  
Este script:

- descarga datos desde APIs

- limpia datos

- corrige codificaciones

- genera catálogos

- carga los datos a MySQL

- produce Defunciones_Completo.csv

4.- Ejecutar el dashboard 

```bash
  py -m streamlit run Inicio.py
```



## Authors

**Becerra Zavala Atziri Elizabeth**

**Fernandez Fabian Lucia Beatriz**

**Hernandez Vazquez Mariana Isabel**

**Maldonado Neri Diana Mercedes**

**Soto Chavarin Andy**




