import pandas as pd
import requests
from sqlalchemy import create_engine
from enum import Enum
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def abrir_navegador():
    opciones = Options()
    opciones.add_argument("--start-maximized")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opciones)

def descargar_ocupaciones():
    nav = abrir_navegador()
    wait = WebDriverWait(nav, 20)

    nav.get("https://www.inegi.org.mx/programas/edr/#microdatos")
    nav.execute_script("window.scrollTo(0, 800);")

    boton = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a[href$='defunciones_base_datos_2023_dbf.zip']")))

    nav.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
    time.sleep(1)

    nav.execute_script("arguments[0].click();", boton)
    boton.click()
    print("Descargando archivo de ocupaciones")

    time.sleep(5)
    nav.close()


def descargar_cie10():
    nav = abrir_navegador()
    wait = WebDriverWait(nav, 20)

    nav.get("https://www.inegi.org.mx/rnm/index.php/catalog/1048/related-materials")
    nav.execute_script("window.scrollTo(0, 1200);")

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(., 'Lista de causas CIE-10')]"))).click()

    boton = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "a.download[href*='32901']")))
    boton.click()
    print("Descargando archivo de causas")

    time.sleep(5)
    nav.close()

def extraccion_defunciones_y_municipios_conAPI():
    print("Extrayendo información con API")

    # ========== Defunciones ==========
    url_def = (
        "https://datos.gob.mx/api/3/action/datastore_search"
        "?resource_id=f6fab6c3-6cba-4e9f-a406-4ce7b8432565"
        "&filters={\"ENT_OCURR\":\"2\"}"
        "&fields=ENT_OCURR,MUN_OCURR,CAUSA_DEF,EDAD,FECHA_OCURR,OCUPACION,SEXO"
        "&limit=30000")

    df_def = pd.DataFrame(requests.get(url_def).json()["result"]["records"])
    df_def.to_csv("csvs/Defunciones_api_sucio.csv", index=False, encoding="utf-8-sig")

    # ========== Municipios ==========
    url_mun = "https://gaia.inegi.org.mx/wscatgeo/v2/mgem/02"
    df_mun = pd.DataFrame(requests.get(url_mun).json()["datos"])
    df_mun.to_csv("csvs/Municipios_api_sucio.csv", index=False, encoding="utf-8-sig")

    # ========== CIE10 ==========
    df_cie10 = pd.read_excel("data/catminde.xls", engine="xlrd", dtype=str)
    df_cie10.to_csv("csvs/CIE10_sucio.csv", index=False)

    # ========== Ocupaciones ==========
    df_ocup = pd.read_excel("data/OCUPACIONES.xlsx")
    df_ocup.to_csv("csvs/Ocupaciones_sucio.csv", index=False)

    print("Información extraída correctamente")

