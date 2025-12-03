import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------
# Gráfica de lineas
# ---------------------------
def plot_line(df, x, y):
    orden_meses = ["enero","febrero","marzo","abril","mayo","junio",
        "julio","agosto","septiembre","octubre","noviembre","diciembre"]

    if x.lower() == "mes":
        df[x] = pd.Categorical(df[x], categories=orden_meses, ordered=True)
        df = df.sort_values(by=x)

    fig = px.line(df, x=x, y=y, markers=True)

    fig.update_traces(
        text=df[y],
        textposition="top center",
        mode="lines+markers+text",
        line=dict(width=3, color="#2B3674"))

    fig.update_layout(template="plotly_white", height=400)
    return fig


# ---------------------------
# Gráfica de barras
# ---------------------------
def plot_bar(series):
    fig = px.bar(
        series.reset_index(),
        x=series.index.name,
        y=series.name,
        text=series.name)

    fig.update_traces(
        textposition="outside",
        marker_color="#4B8BBE")

    fig.update_layout(
        template="plotly_white",
        yaxis_title="Cantidad")

    return fig


# ---------------------------
# Gráfica de área
# ---------------------------
def plot_area(df, x, y):

    fig = px.area(
        df,
        x=x,
        y=y,
        markers=True,
        color_discrete_sequence=["#2B3674"] )

    fig.update_traces(
        text=df[y],
        textposition="top center",
        mode="lines+markers+text",
        line=dict(width=3, shape="spline"), # Curva suave
        opacity=0.85)

    fig.update_layout(
        template="plotly_white",
        height=420,
        hovermode="x unified",
        margin=dict(l=40, r=20, t=40, b=40),
        dragmode="pan",)  # Mover la gráfica arrastrando

    fig.update_xaxes(
        showgrid=False,
        rangeslider=dict(visible=True), # Moverse entre meses
        fixedrange=False) # Zoom libre

    fig.update_yaxes(
        showgrid=True,
        fixedrange=False)

    return fig



# ---------------------------
# Gráfica barras horizontales
# ---------------------------

def plot_horizontal_bar(series):

    df = pd.DataFrame({
        "MUNICIPIO": series.index,
        "DEFUNCIONES": series.values})

    fig = px.bar(
        df,
        x="DEFUNCIONES",
        y="MUNICIPIO",
        orientation="h",
        text="DEFUNCIONES",
        color="DEFUNCIONES",
        color_continuous_scale="Blues",)

    fig.update_traces(
        textposition="outside",
        marker_line_color="#333",
        marker_line_width=1.2)

    fig.update_layout(
        title="Municipios con Más Defunciones",
        template="plotly_white",
        height=420,
        coloraxis_colorbar_title="Defunciones",   # barra lateral
        margin=dict(l=40, r=20, t=40, b=20))

    return fig


# ---------------------------
# Gráfica de lína dashboard general
# ---------------------------
def plot_line_scaled(df, x, y):

    orden_meses = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]

    # Ordenar por mes
    if x.lower() == "mes_nombre" or x.lower() == "mes":
        df = df.copy()
        df[x] = pd.Categorical(df[x], categories=orden_meses, ordered=True)
        df = df.sort_values(by=x)

    fig = px.line(df, x=x, y=y, markers=True)

    # Ajustar eje Y
    ymin = df[y].min() - 20
    ymax = df[y].max() + 20
    fig.update_yaxes(range=[ymin, ymax])

    # Mostrar valores encima de cada punto
    fig.update_traces(
        text=df[y],
        textposition="top center",
        mode="lines+markers+text")

    fig.update_layout(
        title="Tendencia Mensual (Escala Ajustada)",
        template="plotly_white",
        height=400,
        margin=dict(l=10, r=10, t=40, b=10))

    return fig

