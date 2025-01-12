"""
Pandemic blueprint views
"""
import time

from flask import render_template, redirect
from flask_babel import gettext

from app.data import (
    get_notes, get_national_trends, get_regional_trends,
    get_provincial_trends, get_regional_breakdown, get_provincial_breakdown,
    get_national_series, get_regional_series, get_provincial_series,
    get_positivity_idx, get_latest_update, enrich_frontend_data,
    get_it_pop_dict
)
from app.ui import pandemic
from app.utils import region_of_province
from settings import (
    PAGE_BASE_TITLE, ITALY_MAP, REGIONS, PROVINCES
)

URL_REGIONS = "/regions"
URL_PROVINCES = "/provinces"


@pandemic.route("/national")
def old_national_view():
    """Redirect old national view to home"""
    return redirect('/')


@pandemic.route("/")
def national_view():
    """
    Render the national view
    :return: template
    """
    data_type = "national"
    cards = get_national_trends()
    breakdown = get_regional_breakdown()
    series = get_national_series()
    notes = get_notes(notes_type=data_type)
    updated_at = get_latest_update(data_type=data_type)
    positivity_idx = get_positivity_idx(area_type=data_type)
    population = get_it_pop_dict()['Italia']
    data = enrich_frontend_data(
        page_title=PAGE_BASE_TITLE,
        dashboard_title=gettext("Italy"),
        ts=int(time.time()),
        trend_cards=cards,
        series=series,
        latest_update=updated_at,
        breakdown=breakdown,
        positivity_idx=positivity_idx,
        data_type=data_type,
        notes=notes,
        population="{:,d}".format(population)
    )
    return render_template("pandemic.html", **data)


@pandemic.route(f"{URL_REGIONS}/<region>")
def regional_view(region):
    """
    Render the regional view
    :param region: str: region
    :return: template
    """
    data_type = "regional"
    if region not in REGIONS:
        error = f'Area {region} not found'
        return render_template("errors/404.html", error=error)
    cards = get_regional_trends(region)
    breakdown = get_provincial_breakdown(region=region)
    series = get_regional_series(region=region)
    notes = get_notes(notes_type=data_type, area=region)
    latest_update = get_latest_update(data_type=data_type)
    positivity_idx = get_positivity_idx(area_type=data_type, area=region)
    provinces = ITALY_MAP[region]
    region_index = REGIONS.index(region)
    previous_url = f"{URL_REGIONS}/{REGIONS[region_index - 1]}"
    population = get_it_pop_dict()[region]
    try:
        next_region_url = f"{URL_REGIONS}/{REGIONS[region_index + 1]}"
    except IndexError:
        next_region_url = f"{URL_REGIONS}/{REGIONS[-1]}"
    view_data = dict(
        ts=int(time.time()),
        page_title="{} | {}".format(region, PAGE_BASE_TITLE),
        dashboard_title=region,
        region=region,
        region_provinces=provinces,
        trend_cards=cards,
        breakdown=breakdown,
        positivity_idx=positivity_idx,
        series=series,
        notes=notes,
        previous_area_url=previous_url,
        next_area_url=next_region_url,
        latest_update=latest_update,
        areas_length=len(REGIONS),
        area_index=region_index,
        data_type=data_type,
        cards=cards,
        population="{:,d}".format(population)
    )
    dashboard_data = enrich_frontend_data(area=region, **view_data)
    return render_template("pandemic.html", **dashboard_data)


@pandemic.route(f"{URL_PROVINCES}/<province>")
def provincial_view(province):
    """
    Render the provincial view
    :param province: str
    :return: template
    """
    data_type = "provincial"
    if province not in PROVINCES:
        error = f'Area "{province}" not found.'
        return render_template("errors/404.html", error=error)
    cards = get_provincial_trends(province=province)
    series = get_provincial_series(province=province)
    notes = get_notes(notes_type=data_type, area=province)
    latest_update = get_latest_update(data_type=data_type)
    province_region = region_of_province(province)
    n_provinces = len(ITALY_MAP[province_region])
    provinces = ITALY_MAP[province_region]
    province_index = ITALY_MAP[province_region].index(province)
    previous_url = f"{URL_PROVINCES}/{provinces[province_index - 1]}"
    try:
        next_province_url = f"{URL_PROVINCES}/{provinces[province_index + 1]}"
    except IndexError:
        next_province_url = f"{URL_PROVINCES}/{provinces[-1]}"
    view_data = dict(
        ts=int(time.time()),
        page_title="{} | {}".format(province, PAGE_BASE_TITLE),
        dashboard_title=province,
        province=province,
        region=province_region,
        trend_cards=cards,
        series=series,
        notes=notes,
        previous_area_url=previous_url,
        next_area_url=next_province_url,
        latest_update=latest_update,
        areas_length=n_provinces,
        data_type=data_type,
        area_index=province_index,
    )
    dashboard_data = enrich_frontend_data(area=province, **view_data)
    return render_template("pandemic.html", **dashboard_data)


@pandemic.route("/thanks")
def thanks_view():
    """
    Render the "thank you" view
    :return: HTML
    """
    return render_template("thanks.html")
