import pandas as pd
from streamlit import dataframe


carpeta= r"Pages"
dataframe= "Defunciones_Completo"

def load_main_data():
    global carpeta
    try:
        df = pd.read_csv(f"{carpeta}/{dataframe}.csv")
        return df
    except Exception as e:
        raise Exception(f"Error cargando main_data.csv: {e}")
