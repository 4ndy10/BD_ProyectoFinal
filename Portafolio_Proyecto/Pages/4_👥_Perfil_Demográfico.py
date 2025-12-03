import streamlit as st
from utils.cargas import load_main_data


st.title("📊 Perfil Demográfico — Análisis de Mortalidad")
df = load_main_data()

# ==============================
# Clasificación de Causas
# ==============================
def clasificar_mortalidad(causa):
    code = causa[:3]

    if "X60" <= code <= "X84":
        return "Violenta - Suicidio"

    if ("X85" <= code <= "X99") or ("Y00" <= code <= "Y09"):
        return "Violenta - Homicidio"

    if "Y20" <= code <= "Y34":
        return "Violenta - Intención no determinada"

    if ("V01" <= code <= "V99") or ("W00" <= code <= "W84") or ("X00" <= code <= "X59"):
        return "Violenta - Accidental"

    return "No violenta"

def clasif_solo_general(tipo):
    return "Violenta" if "Violenta" in tipo else "No violenta"


df["TIPO_MORTALIDAD"] = df["ID_CAUSA"].apply(clasificar_mortalidad)
df["VIOLENTO"] = df["TIPO_MORTALIDAD"].apply(clasif_solo_general)


# ==============================
# Filtros
# ==============================
with st.expander("🔎 Mostrar filtros", expanded=True):
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        municipio = st.selectbox("🏙️ Municipio", ["Todos"] + sorted(df["MUNICIPIO"].unique()))

    with col2:
        sexo = st.selectbox("⚧ Sexo", ["Todos"] + sorted(df["SEXO"].unique()))

    with col3:
        tipo_mort = st.selectbox("☠ Tipo de mortalidad de la causa de defunción", ["Todos"] + sorted(df["TIPO_MORTALIDAD"].unique()))

    with col4:
        categoria = st.selectbox("👶 Categoría de edad", ["Todos"] + sorted(df["CATEGORIA"].unique()))

filtro = df.copy()

if municipio != "Todos":
    filtro = filtro[filtro["MUNICIPIO"] == municipio]

if sexo != "Todos":
    filtro = filtro[filtro["SEXO"] == sexo]

if tipo_mort != "Todos":
    filtro = filtro[filtro["TIPO_MORTALIDAD"] == tipo_mort]

if categoria != "Todos":
    filtro = filtro[filtro["CATEGORIA"] == categoria]

# ==============================
# Filtrar tabla principal
# ==============================
st.subheader("📄 Datos filtrados")

filtro = filtro.reset_index(drop=True)

columnas_mostrar = [
    "ID_DEFUNCION",
    "MUNICIPIO",
    "SEXO",
    "EDAD",
    "CATEGORIA",
    "CAUSA",
    "OCUPACION",
    "TIPO_MORTALIDAD",
    "VIOLENTO"]

st.dataframe(filtro[columnas_mostrar], use_container_width=True)

# ==============================
# Indicadores
# ==============================
st.header("📈 Indicadores principales")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total de defunciones", len(filtro))

with col2:
    st.metric("Total violentas", sum(filtro["VIOLENTO"] == "Violenta"))

# ==============================
# Resumenes
# ==============================
st.subheader("📊 Violento vs No violento")
st.dataframe(filtro["VIOLENTO"].value_counts())

st.subheader("📊 Subtipos de violencia")
st.dataframe(filtro["TIPO_MORTALIDAD"].value_counts())

st.subheader("📊 Violencia por sexo")
st.dataframe(filtro.groupby(["VIOLENTO", "SEXO"]).size().reset_index(name="conteo"))

