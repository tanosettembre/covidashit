"""
Data Module
"""
import datetime as dt

import pandas as pd
import pytz
import requests
from flask import current_app as app
from flask_babel import gettext

from app.db_utils import (
    nat_data_coll, nat_trends_coll, nat_series_coll, reg_data_coll,
    reg_trends_coll, reg_series_coll, reg_bdown_coll, prov_data_coll,
    prov_trends_coll, prov_series_coll, prov_bdown_coll, vax_admins_coll,
    vax_admins_summary_coll, it_pop_coll
)
from app.utils import rubbish_notes, translate_series_lang
from settings import (
    VERSION, KEY_PERIODS, ITALY_MAP, REGIONS, PROVINCES,
    OD_TO_PC_MAP
)
from settings.urls import URL_VAX_LATEST_UPDATE, URL_VAX_SUMMARY_DATA
from settings.vars import (
    NEW_POSITIVE_KEY, TOTAL_CASES_KEY, DAILY_POSITIVITY_INDEX, REGION_KEY,
    PROVINCE_KEY, VAX_LATEST_UPDATE_KEY, VAX_DATE_FMT, CHART_DATE_FMT,
    UPDATE_FMT, VAX_UPDATE_FMT, DATE_KEY, NOTE_KEY, VAX_DATE_KEY, VAX_AREA_KEY,
    VAX_AGE_KEY, POP_KEY, ADMINS_DOSES_KEY, DELIVERED_DOSES_KEY,
    VAX_ADMINS_PERC_KEY, VAX_TOT_ADMINS_KEY, VAX_FIRST_DOSE_KEY,
    VAX_SECOND_DOSE_KEY, VAX_PROVIDER_KEY, HEALTHCARE_PERS_KEY,
    NONHEALTHCARE_PERS_KEY, HFE_GUESTS_KEY, OVER_80_KEY, OTHER_KEY,
    ARMED_FORCES_KEY, SCHOOL_PERS_KEY, VARS, POP_ISTAT_KEY
)

DATA_SERIES = [VARS[key]["title"] for key in VARS]
DASHBOARD_DATA = {
    "vars_config": VARS,
    "data_series": DATA_SERIES,
    "italy_map": ITALY_MAP,
    "VERSION": VERSION,
    "regions": REGIONS,
    "provinces": PROVINCES,
    "key_periods": KEY_PERIODS
}

CUM_QUANTITIES = [qty for qty in VARS if VARS[qty]["type"] == "cum"]
NON_CUM_QUANTITIES = [qty for qty in VARS if VARS[qty]["type"] == "current"]
DAILY_QUANTITIES = [qty for qty in VARS if VARS[qty]["type"] == "daily"]
TREND_CARDS = [
    qty for qty in VARS
    if not qty.endswith("_ma") and VARS[qty]["type"] != "vax"
]
PROV_TREND_CARDS = [TOTAL_CASES_KEY, NEW_POSITIVE_KEY]
VAX_PEOPLE_CATEGORIES = [
    HEALTHCARE_PERS_KEY, NONHEALTHCARE_PERS_KEY, HFE_GUESTS_KEY, OVER_80_KEY,
    OTHER_KEY, ARMED_FORCES_KEY, SCHOOL_PERS_KEY
]


def get_query_menu(area=None):
    """
    Return the query menu
    :param area: str
    :return: dict
    """
    return {
        "national": {
            "query": {},
            "collection": nat_data_coll
        },
        "regional": {
            "query": {REGION_KEY: area},
            "collection": reg_data_coll
        },
        "provincial": {
            "query": {PROVINCE_KEY: area},
            "collection": prov_data_coll
        }
    }


def get_notes(notes_type="national", area=None):
    """
    Return the notes in the data otherwise empty string when
    the received note is 0 or matches the RUBBISH_NOTE_REGEX
    :param notes_type: str
    :param area: str
    :return: str
    """
    query_menu = get_query_menu(area)
    query = query_menu[notes_type]["query"]
    collection = query_menu[notes_type]["collection"]
    notes = ""
    try:
        doc = next(collection.find(query).sort([(DATE_KEY, -1)]).limit(1))
        notes = doc[NOTE_KEY] if doc[NOTE_KEY] != 0 else None
    except StopIteration:
        app.logger.error("While getting notes: no data")
    return notes if notes is not None and not rubbish_notes(notes) else ""