# ---------------------------
# Gráfica de pastel
# ---------------------------
def plot_pie(series):

    df = pd.DataFrame({
        "CATEGORIA": series.index,
        "VALOR": series.values})

    azul_palette = ["#0B3C5D", "#3282B8", "#BBE1FA"]

    fig = px.pie(
        df,
        names="CATEGORIA",
        values="VALOR",
        color="CATEGORIA",
        color_discrete_sequence=azul_palette[:len(df)],
        hole=0.35)

    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        pull=[0.05] * len(df))

    fig.update_layout(
        title="Distribución por Sexo",
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title="")

    return fig


# ---------------------------
# Histograma
# ---------------------------
def plot_histogram(df, x_col="EDAD", nbins=20, title="Distribución de defunciones por edad"):

    fig = px.histogram(
        df,
        x=x_col,
        nbins=nbins,
        labels={x_col: x_col.capitalize()},
        title=title,
        color_discrete_sequence=["#3282B8"])

    fig.update_traces(
        marker_line_color="#0B3C5D",
        marker_line_width=1.5,
        opacity=0.85)

    fig.update_layout(
        bargap=0.05,
        xaxis_title=x_col.capitalize(),
        yaxis_title="Cantidad",
        template="simple_white",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=40, b=20))

    return fig



# =====================================================
# Barras horizontales ranking de causas
# =====================================================
def plot_barh_causas(df, top_n=5):

    ranking = (
        df.groupby("CAUSA")["ID_DEFUNCION"]
        .count()
        .reset_index(name="CANTIDAD")
        .sort_values("CANTIDAD", ascending=False)
        .head(top_n))

    fig = px.bar(
        ranking,
        x="CANTIDAD",
        y="CAUSA",
        orientation="h",
        text="CANTIDAD",
        color="CANTIDAD",
        color_continuous_scale="Blues",)

    fig.update_traces(
        textposition="outside",
        marker_line_color="#333",
        marker_line_width=1.2)

    fig.update_layout(
        title=f"Barras Horizontales – Top {top_n} causas de muerte",
        template="plotly_white",
        height=500,
        yaxis=dict(title="", automargin=True),
        xaxis_title="Cantidad",
        coloraxis_colorbar_title="Cantidad",
        margin=dict(l=40, r=20, t=60, b=20))

    return fig


# =====================================================
# Barras horizontales ranking ocupación
# =====================================================

def plot_dotplot_ocupacion(df, top_n=12):

    ocupaciones_omitidas = [
        "No trabaja",
        "No especificada",
        "Ocupaciones insuficientemente especificadas"]

    ranking_general = (
        df.groupby("OCUPACION")["ID_DEFUNCION"]
          .count()
          .reset_index(name="CANTIDAD")
          .sort_values("CANTIDAD", ascending=False))

    # Filtrar ocupaciones que omitimos
    ranking_filtrado = ranking_general[
        ~ranking_general["OCUPACION"].isin(ocupaciones_omitidas)].head(top_n)

    # Empezar la numeración desde el 4
    ranking_filtrado = ranking_filtrado.copy()
    ranking_filtrado["OCUPACION_NUM"] = [
        f"{i}. {oc}"
        for i, oc in zip(range(4, 4 + len(ranking_filtrado)),
                         ranking_filtrado["OCUPACION"])]

    fig = px.scatter(
        ranking_filtrado,
        x="CANTIDAD",
        y="OCUPACION_NUM",
        size=[10] * len(ranking_filtrado),     # 🔵 CÍRCULOS MÁS PEQUEÑOS
        color="CANTIDAD",
        color_continuous_scale="Blues",
        title="🔵 Dot Plot – Ocupaciones con más defunciones (desde 4° lugar real)",)

    fig.update_traces(
        marker=dict(
            line=dict(color="black", width=1)) )

    fig.update_layout(
        template="plotly_white",
        yaxis=dict(automargin=True),
        height=600,
        margin=dict(l=350),
        coloraxis_colorbar_title="CANTIDAD")

    # Top 3 sin filtrar
    top3 = ranking_general.head(3)

    return fig, ocupaciones_omitidas, top3


