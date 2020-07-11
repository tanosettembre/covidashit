from flask import jsonify

from config import COLLECTION_NAME, BARCHART_RACE_QUERY, UPDATE_FMT
from app.api import api


@api.route("/get_bcr")
def get_bcr():
    from app import mongo
    bcr_data = next(
        mongo.db[COLLECTION_NAME].find(BARCHART_RACE_QUERY)
    )
    bcr_html = bcr_data["html_str"]
    bcr_ts = bcr_data["ts"].strftime(UPDATE_FMT)
    return jsonify(html=bcr_html, ts=bcr_ts)