def get_national_trends():
    """Return national trends from DB"""
    return sorted(
        list(nat_trends_coll.find({})),
        key=lambda x: list(VARS.keys()).index(x['id'])
    )


def get_regional_trends(region):
    """
    Return a list of regional trends for a given region
    :param region: str
    :return: list
    """
    trends = []
    doc = reg_trends_coll.find_one({REGION_KEY: region})
    if doc:
        trends = doc["trends"]
    return trends


def get_provincial_trends(province):
    """
    Return a list of provincial trends for a given province
    :param province: str
    :return: list
    """
    doc = prov_trends_coll.find_one({PROVINCE_KEY: province})
    return doc["trends"]


def get_regional_breakdown():
    """Return regional breakdown from DB"""
    doc = reg_bdown_coll.find_one({}, {"_id": False})
    if doc:
        breakdown = {
            key: sorted(doc[key], key=lambda x: x['count'], reverse=True)
            for key in doc
        }
    else:
        breakdown = {"err": "No data"}
    return breakdown


def get_provincial_breakdown(region):
    """Return provincial breakdown from DB"""
    b = {}
    doc = prov_bdown_coll.find_one({REGION_KEY: region}, {"_id": False})
    if doc:
        b = doc["breakdowns"]
        for key in b.keys():
            b[key] = sorted(b[key], key=lambda x: x['count'], reverse=True)
    return b


def get_national_series():
    """Return national series from DB"""
    series = nat_series_coll.find_one({}, {"_id": False})
    if series:
        data = translate_series_lang(series)
    else:
        data = {"err": "No data"}
    return data


def get_regional_series(region):
    """Return regional series from DB"""
    data = {}
    series = reg_series_coll.find_one({REGION_KEY: region}, {"_id": False})
    if series:
        data = translate_series_lang(series)
    return data


def get_provincial_series(province):
    """Return provincial series from DB"""
    series = prov_series_coll.find_one(
        {PROVINCE_KEY: province}, {"_id": False})
    return translate_series_lang(series)


def get_positivity_idx(area_type="national", area=None):
    """
    Return the positivity index for either the national or the regional
    views
    :param area_type: str: "national" or "regional"
    :param area: str
    :return: str
    """
    query_menu = get_query_menu(area)
    query = query_menu[area_type]["query"]
    collection = query_menu[area_type]["collection"]
    try:
        doc = next(collection.find(query).sort([(DATE_KEY, -1)]).limit(1))
        idx = f"{round(doc[DAILY_POSITIVITY_INDEX])}%"
    except StopIteration:
        app.logger.error("While getting positivity idx: no data")
        idx = "n/a"
    return idx


def get_national_data():
    """Return a data frame of the national data from DB"""
    cursor = nat_data_coll.find({})
    df = pd.DataFrame(list(cursor))
    if df.empty:
        app.logger.error("While getting national data: no data")
    return df


def get_region_data(region):
    """Return a data frame for a given region from the regional collection"""
    cursor = reg_data_coll.find({REGION_KEY: region})
    df = pd.DataFrame(list(cursor))
    if df.empty:
        app.logger.error(f"While getting {region} data: no data")
    return df


def get_province_data(province):
    """
    Return a data frame for a given province from the provincial collection
    """
    cursor = prov_data_coll.find({PROVINCE_KEY: province})
    df = pd.DataFrame(list(cursor))
    if df.empty:
        app.logger.error(f"While getting {province} data: no data")
    return df


def get_latest_update(data_type="national"):
    """
    Return the value of the key PCM_DATE_KEY of the last dict in data
    :return: str
    """
    query_menu = get_query_menu()
    collection = query_menu[data_type]["collection"]
    try:
        doc = next(collection.find({}).sort([(DATE_KEY, -1)]).limit(1))
        latest_update = doc[DATE_KEY].strftime(UPDATE_FMT)
    except StopIteration:
        app.logger.error("While getting latest update: no data")
        latest_update = "n/a"
    return latest_update


