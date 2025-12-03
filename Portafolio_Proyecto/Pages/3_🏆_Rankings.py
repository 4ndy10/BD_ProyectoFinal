import streamlit as st
from utils.cargas import load_main_data
from utils.graficas import (plot_barras_municipio,plot_linea_mensual,
                            plot_area_top_dias, plot_barh_causas, plot_dotplot_ocupacion)


def main():
    st.title("🏆 Rankings")
    df = load_main_data()

    tipo = st.selectbox(
        "Selecciona Ranking:",
        ["Causas de muerte",
            "Ocupación",
            "Municipio",
            "Por mes",
            "Por día"])

    # Aplicar TOP
    if tipo in ["Causas de muerte", "Ocupación", "Municipio", "Por día","Por mes"]:
        top_n = st.slider("Selecciona TOP N:", 1, 7, 5)
    else:
        top_n = None

    st.write("---")

    if tipo == "Causas de muerte":
        st.plotly_chart(plot_barh_causas(df, top_n), use_container_width=True)

    elif tipo == "Ocupación":
        fig, omitidas, top3 = plot_dotplot_ocupacion(df, top_n)
        st.plotly_chart(fig, use_container_width=True)

        # Mostrar cantidades omitidas
        lugar1 = top3.iloc[0]
        lugar2 = top3.iloc[1]
        lugar3 = top3.iloc[2]

        st.info(f"""🔎 **Nota:** Para mejorar la visualización se omitieron las tres ocupaciones con mayor cantidad de defunciones:
        🥇 **1° lugar:** {lugar1['OCUPACION']} — **{lugar1['CANTIDAD']:,} defunciones** 
        🥈 **2° lugar:** {lugar2['OCUPACION']} — **{lugar2['CANTIDAD']:,} defunciones**
        🥉 **3° lugar:** {lugar3['OCUPACION']} — **{lugar3['CANTIDAD']:,} defunciones**
        La gráfica muestra las ocupaciones **a partir del 4° lugar real**""")

    elif tipo == "Municipio":
        st.plotly_chart(plot_barras_municipio(df, top_n), use_container_width=True)

    elif tipo == "Por mes":
        st.plotly_chart(plot_linea_mensual(df, top_n), use_container_width=True)

    elif tipo == "Por día":
        st.plotly_chart(plot_area_top_dias(df, top_n), use_container_width=True)

if __name__ == "__main__":
    main()


