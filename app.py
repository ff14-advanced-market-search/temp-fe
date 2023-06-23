from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)


def str_to_bool(bool_str):
    if bool_str == "True":
        return True
    else:
        return False


@app.route("/", methods=["GET", "POST"])
def root():
    return render_template("index.html", len=len)


@app.route("/wow/uploadtimers", methods=["GET", "POST"])
def uploadtimers():
    if request.method == "GET":
        return render_template("uploadtimers.html")
    elif request.method == "POST":
        results = []


@app.route("/scan", methods=["GET", "POST"])
def scan():
    if request.method == "GET":
        return render_template("oldscan.html")
    elif request.method == "POST":
        scan_hours = request.form.get("scan_hours")
        sale_amt = request.form.get("sale_amt")
        roi = request.form.get("roi")
        home_server = request.form.get("home_server")
        stack_size = request.form.get("stack_size")
        hq_only = request.form.get("hq_only")
        profit_amt = request.form.get("profit_amt")
        min_desired_avg_ppu = request.form.get("min_desired_avg_ppu")
        game_wide = request.form.get("game_wide")
        include_vendor = request.form.get("include_vendor")
        out_stock = request.form.get("out_stock")
        filters = [int(request.form.get("filters"))]

        headers = {"Accept": "application/json"}
        json_data = {
            "preferred_roi": int(roi),
            "min_profit_amount": int(profit_amt),
            "min_desired_avg_ppu": int(min_desired_avg_ppu),
            "min_stack_size": int(stack_size),
            "hours_ago": int(scan_hours),
            "min_sales": int(sale_amt),
            "hq": str_to_bool(hq_only),
            "home_server": home_server,
            "filters": filters,
            "region_wide": str_to_bool(game_wide),
            "include_vendor": str_to_bool(include_vendor),
            "show_out_stock": str_to_bool(out_stock),
            "universalis_list_uid": "",
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/scan/",
            headers=headers,
            json=json_data,
        ).json()["data"]

        fieldnames = list(response[0].keys())

        return render_template(
            "oldscan.html", results=response, fieldnames=fieldnames, len=len
        )


if __name__ == "__main__":
    ## http
    app.run(host="0.0.0.0", debug=True)

    # ## https
    # app.run(host='0.0.0.0',port=443,debug=True, ssl_context=("./certs/full_chain.crt","./certs/private.key"))