def get_latest_vax_update():
    """Return the lastest update dt"""
    try:
        response = requests.get(URL_VAX_LATEST_UPDATE).json()
        datestr = response[VAX_LATEST_UPDATE_KEY]
        date_dt = dt.datetime.strptime(datestr, VAX_DATE_FMT)
        cet_dt = date_dt.astimezone(pytz.timezone('Europe/Rome'))
        latest_update = cet_dt.strftime(VAX_UPDATE_FMT)
    except Exception as e:
        app.logger.error(f"While getting latest vax update dt: {e}")
        latest_update = "n/a"
    return latest_update


def get_perc_pop_vax(population, area=None):
    """
    Return the ratio tot administrations / population rounded to 2 figs
    :param population: int
    :param area: str
    :return: float
    """
    tot_1st_admins = get_tot_admins(dtype=VAX_FIRST_DOSE_KEY, area=area)
    tot_2nd_admins = get_tot_admins(dtype=VAX_SECOND_DOSE_KEY, area=area)
    return {
        'first': round(((int(tot_1st_admins) / population) * 100), 1),
        'second': round(((int(tot_2nd_admins) / population) * 100), 1)
    }


def enrich_frontend_data(area=None, **data):
    """
    Return a data dict to be rendered which is an augmented copy of
    DASHBOARD_DATA defined in constants.py
    :param area: optional, str
    :param data: **kwargs
    :return: dict
    """
    try:
        data["area"] = area
    except KeyError:
        pass
    data.update(DASHBOARD_DATA)
    return data


def get_tot_admins(dtype, area=None):
    """
    Return the total of one of the three main vaccine data types
    allowed_types (VAX_TOT_ADMINS_KEY, VAX_FIRST_DOSE_KEY, VAX_SECOND_DOSE_KEY)
    :param dtype: str: must be in allowed_types
    :param area: str: region
    :return: int: the total administrations of a given data type
        if the data type is in allowed_types else 0
    """
    allowed_types = (
        VAX_TOT_ADMINS_KEY, VAX_FIRST_DOSE_KEY, VAX_SECOND_DOSE_KEY)
    tot_adms = 0
    if dtype in allowed_types:
        if area:
            pipe = [
                {'$match': {VAX_AREA_KEY: area}},
                {
                    '$group': {
                        '_id': f'${VAX_AREA_KEY}',
                        'tot': {
                            '$sum': f'${dtype}'
                        }
                    }
                }
            ]
        else:
            pipe = [{'$group': {'_id': '{}', 'tot': {'$sum': f'${dtype}'}}}]
        try:
            cursor = vax_admins_summary_coll.aggregate(pipeline=pipe)
            tot_adms = next(cursor)['tot']
        except Exception as e:
            app.logger.error(f"While getting total admins: {e}")
    return int(tot_adms)


def get_age_chart_data(area=None):
    """Return age series data"""
    chart_data = {}
    match = {'$match': {VAX_AREA_KEY: area}}
    group = {
        '$group': {
            '_id': f'${VAX_AGE_KEY}',
            'tot': {'$sum': f'${VAX_TOT_ADMINS_KEY}'}
        }
    }
    sort = {'$sort': {'_id': 1}}
    try:
        if area is not None:
            pipe = [match, group, sort]
        else:
            pipe = [group, sort]
        cursor = vax_admins_coll.aggregate(pipeline=pipe)
        data = list(cursor)
        df = pd.DataFrame(data)
        categories = df['_id'].values.tolist()
        admins_per_age = df['tot'].values.tolist()
        chart_data = {
            "categories": categories,
            "admins_per_age": [{
                'name': gettext("Doses administered"),
                'data': admins_per_age
            }]
        }
    except Exception as e:
        app.logger.error(f"While getting age chart data: {e}")
    return chart_data


