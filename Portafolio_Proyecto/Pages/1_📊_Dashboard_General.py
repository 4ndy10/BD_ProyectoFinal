import pandas as pd
import streamlit as st
from utils.cargas import load_main_data
from utils.graficas import (plot_line, plot_bar, plot_horizontal_bar,
                            plot_area, plot_line_scaled)


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

    st.title("📊 Panel General de Defunciones")

    # ============================
    #        Carga de datos
    # ============================
    df = load_main_data()
    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    # ============================
    #        Tarjetas API
    # ============================
    col1, col2, col3 = st.columns(3)

    # --- KPI 1: Defunciones totales ---
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Total Defunciones</h3>
            <p style="font-size:28px; color:#2B3674; font-weight:700;">
                {len(df):,}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- KPI 2: Causas totales ---
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Causas Totales</h3>
            <p style="font-size:28px; color:#2B3674; font-weight:700;">
                {df['CAUSA'].nunique()}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- KPI 3: Edad promedio ---
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <h3>Edad Promedio</h3>
            <p style="font-size:28px; color:#2B3674; font-weight:700;">
                {round(df['EDAD'].mean(), 1)}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # ============================
    #   Tendencia mensual
    # ============================
    st.subheader("📈 Tendencia mensual de defunciones (2023)")

    df["MES_NOMBRE_EN"] = df["FECHA"].dt.strftime("%B")

    orden_meses_en = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    defunciones_x_mes = (
        df.groupby("MES_NOMBRE_EN").size()
        .reindex(orden_meses_en, fill_value=0)
        .reset_index(name="DEFUNCIONES")
    )

    st.plotly_chart(
        plot_line_scaled(defunciones_x_mes, x="MES_NOMBRE_EN", y="DEFUNCIONES"),
        use_container_width=True
    )

    st.write("---")

    # ============================
    #      Municipios TOP
    # ============================
    st.subheader("🏙️ Municipios con más defunciones")

    top_mun = df["MUNICIPIO"].value_counts().head(10)

    st.plotly_chart(plot_horizontal_bar(top_mun), use_container_width=True)


if __name__ == "__main__":
    main()
