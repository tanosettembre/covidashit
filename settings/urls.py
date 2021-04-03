"""
URLs Settings
"""
import os

URL_BASE_PC = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/"
NATIONAL_FILE = (
    "dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")
REGIONAL_FILE = "dati-regioni/dpc-covid19-ita-regioni.csv"
PROVINCIAL_FILE = "dati-province/dpc-covid19-ita-province.csv"
URL_NATIONAL = os.path.join(URL_BASE_PC, NATIONAL_FILE)
URL_REGIONAL = os.path.join(URL_BASE_PC, REGIONAL_FILE)
URL_PROVINCIAL = os.path.join(URL_BASE_PC, PROVINCIAL_FILE)
URL_BASE_OD = (
    "https://raw.githubusercontent.com/"
    "italia/covid19-opendata-vaccini/master/dati/"
)
ADMINS_FILE = "somministrazioni-vaccini-latest.csv"
ADMINS_SUMMARY_FILE = "somministrazioni-vaccini-summary-latest.csv"
SUMMARY_FILE = "vaccini-summary-latest.csv"
VAX_LATEST_UPDATE_FILE = "last-update-dataset.="
URL_ADMINS = os.path.join(URL_BASE_OD, ADMINS_FILE)
URL_VAX_LATEST_UPDATE = os.path.join(URL_BASE_OD, VAX_LATEST_UPDATE_FILE)
URL_SUMMARY = os.path.join(URL_BASE_OD, SUMMARY_FILE)
URL_ADMINS_SUMMARY = os.path.join(URL_BASE_OD, ADMINS_SUMMARY_FILE)