def get_category_chart_data(area=None):
    """Return category series data"""
    chart_data = []
    if area is not None:
        match = {'$match': {VAX_AREA_KEY: area}}
        group = {
            '$group': {
                '_id': f'${VAX_AREA_KEY}',
                HEALTHCARE_PERS_KEY: {'$sum': f'${HEALTHCARE_PERS_KEY}'},
                NONHEALTHCARE_PERS_KEY: {'$sum': f'${NONHEALTHCARE_PERS_KEY}'},
                HFE_GUESTS_KEY: {'$sum': f'${HFE_GUESTS_KEY}'},
                OVER_80_KEY: {'$sum': f'${OVER_80_KEY}'},
                OTHER_KEY: {'$sum': f'${OTHER_KEY}'},
                ARMED_FORCES_KEY: {'$sum': f'${ARMED_FORCES_KEY}'},
                SCHOOL_PERS_KEY: {'$sum': f'${SCHOOL_PERS_KEY}'},
            }
        }
        pipe = [match, group]
    else:
        group = {
            '$group': {
                '_id': '',
                HEALTHCARE_PERS_KEY: {'$sum': f'${HEALTHCARE_PERS_KEY}'},
                NONHEALTHCARE_PERS_KEY: {'$sum': f'${NONHEALTHCARE_PERS_KEY}'},
                HFE_GUESTS_KEY: {'$sum': f'${HFE_GUESTS_KEY}'},
                OVER_80_KEY: {'$sum': f'${OVER_80_KEY}'},
                OTHER_KEY: {'$sum': f'${OTHER_KEY}'},
                ARMED_FORCES_KEY: {'$sum': f'${ARMED_FORCES_KEY}'},
                SCHOOL_PERS_KEY: {'$sum': f'${SCHOOL_PERS_KEY}'},
            }
        }
        pipe = [group]
    try:
        cursor = vax_admins_summary_coll.aggregate(pipeline=pipe)
        doc = next(cursor)
        app.logger.debug(f"Category chart data: f{doc}")
        chart_data = [
            {'name': gettext(VARS[cat]["title"]), 'y': doc[cat]}
            for cat in VAX_PEOPLE_CATEGORIES
        ]
    except Exception as e:
        app.logger.error(f"While getting category-chart data: {e}")
    return chart_data


def get_region_chart_data(tot_admins=1):
    """Return administrations data per region"""
    chart_data = {}
    try:
        pipe = [
            {
                '$match': {
                    VAX_AREA_KEY: {
                        '$not': {
                            '$eq': 'ITA'
                        }
                    }
                }
            },
            {
                '$group': {
                    '_id': f'${VAX_AREA_KEY}',
                    'tot': {'$sum': f'${VAX_TOT_ADMINS_KEY}'}
                }
            },
            {'$sort': {'tot': -1}}
        ]
        cursor = vax_admins_summary_coll.aggregate(pipeline=pipe)
        data = list(cursor)
        app.logger.debug(f"Per region data: {data}")
        df = pd.DataFrame(data)
        df['region'] = df['_id'].apply(lambda x: OD_TO_PC_MAP[x])
        df['exp_admins'] = df['region'].apply(
            lambda x: exp_tot_admins(x, tot_admins))
        chart_data = {
            "categories": df['region'].values.tolist(),
            "admins_per_region": {
                'name': gettext("Real"),
                'data': df['tot'].values.tolist()
            },
            "expected_admins": {
                'name': gettext("Expected"),
                'data': df['exp_admins'].values.tolist()
            }
        }
    except Exception as e:
        app.logger.error(f"While getting region chart data: {e}")
    return chart_data


def exp_tot_admins(x, tot_admins):
    """Return tot administration scaled to the region pop percentage"""
    it_population = get_it_pop_dict()
    return round(
        it_population[x] / it_population['Italia'] * tot_admins)


def pop_perc(x):
    """Return percentage of population in a given region"""
    it_population = get_it_pop_dict()
    return round(it_population[x] / it_population['Italia'] * 100, 2)


def get_admins_perc(area=None):
    """
    Return the percentage of administered doses wrt the delivered ones.
    It uses the CSV Url as it's tiny.
    :param area: optional str
    :return: float
    """
    admins_perc = "n/a"
    try:
        df = pd.read_csv(URL_VAX_SUMMARY_DATA)
        if area is None:
            admins_perc = round(
                (df[ADMINS_DOSES_KEY].sum() /
                 df[DELIVERED_DOSES_KEY].sum() * 100), 1)
        else:
            df = df[df[VAX_AREA_KEY] == area]
            admins_perc = df[VAX_ADMINS_PERC_KEY].values[0]
    except Exception as e:
        app.logger.error(f"While getting % administered doses: {e}")
    return admins_perc


