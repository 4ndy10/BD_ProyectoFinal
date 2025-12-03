import streamlit as st
import pandas as pd
from utils.cargas import load_main_data
from utils.graficas import plot_bar, plot_line, plot_area, plot_pie, plot_histogram


def main():

    # ============================
    #     Estilo global
    # ============================
    st.markdown("""
    <style>
    .stApp { background-color: #F8F9FC; }

    h1, h2, h3 {
        color: #2B3674;
        font-weight: 700;
    }

    .kpi-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📊 Dashboard de KPIs por Municipio")

    # ============================
    #        Carga de datos
    # ============================
    df = load_main_data()
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    df["MES"] = df["FECHA"].dt.month
    df["MES_NOMBRE"] = df["FECHA"].dt.month_name(locale="es_MX").str.capitalize()

    orden_meses = [
        "Enero","Febrero","Marzo","Abril","Mayo","Junio",
        "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
    ]
    df["MES_NOMBRE"] = pd.Categorical(df["MES_NOMBRE"], categories=orden_meses, ordered=True)

    # ============================
    #     Filtro municipios barra lateral
    # ============================
    st.sidebar.markdown("### 🔍 Filtro por municipio")

    municipios = ["Todos"] + sorted(df["MUNICIPIO"].unique())
    municipio_global = st.sidebar.selectbox("Selecciona un municipio:", municipios, index=0)

    df_filtro_global = df if municipio_global == "Todos" else df[df["MUNICIPIO"] == municipio_global]

    # ============================
    #        Tarjetas API
    # ============================

    col1, col2, col3 = st.columns(3)

    # --- Municipios registrados ---
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <h3>Municipios Registrados</h3>
                <p style="font-size:28px; color:#2B3674; font-weight:700;">
                    {df['MUNICIPIO'].nunique()}
                </p>
            </div>
        """, unsafe_allow_html=True)

    # --- Sexo con más defunciones ---
    sexo_top = df["SEXO"].value_counts().idxmax()
    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <h3>Sexo con más defunciones</h3>
                <p style="font-size:28px; color:#2B3674; font-weight:700;">{sexo_top}</p>
            </div>
        """, unsafe_allow_html=True)

    # --- Mes con más defunciones ---
    mes_top = df["MES_NOMBRE"].value_counts().idxmax()
    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <h3>Mes con más defunciones</h3>
                <p style="font-size:28px; color:#2B3674; font-weight:700;">{mes_top}</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # ============================
    #   Defunciones municipio y sexo
    # ============================
    st.subheader("1️⃣ Defunciones por Municipio y Sexo")

    kpi_sexo = df_filtro_global.groupby("SEXO")["ID_DEFUNCION"].count().sort_values(ascending=False)

    st.plotly_chart(plot_pie(kpi_sexo), use_container_width=True)

    st.dataframe(kpi_sexo.reset_index())

    st.write("---")

    # ============================
    #   Histograma municipio, categoría y edad
    # ============================
    st.subheader("2️⃣ Histograma por Municipio, Categoría y Edad")

    categorias = sorted(df_filtro_global["CATEGORIA"].unique())
    categoria_sel = st.selectbox("Selecciona una categoría:", categorias)

    df_hist = df_filtro_global[df_filtro_global["CATEGORIA"] == categoria_sel]

    st.plotly_chart(plot_histogram(df_hist), use_container_width=True)

    df_kpi = (
        df_hist.groupby("EDAD")["ID_DEFUNCION"]
        .count()
        .reset_index(name="CANTIDAD")
        .sort_values("EDAD"))

    st.dataframe(df_kpi)

    st.write("---")

    # ============================
    #   Defunciones por municipio y mes
    # ============================
    st.subheader("3️⃣ Defunciones por Municipio y Mes del Año")

    kpi_mes = df_filtro_global.groupby("MES_NOMBRE")["ID_DEFUNCION"].count()

    st.plotly_chart(
        plot_area(kpi_mes.reset_index(), "MES_NOMBRE", "ID_DEFUNCION"),
        use_container_width=True)
    st.dataframe(kpi_mes.reset_index())

    st.write("---")


if __name__ == "__main__":
    main()
