"""
Settings
"""
from collections import OrderedDict

from flask_babel import gettext

from settings.vars import (
    HOSPITALIZED_WITH_SYMPTOMS_KEY, ICU_KEY,
    DAILY_ICU_KEY, DAILY_ICU_MA_KEY, TOTAL_HOSPITALIZED_KEY,
    DAILY_HOSPITALIZED_KEY, DAILY_HOSPITALIZED_MA_KEY, SELF_ISOLATION_KEY,
    TOTAL_POSITIVE_KEY, NEW_POSITIVE_KEY, NEW_POSITIVE_MA_KEY,
    TOTAL_HEALED_KEY, TOTAL_DEATHS_KEY, DAILY_DEATHS_KEY, DAILY_DEATHS_MA_KEY,
    TOTAL_CASES_KEY, TOTAL_SWABS_KEY, DAILY_SWABS_KEY, DAILY_SWABS_MA_KEY,
    VAX_FIRST_DOSE_KEY, VAX_SECOND_DOSE_KEY, HEALTHCARE_PERS_KEY,
    NONHEALTHCARE_PERS_KEY, HFE_GUESTS_KEY, OVER_80_KEY, OTHER_KEY,
    ARMED_FORCES_KEY, SCHOOL_PERS_KEY
)

VERSION = "4.8"
PAGE_BASE_TITLE = gettext("COVID-19 Italy")
TRANSLATION_DIRNAME = "translations"
TREND_CONF = {
    "stable": {
        "colour": "text-info",
        "icon": "bi bi-dash",
        "tooltip": gettext("Stable with respect to yesterday")
    },
    "increase": {
        "colour": "text-danger",
        "icon": "bi bi-arrow-up-right",
        "tooltip": gettext("Increased with respect to yesterday")
    },
    "increase_inverted": {
        "colour": "text-success",
        "icon": "bi bi-arrow-up-right",
        "tooltip": gettext("Increased with respect to yesterday")
    },
    "decrease": {
        "colour": "text-success",
        "icon": "bi bi-arrow-down-left",
        "tooltip": gettext("Decreased with respect to yesterday")
    },
    "decrease_inverted": {
        "colour": "text-danger",
        "icon": "bi bi-arrow-down-left",
        "tooltip": gettext("Decreased with respect to yesterday")
    }
}
VARS_CONF = OrderedDict()
# Daily variables
VARS_CONF[NEW_POSITIVE_KEY] = {
    "title": gettext("New Positive"),
    "desc": gettext("Daily count of new positive cases"),
    "longdesc": gettext("Daily count of new positive cases"),
    "icon": "fas fa-head-side-cough",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[DAILY_ICU_KEY] = {
    "title": gettext("Daily ICU"),
    "desc": gettext("# of people daily admitted in ICU"),
    "longdesc": gettext("Daily count of people in ICU"),
    "icon": "fas fa-procedures",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[DAILY_DEATHS_KEY] = {
    "title": gettext("Daily Deaths"),
    "desc": gettext("Daily deaths count"),
    "longdesc": gettext(
        "Daily deaths count"
    ),
    "icon": "fas fa-cross",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[DAILY_SWABS_KEY] = {
    "title": gettext("Daily Swabs"),
    "desc": gettext("# of swabs performed daily"),
    "longdesc": gettext(
        "Daily number of swabs performed"
    ),
    "icon": "fas fa-vial",
    "increase": TREND_CONF["increase_inverted"],
    "decrease": TREND_CONF["decrease_inverted"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[DAILY_HOSPITALIZED_KEY] = {
    "title": gettext("Daily Hospitalized"),
    "desc": gettext("# of people daily hospitalized"),
    "longdesc": gettext(
        "Daily count of people currently hospitalized. "
        "It takes into account ICU"),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[NEW_POSITIVE_MA_KEY] = {
    "title": gettext("New Positive (7-day MA)"),
    "desc": gettext("Daily count of new positve cases"),
    "longdesc": gettext("Daily count of new positve cases"),
    "icon": "fas fa-head-side-cough",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[DAILY_DEATHS_MA_KEY] = {
    "title": gettext("Daily Deaths (7-day MA)"),
    "desc": gettext("Daily deaths count"),
    "longdesc": gettext(
        "Daily deaths count"
    ),
    "icon": "fas fa-cross",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[DAILY_ICU_MA_KEY] = {
    "title": gettext("Daily ICU (7-day MA)"),
    "desc": gettext("# of people daily admitted in ICU"),
    "longdesc": gettext("Daily count of people in ICU"),
    "icon": "fas fa-procedures",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[DAILY_SWABS_MA_KEY] = {
    "title": gettext("Daily Swabs (7-day MA)"),
    "desc": gettext("# of swabs performed daily"),
    "longdesc": gettext(
        "Daily number of swabs performed"
    ),
    "icon": "fas fa-vial",
    "increase": TREND_CONF["increase_inverted"],
    "decrease": TREND_CONF["decrease_inverted"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}
VARS_CONF[DAILY_HOSPITALIZED_MA_KEY] = {
    "title": gettext("Daily Hospitalized (7-day MA)"),
    "desc": gettext("# of people daily hospitalized"),
    "longdesc": gettext(
        "Daily count of people currently hospitalized. "
        "It takes into account ICU"),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "daily"
}

# Current-state variables
VARS_CONF[TOTAL_POSITIVE_KEY] = {
    "title": gettext("Total Positive"),
    "desc": gettext(
        "# of people currently "
        "hospitalized with symptoms + ICU + self isolation"
    ),
    "longdesc": gettext(
        "People currently positive. "
        "Unlike 'Total Cases' it does not take into account "
        "'healed' and 'deaths'. By the end of the outbreak "
        "this should tend to zero. In particular, it is: "
        "total positive = total cases - total healed - total deaths"
    ),
    "icon": "fas fa-viruses",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "current"
}
VARS_CONF[ICU_KEY] = {
    "title": gettext("Intensive Care Unit"),
    "desc": gettext("# of people currently in ICU"),
    "longdesc": gettext(
        "Total count of people currently in ICU and positive to COVID-19"
    ),
    "icon": "fas fa-procedures",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "current"
}
VARS_CONF[HOSPITALIZED_WITH_SYMPTOMS_KEY] = {
    "title": gettext("Hospitalized With Symptoms"),
    "desc": gettext(
        "# of people currently hospitalized with symptoms"
    ),
    "longdesc": gettext(
        "Total count of people currently in hospital "
        "due to coronavirus with symptoms"
    ),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "current"
}

VARS_CONF[TOTAL_HOSPITALIZED_KEY] = {
    "title": gettext("Total Hospitalized"),
    "desc": gettext("# of people currently hospitalized"),
    "longdesc": gettext(
        "Total count of people currently hospitalized. "
        "It takes into account ICU"),
    "icon": "fas fa-hospital-symbol",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "current"
}
VARS_CONF[SELF_ISOLATION_KEY] = {
    "title": gettext("Self Isolation"),
    "desc": gettext("# of people currently in self isolation"),
    "longdesc": gettext(
        "People currently positive but who do not need hospitalization"
    ),
    "icon": "fas fa-house-user",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "current"
}

# Cumulative variables
VARS_CONF[TOTAL_CASES_KEY] = {
    "title": gettext("Total Cases"),
    "desc": gettext(
        "Total count of the positive tests since the"
        " beginning of the outbreak"
    ),
    "longdesc": gettext(
        "Total count of the positive tests since the"
        " beginning of the outbreak"
    ),
    "icon": "fas fa-viruses",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "cum"
}
VARS_CONF[TOTAL_DEATHS_KEY] = {
    "title": gettext("Total Deaths"),
    "desc": gettext("Total deaths count"),
    "longdesc": gettext(
        "Total deaths count since the beginning of the outbreak"
    ),
    "icon": "fas fa-cross",
    "increase": TREND_CONF["increase"],
    "decrease": TREND_CONF["decrease"],
    "stable": TREND_CONF["stable"],
    "type": "cum"
}

VARS_CONF[TOTAL_SWABS_KEY] = {
    "title": gettext("Total Swabs"),
    "desc": gettext("# of swabs performed"),
    "longdesc": gettext(
        "Total number of swabs performed since the beginning of the outbreak"
    ),
    "icon": "fas fa-vial",
    "increase": TREND_CONF["increase_inverted"],
    "decrease": TREND_CONF["decrease_inverted"],
    "stable": TREND_CONF["stable"],
    "type": "cum"
}
VARS_CONF[TOTAL_HEALED_KEY] = {
    "title": gettext("Total Healed"),
    "desc": gettext("Cumulative # of people healed"),
    "longdesc": gettext(
        "Total number of people healed since the beginning of the outbreak"
    ),
    "icon": "fas fa-smile",
    "increase": TREND_CONF["increase_inverted"],
    "decrease": TREND_CONF["decrease_inverted"],
    "stable": TREND_CONF["stable"],
    "type": "cum"
}

# Vax variables
VARS_CONF[HEALTHCARE_PERS_KEY] = {
    "title": gettext("Healthcare Personnel"),
    "type": "vax"
}
VARS_CONF[NONHEALTHCARE_PERS_KEY] = {
    "title": gettext("Non-healthcare Personnel"),
    "type": "vax"
}
VARS_CONF[HFE_GUESTS_KEY] = {
    "title": gettext("HFE Guests"),
    "type": "vax"
}
VARS_CONF[OVER_80_KEY] = {
    "title": gettext("Over 80"),
    "type": "vax"
}
VARS_CONF[OTHER_KEY] = {
    "title": gettext("Other"),
    "type": "vax"
}
VARS_CONF[ARMED_FORCES_KEY] = {
    "title": gettext("Armed Forces"),
    "type": "vax"
}
VARS_CONF[SCHOOL_PERS_KEY] = {
    "title": gettext("School personnel"),
    "type": "vax"
}
VARS_CONF[VAX_FIRST_DOSE_KEY] = {
    "title": gettext("Daily First administrations"),
    "icon": "fas fa-check",
    "increase": TREND_CONF["increase_inverted"],
    "decrease": TREND_CONF["decrease_inverted"],
    "stable": TREND_CONF["stable"],
    "type": "vax"
}
VARS_CONF[VAX_SECOND_DOSE_KEY] = {
    "title": gettext("Daily Second administrations"),
    "icon": "fas fa-check-double",
    "increase": TREND_CONF["increase_inverted"],
    "decrease": TREND_CONF["decrease_inverted"],
    "stable": TREND_CONF["stable"],
    "type": "vax"
}
LANGUAGES = {
    "en": "English",
    "it_IT": "Italiano"
}
ITALY_MAP = {
    'Abruzzo': ['Chieti', "L'Aquila", 'Pescara', 'Teramo'],
    'Basilicata': ['Matera', 'Potenza'],
    'Calabria': ['Catanzaro',
                 'Cosenza',
                 'Crotone',
                 'Reggio di Calabria',
                 'Vibo Valentia'],
    'Campania': ['Avellino', 'Benevento', 'Caserta', 'Napoli', 'Salerno'],
    'Emilia-Romagna': ['Bologna',
                       'Ferrara',
                       'Forlì-Cesena',
                       'Modena',
                       'Parma',
                       'Piacenza',
                       'Ravenna',
                       "Reggio nell'Emilia",
                       'Rimini'],
    'Friuli Venezia Giulia': ['Gorizia', 'Pordenone', 'Trieste', 'Udine'],
    'Lazio': ['Frosinone', 'Latina', 'Rieti', 'Roma', 'Viterbo'],
    'Liguria': ['Genova', 'Imperia', 'La Spezia', 'Savona'],
    'Lombardia': ['Bergamo',
                  'Brescia',
                  'Como',
                  'Cremona',
                  'Lecco',
                  'Lodi',
                  'Mantova',
                  'Milano',
                  'Monza e della Brianza',
                  'Pavia',
                  'Sondrio',
                  'Varese'],
    'Marche': ['Ancona', 'Ascoli Piceno', 'Fermo', 'Macerata',
               'Pesaro e Urbino'],
    'Molise': ['Campobasso', 'Isernia'],
    'Piemonte': ['Alessandria',
                 'Asti',
                 'Biella',
                 'Cuneo',
                 'Novara',
                 'Torino',
                 'Verbano-Cusio-Ossola',
                 'Vercelli'],
    'Puglia': ['Bari',
               'Barletta-Andria-Trani',
               'Brindisi',
               'Lecce',
               'Foggia',
               'Taranto'],
    'Sardegna': ['Cagliari',
                 'Nuoro',
                 'Sassari',
                 'Sud Sardegna'],
    'Sicilia': ['Agrigento',
                'Caltanissetta',
                'Catania',
                'Enna',
                'Messina',
                'Palermo',
                'Ragusa',
                'Siracusa',
                'Trapani'],
    'Toscana': ['Arezzo',
                'Firenze',
                'Grosseto',
                'Livorno',
                'Lucca',
                'Massa Carrara',
                'Pisa',
                'Pistoia',
                'Prato',
                'Siena'],
    'P.A. Bolzano': [],
    'P.A. Trento': [],
    'Umbria': ['Perugia', 'Terni'],
    "Valle d'Aosta": ['Aosta'],
    'Veneto': ['Belluno',
               'Padova',
               'Rovigo',
               'Treviso',
               'Venezia',
               'Verona',
               'Vicenza']
}
REGIONS = [key for key in ITALY_MAP]
PROVINCES = [p for pp in ITALY_MAP.values() for p in pp]
ITALY_POPULATION = {
    'Piemonte': 4311217,
    "Valle d'Aosta": 125034,
    'Lombardia': 10027602,
    'P.A. Bolzano': 532250,
    'P.A. Trento': 542214,
    'Veneto': 4879133,
    'Friuli Venezia Giulia': 1206216,
    'Liguria': 1524826,
    'Emilia-Romagna': 4464119,
    'Toscana': 3692555,
    'Umbria': 870165,
    'Marche': 1512672,
    'Lazio': 5755700,
    'Abruzzo': 1293941,
    'Molise': 300516,
    'Campania': 5712143,
    'Puglia': 3953305,
    'Basilicata': 553254,
    'Calabria': 1894110,
    'Sicilia': 4875290,
    'Sardegna': 1611621,
    'Italia': 59641488
}
PC_TO_OD_MAP = {
    'Italia': 'ITA',
    'Abruzzo': 'ABR',
    'Basilicata': 'BAS',
    'Calabria': 'CAL',
    'Campania': 'CAM',
    'Emilia-Romagna': 'EMR',
    'Friuli Venezia Giulia': 'FVG',
    'Lazio': 'LAZ',
    'Liguria': 'LIG',
    'Lombardia': 'LOM',
    'Marche': 'MAR',
    'Molise': 'MOL',
    'P.A. Bolzano': 'PAB',
    'P.A. Trento': 'PAT',
    'Piemonte': 'PIE',
    'Puglia': 'PUG',
    'Sardegna': 'SAR',
    'Sicilia': 'SIC',
    'Toscana': 'TOS',
    'Umbria': 'UMB',
    "Valle d'Aosta": 'VDA',
    'Veneto': 'VEN',
}
OD_TO_PC_MAP = {
    'ITA': 'Italia',
    'ABR': 'Abruzzo',
    'BAS': 'Basilicata',
    'CAL': 'Calabria',
    'CAM': 'Campania',
    'EMR': 'Emilia-Romagna',
    'FVG': 'Friuli Venezia Giulia',
    'LAZ': 'Lazio',
    'LIG': 'Liguria',
    'LOM': 'Lombardia',
    'MAR': 'Marche',
    'MOL': 'Molise',
    'PAB': 'P.A. Bolzano',
    'PAT': 'P.A. Trento',
    'PIE': 'Piemonte',
    'PUG': 'Puglia',
    'SAR': 'Sardegna',
    'SIC': 'Sicilia',
    'TOS': 'Toscana',
    'UMB': 'Umbria',
    'VDA': "Valle d'Aosta",
    'VEN': 'Veneto'
}
