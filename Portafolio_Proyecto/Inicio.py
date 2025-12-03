import streamlit as st

st.set_page_config(
    page_title="Dashboard de Defunciones en Baja California",
    page_icon="⚰️",
    layout="wide",)

# Título principal
st.title("⚰️ Dashboard de Defunciones en Baja California")

# Descripción general
st.markdown("""
Este dashboard interactivo presenta un análisis integral de las **defunciones registradas en Baja California durante el año 2023**,  
con información organizada por características demográficas, distribución geográfica y causas principales de muerte.

Utiliza el menú lateral para navegar por cada sección.
""")

st.divider()

# Descripción de cada pestaña
st.subheader("📁 Contenido del Dashboard")

st.markdown("""
### 📊 1. Dashboard General  
Resume la información esencial del registro de defunciones mediante gráficas, tarjetas informativas  
y tendencias generales del estado.

---

### ⚙️ 2. KPIs por Municipio  
Muestra indicadores clave desglosados por municipio: tasas, proporciones, variaciones  
y métricas que permiten evaluar el comportamiento local.

---

### 🏆 3. Rankings  
Presenta comparativas ordenadas como las principales causas, municipios con mayor incidencia,  
grupos de edad predominantes y otros listados destacados.

---

### 👥 4. Perfil Demográfico  
Explora las características de la población fallecida: edad, sexo, categorías de edad, ocupación  
y otros atributos que permiten describir la composición demográfica.

---

### 📍 5. Geografía Municipal  
Visualiza la distribución territorial de las defunciones.  
Incluye un mapa interactivo, concentraciones por municipio y comparaciones espaciales.
""")


st.info("Selecciona una pestaña en el menú lateral para comenzar el análisis.")