def get_admins_timeseries_chart_data():
    """
    Return admins timeseries data to frontend
    :return: dict
    """
    chart_data = {}
    try:
        pipe = [
            {'$match': {VAX_AREA_KEY: {'$ne': 'ITA'}}},
            {'$sort': {VAX_DATE_KEY: 1}}
        ]
        cursor = vax_admins_summary_coll.aggregate(pipeline=pipe)
        data = list(cursor)
        df = pd.DataFrame(data)
        dates = df[VAX_DATE_KEY].apply(
            lambda x: x.strftime(CHART_DATE_FMT)).unique().tolist()
        data = [{
            'name': OD_TO_PC_MAP[r],
            'data': (
                    df[df[VAX_AREA_KEY] == r][VAX_FIRST_DOSE_KEY].cumsum() /
                    df[df[VAX_AREA_KEY] == r][POP_KEY] * 100
            ).round(2).to_list()
        } for r in sorted(df[VAX_AREA_KEY].unique())]
        chart_data = {
            "dates": dates,
            "data": data
        }
        app.logger.debug(f"Time series chart data {chart_data}")
    except Exception as e:
        app.logger.error(f"While getting vax timeseries chart data {e}")
    return chart_data


def get_admins_per_provider_chart_data(area=None):
    """
    Return provider pie-chart data for highcharts
    :return:
    """
    group = {
        '$group': {
            '_id': f'${VAX_PROVIDER_KEY}',
            'tot': {
                '$sum': f'${VAX_TOT_ADMINS_KEY}'
            }
        }
    }
    sort = {'$sort': {'tot': -1}}
    if area is not None:
        match = {'$match': {VAX_AREA_KEY: area}}
        pipe = [match, group, sort]
    else:
        pipe = [group, sort]
    data = list(vax_admins_coll.aggregate(pipeline=pipe))
    return [{'name': d['_id'], 'y': d['tot']} for d in data]


def get_vax_trends_data(area=None):
    """
    Return the first- and second-dose data in the last two days
    :param area: optional, str
    :return: list of dicts
    """
    if area is None:
        pipe = [
            {
                '$group': {
                    '_id': f'${VAX_DATE_KEY}',
                    VAX_FIRST_DOSE_KEY: {'$sum': f'${VAX_FIRST_DOSE_KEY}'},
                    VAX_SECOND_DOSE_KEY: {'$sum': f'${VAX_SECOND_DOSE_KEY}'}
                }
            },
            {"$sort": {"_id": -1}},
            {'$limit': 2}
        ]
    else:
        pipe = [
            {'$match': {VAX_AREA_KEY: area}},
            {
                '$group': {
                    '_id': f'$data_somministrazione',
                    VAX_FIRST_DOSE_KEY: {'$sum': f'${VAX_FIRST_DOSE_KEY}'},
                    VAX_SECOND_DOSE_KEY: {'$sum': f'${VAX_SECOND_DOSE_KEY}'}
                }
            },
            {"$sort": {"_id": -1}},
            {'$limit': 2}
        ]
    data = list(vax_admins_coll.aggregate(pipeline=pipe))
    return data


def get_vax_trends(area=None):
    """
    Return the vax-trends array
    :param area: optional, str
    :return: list of dicts
    """
    data = get_vax_trends_data(area)
    trends = []
    for d in (VAX_FIRST_DOSE_KEY, VAX_SECOND_DOSE_KEY):
        count = data[0][d]
        yesterday_count = data[1][d]
        diff = count - yesterday_count
        if diff > 0:
            status = 'increase'
        elif diff < 0:
            status = 'decrease'
        else:
            status = 'stable'
        try:
            perc = '{}%'.format(round(diff / data[1][d] * 100, 1))
        except ValueError:
            perc = 'n/a'
        trends.append({
            'id': d,
            'yesterday_count': "{:,d}".format(yesterday_count),
            'percentage': perc,
            'title': VARS[d]["title"],
            "colour": VARS[d][status]["colour"],
            "icon": VARS[d]["icon"],
            "status_icon": VARS[d][status]["icon"],
            'count': "{:,d}".format(count)
        })
    return trends


def get_it_pop_dict():
    """
    Return a region:population dict
    :return: dict
    """
    it_pop_dict = {}
    try:
        records = list(it_pop_coll.find({}))
        it_pop_dict = {
            r[REGION_KEY]: r[POP_ISTAT_KEY]
            for r in records
        }
    except Exception as e:
        app.logger.error(f"While getting IT pop dict: {e}")
    return it_pop_dict