# =====================================================
# Barras verticales ranking municipios
# =====================================================
def plot_barras_municipio(df, top_n):

    ranking = (
        df.groupby("MUNICIPIO")["ID_DEFUNCION"]
        .count()
        .reset_index(name="CANTIDAD")
        .sort_values("CANTIDAD", ascending=False))

    top_df = ranking.head(top_n)

    fig = px.bar(
        top_df,
        x="MUNICIPIO",
        y="CANTIDAD",
        text="CANTIDAD",
        title=f"📍 Top {top_n} municipios con más defunciones",
        color="CANTIDAD",
        color_continuous_scale="Blues",)

    fig.update_traces(
        textposition="outside",
        marker_line_color="black",
        marker_line_width=1.3)

    fig.update_layout(
        template="plotly_white",
        xaxis={'categoryorder': 'total descending'},
        coloraxis_colorbar_title="Defunciones",
        height=450,
        margin=dict(l=40, r=40, t=60, b=40))

    return fig



# =====================================================
# Gráfica de líneas ranking mes
# =====================================================
def plot_linea_mensual(df, top_n=None):

    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
    df["MES"] = df["FECHA"].dt.month

    orden_meses = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO",
        "JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]

    df["MES_NOMBRE"] = df["MES"].apply(
        lambda x: orden_meses[int(x)-1] if pd.notna(x) else None)

    ranking = (
        df.groupby("MES_NOMBRE")["ID_DEFUNCION"]
        .count()
        .reset_index(name="CANTIDAD"))

    if top_n is not None:
        ranking = ranking.sort_values("CANTIDAD", ascending=False).head(top_n)

    ranking = ranking.sort_values("CANTIDAD", ascending=False)

    fig = go.Figure()

    # Hacer la línea azu
    fig.add_trace(go.Scatter(
        x=ranking["MES_NOMBRE"],
        y=ranking["CANTIDAD"],
        mode="lines",
        line=dict(color="#1f77b4", width=3),
        name="Tendencia"))

    # Hacer los puntos mas pequeños
    fig.add_trace(go.Scatter(
        x=ranking["MES_NOMBRE"],
        y=ranking["CANTIDAD"],
        mode="markers+text",
        marker=dict(
            size=11,
            color=ranking["CANTIDAD"],
            colorscale="Blues",
            line=dict(color="black", width=1)),
        text=ranking["CANTIDAD"],
        textposition="top center",
        showlegend=False))

    fig.update_layout(
        title=(
            f"📅 Ranking mensual – Top {top_n} meses con más defunciones"
            if top_n else "📅 Defunciones por mes"),
        template="plotly_white",
        height=480,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis_title="Mes",
        yaxis_title="Defunciones",)

    return fig


# =====================================================
# Gráfica de área ranking días
# =====================================================
def plot_area_top_dias(df, top_n=5):

    df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")

    df = df[df["FECHA"].dt.year == 2023]

    tendencia = (
        df.groupby(df["FECHA"].dt.date)["ID_DEFUNCION"]
        .count()
        .reset_index(name="CANTIDAD"))

    tendencia = tendencia.sort_values("CANTIDAD", ascending=False).head(top_n)

    tendencia["FECHA_STR"] = tendencia["FECHA"].astype(str)

    max_val = tendencia["CANTIDAD"].max()

    fig = px.area(
        tendencia,
        x="FECHA_STR",
        y="CANTIDAD",
        title=f"📈 TOP {top_n} días con más defunciones (2023)",)

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Número de defunciones",
        xaxis=dict(
            type="category",
            categoryorder="array",
            categoryarray=tendencia["FECHA_STR"].tolist()),
        yaxis=dict(
            range=[80, max_val + 3],  # Que la gráfica inicie en 80
            dtick=1 ))

    fig.update_traces(
        mode="lines+markers",
        line_shape="spline",
        fill="tozeroy")

    return fig
