def limpieza():
    print("Limpiando datos")

    # ====== Defunciones ======
    df = pd.read_csv("csvs/Defunciones_api_sucio.csv", dtype=str)

    df = df.rename(columns={
        "MUN_OCURR": "ID_MUN",
        "CAUSA_DEF": "ID_CAUSA",
        "SEXO": "ID_SEXO",
        "OCUPACION": "ID_OCUP",
        "FECHA_OCURR": "FECHA",
        "EDAD": "CLAVE_EDAD"})

    df["CLAVE_EDAD"] = pd.to_numeric(df["CLAVE_EDAD"], errors="coerce")

    df.loc[df["CLAVE_EDAD"] == 4998, "ID_CAT_EDAD"] = 5
    df.loc[df["CLAVE_EDAD"] == 4998, "EDAD"] = 0
    df.loc[df["CLAVE_EDAD"] != 4998, "ID_CAT_EDAD"] = df["CLAVE_EDAD"] // 1000
    df.loc[df["CLAVE_EDAD"] != 4998, "EDAD"] = df["CLAVE_EDAD"] % 1000

    df = df[["ID_MUN", "ID_CAUSA", "ID_SEXO",
        "ID_OCUP", "FECHA", "ID_CAT_EDAD", "EDAD"]]

    df["ID_CAT_EDAD"] = df["ID_CAT_EDAD"].astype("Int64")
    df["EDAD"] = df["EDAD"].astype("Int64")

    df.insert(0, "ID_DEFUNCION", range(1, len(df) + 1))

    df.to_csv("csvs/Defunciones_limpio.csv", index=False, encoding="utf-8-sig")

    # ====== Municipios ======
    df_mun = pd.read_csv("csvs/Municipios_api_sucio.csv")
    df_mun = df_mun[["cve_mun", "nomgeo"]]
    df_mun = df_mun.rename(columns={
        "cve_mun": "ID_MUN",
        "nomgeo": "MUNICIPIO"})
    df_mun.to_csv("csvs/Municipios_limpio.csv", index=False, encoding="utf-8-sig")

    # ====== CIE10 ======
    df_cie = pd.read_csv("csvs/CIE10_sucio.csv", dtype=str)
    df_cie = df_cie.rename(columns={
        df_cie.columns[0]: "ID_CAUSA",
        df_cie.columns[1]: "CAUSA"})

    fixes = {'¾': 'ó', '¡': 'í', '®': 'é', '¢': 'á', '³': 'ó',
        'Ã³': 'ó', 'Ã¡': 'á', 'Ã­': 'í', 'Ã©': 'é', 'Ãº': 'ú',
        'â€“': '–', 'â€™': "’", "Ý": "'í", "ß": "á", "Ú": "é", "·": "ú",
        "'": "", "┌":"Ú", "±": "ñ", "═":"Í"}

    def reparar(texto):
        if pd.isna(texto):
            return texto
        for malo, bueno in fixes.items():
            texto = texto.replace(malo, bueno)
        return texto

    df_cie["CAUSA"] = df_cie["CAUSA"].apply(reparar)
    df_cie.to_csv("csvs/Causas_limpio.csv", index=False, encoding="utf-8-sig")

    # ====== Ocupaciones ======
    df_ocup = pd.read_csv("csvs/Ocupaciones_sucio.csv")
    df_ocup = df_ocup.rename(columns={
        "CVE": "ID_OCUP",
        "DESCRIP": "OCUPACION"})
    df_ocup.to_csv("csvs/Ocupaciones_limpio.csv", index=False, encoding="utf-8-sig")

    # ====== Sexo y Categorías ======
    pd.DataFrame({
        "ID_SEXO": [1, 2, 9],
        "SEXO": ["Masculino", "Femenino", "No aplica"]}).to_csv("csvs/Sexo.csv", index=False, encoding="utf-8-sig")

    pd.DataFrame({
        "ID_CAT_EDAD": [1, 2, 3, 4, 5],
        "CATEGORIA": ["Horas", "Días", "Meses", "Años", "No especificado"]
    }).to_csv("csvs/Categorias.csv", index=False, encoding="utf-8-sig")

    print("Limpieza completada\n")

class DataDB(Enum):
    USER = "root"
    PASSWORD = "root"
    NAME_BD = "base_defunciones"
    SERVER = "localhost"

def cargar_mysql():
    print("Cargando a MySQL\n")

    con_string = (
        f"mysql+mysqlconnector://{DataDB.USER.value}:"
        f"{DataDB.PASSWORD.value}@{DataDB.SERVER.value}/"
        f"{DataDB.NAME_BD.value}")
    engine = create_engine(con_string)
    conn = engine.connect()

    tablas = {"Defunciones": "csvs/Defunciones_limpio.csv",
        "Municipios": "csvs/Municipios_limpio.csv",
        "Causas": "csvs/Causas_limpio.csv",
        "Ocupaciones": "csvs/Ocupaciones_limpio.csv",
        "Sexo": "csvs/Sexo.csv",
        "Categorias": "csvs/Categorias.csv"}

    for tabla, ruta in tablas.items():
        df = pd.read_csv(ruta, encoding="utf-8-sig")
        df.to_sql(tabla, conn, if_exists="replace", index=False)
        print(f"Tabla {tabla} cargada")

    conn.close()
    print("Conexión cerrada\n")

def generar_csv_final():
    print("Fusionando información final")
    c = "csvs"

    df = pd.read_csv(f"{c}/Defunciones_limpio.csv")
    df = df.merge(pd.read_csv(f"{c}/Municipios_limpio.csv"), on="ID_MUN", how="left")
    df = df.merge(pd.read_csv(f"{c}/Causas_limpio.csv"), on="ID_CAUSA", how="left")
    df = df.merge(pd.read_csv(f"{c}/Ocupaciones_limpio.csv"), on="ID_OCUP", how="left")
    df = df.merge(pd.read_csv(f"{c}/Sexo.csv"), on="ID_SEXO", how="left")
    df = df.merge(pd.read_csv(f"{c}/Categorias.csv"), on="ID_CAT_EDAD", how="left")

    df.to_csv(f"Pages/Defunciones_Completo.csv", index=False, encoding="utf-8-sig")

    print("Archivo final generado en carptea Pages\n")


if __name__ == "__main__":
    #descargar_ocupaciones()

    #descargar_cie10()

    # 1. solo extrae
    extraccion_defunciones_y_municipios_conAPI()

    # 2. Limpiatodo
    limpieza()

    # 3. Genera tablas en mysql
    cargar_mysql()

    # 4. genera CSV unificado
    generar_csv_final()
