import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from utils.cargas import load_main_data


st.set_page_config(layout="wide")
st.title("Geografía municipal defunciones - Baja California (AGEM INEGI)")
df = load_main_data()

# Agrupar defunciones por municipio
df_mun = df.groupby("ID_MUN").size().reset_index(name="defunciones")

# -------------------------------------------------------------
# Cargar Shapefile de Municipios de Baja California AGEM
# -------------------------------------------------------------
@st.cache_data
def load_map():
    mapa = gpd.read_file("Pages/2023_1_02_MUN.shp")
    mapa["CVE_MUN"] = mapa["CVE_MUN"].astype(int)
    return mapa

bc = load_map()


# -------------------------------------------------------------
# Unir información con el mapa
# -------------------------------------------------------------
bc = bc.merge(df_mun, left_on="CVE_MUN", right_on="ID_MUN", how="left")
bc["defunciones"] = bc["defunciones"].fillna(0)

# -------------------------------------------------------------
# Creación el mapa
# -------------------------------------------------------------
m = folium.Map(location=[31.8, -116.0], zoom_start=7, tiles="CartoDB positron")

folium.Choropleth(
    geo_data=bc,
    data=bc,
    columns=("CVE_MUN", "defunciones"),
    key_on="feature.properties.CVE_MUN",
    fill_color="YlOrRd",
    fill_opacity=0.8,
    line_opacity=0.4,
    nan_fill_color="white",
    legend_name="Defunciones por Municipio").add_to(m)

for idx, row in bc.iterrows():
    try:
        centroid = row["geometry"].centroid
        folium.Marker(
            location=[centroid.y, centroid.x],
            popup=f"{row['NOMGEO']}: {int(row['defunciones'])} defunciones",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
    except:
        pass

# Unir total de defunciones por municipio
total_mun = df.groupby("MUNICIPIO").size().reset_index(name="total_def")
bc = bc.merge(total_mun, left_on="NOMGEO", right_on="MUNICIPIO", how="left")
bc["total_def"] = bc["total_def"].fillna(0).astype(int)
m = folium.Map(location=[32.5, -115.9], zoom_start=7)

# Polígonos del estado
folium.GeoJson(
    bc,
    name="Municipios",
    style_function=lambda x: {
        "fillColor": "#74a9cf",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.4,},
    highlight_function=lambda x: {
        "weight": 3,
        "color": "yellow",
        "fillOpacity": 0.7},
    tooltip=folium.GeoJsonTooltip(
        fields=["NOMGEO", "total_def"],
        aliases=["Municipio", "Total de defunciones"],
        localize=True),
    popup=folium.GeoJsonPopup(
        fields=["NOMGEO", "total_def"],
        aliases=["Municipio", "Total de defunciones"],
        localize=True)).add_to(m)

st_map = st_folium(m, width=700, height=500)

if st_map and "last_active_drawing" in st_map:
    info = st_map["last_active_drawing"]

    if info and "properties" in info:
        municipio = info["properties"].get("NOMGEO")

        if municipio:
            st.success(f"Municipio seleccionado: {municipio}")

            df_mun = df[df["MUNICIPIO"] == municipio]

            # Métricas
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de defunciones", len(df_mun))
            col2.metric("Hombres", (df_mun["SEXO"] == "Masculino").sum())
            col3.metric("Mujeres", (df_mun["SEXO"] == "Femenino").sum())

            # Principales causas
            st.write("### Principales causas de muerte")
            st.dataframe(
                df_mun["CAUSA"]
                .value_counts()
                .head(10)
                .reset_index()
                .rename(columns={"index": "Causa", "CAUSA": "Total"}))
