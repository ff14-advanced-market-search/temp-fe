import json

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
        ).json()

        if "data" not in response:
            return f"Error no matching data with given inputs {response}"
        response = response["data"]

        fieldnames = list(response[0].keys())

        return render_template(
            "oldscan.html", results=response, fieldnames=fieldnames, len=len
        )


@app.route("/uploadtimers", methods=["GET", "POST"])
def uploadtimers():
    if request.method == "GET":
        return render_template("uploadtimers.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}
        json_data = {}
        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/uploadtimers",
            headers=headers,
            json=json_data,
        ).json()

        if "data" not in response:
            return f"Error no matching data with given inputs {response}"
        response = response["data"]

        for row in response:
            del row["tableName"]
            del row["lastUploadUnix"]

            pop = row["dataSetName"]
            del row["dataSetName"]
            row["dataSetName"] = pop

        fieldnames = list(response[0].keys())

        return render_template(
            "uploadtimers.html", results=response, fieldnames=fieldnames, len=len
        )


@app.route("/itemnames", methods=["GET", "POST"])
def itemnames():
    if request.method == "GET":
        return render_template("itemnames.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}
        json_data = {}
        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/itemnames",
            headers=headers,
            json=json_data,
        ).json()

        resp_list = []
        for k, v in response.items():
            resp_list.append({"id": k, "name": v})

        return render_template(
            "itemnames.html", results=resp_list, fieldnames=["id", "name"], len=len
        )


@app.route("/petshoppinglist", methods=["GET", "POST"])
def petshoppinglist():
    if request.method == "GET":
        return render_template("petshoppinglist.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        json_data = {
            "region": request.form.get("region"),
            "petID": int(request.form.get("petID")),
            "maxPurchasePrice": int(request.form.get("maxPurchasePrice")),
            "connectedRealmIDs": {},
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/petshoppinglist",
            headers=headers,
            json=json_data,
        ).json()

        if "data" not in response:
            return f"Error no matching data with given inputs {response}"
        response = response["data"]

        for row in response:
            link = row["link"]
            del row["link"]
            row["link"] = link

        fieldnames = list(response[0].keys())

        return render_template(
            "petshoppinglist.html", results=response, fieldnames=fieldnames, len=len
        )


@app.route("/petmarketshare", methods=["GET", "POST"])
def petmarketshare():
    if request.method == "GET":
        return render_template("petmarketshare.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        json_data = {
            "region": request.form.get("region"),
            "homeRealmName": request.form.get("homeRealmName"),
            "minPrice": int(request.form.get("minPrice")),
            "salesPerDay": int(request.form.get("salesPerDay")),
            "includeCategories": [],
            "excludeCategories": [],
            "sortBy": "estimatedRegionMarketValue",
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/petmarketshare",
            headers=headers,
            json=json_data,
        ).json()

        if "data" not in response:
            return f"Error no matching data with given inputs {response}"
        response = response["data"]

        for row in response:
            avgTSMPrice = row["avgTSMPrice"]
            estimatedRegionMarketValue = row["estimatedRegionMarketValue"]
            homeMinPrice = row["homeMinPrice"]
            itemID = row["itemID"]
            undermineLink = row["undermineLink"]
            warcraftPetsLink = row["warcraftPetsLink"]
            link = row["link"]

            del row["avgTSMPrice"]
            del row["estimatedRegionMarketValue"]
            del row["homeMinPrice"]
            del row["itemID"]
            del row["link"]
            del row["warcraftPetsLink"]
            del row["undermineLink"]

            row["avgTSMPrice"] = avgTSMPrice
            row["estimatedRevenue"] = estimatedRegionMarketValue
            row["homeMinPrice"] = homeMinPrice
            row["itemID"] = itemID
            row["link"] = link
            row["undermineLink"] = undermineLink
            row["warcraftPetsLink"] = warcraftPetsLink

        fieldnames = list(response[0].keys())

        return render_template(
            "petmarketshare.html", results=response, fieldnames=fieldnames, len=len
        )


@app.route("/petexport", methods=["GET", "POST"])
def petexport():
    if request.method == "GET":
        return render_template("petexport.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        json_data = {
            "region": request.form.get("region"),
            "petID": int(request.form.get("petID")),
            "populationWP": int(request.form.get("populationWP")),
            "populationBlizz": int(request.form.get("populationBlizz")),
            "rankingWP": int(request.form.get("rankingWP")),
            "minPrice": int(request.form.get("minPrice")),
            "maxQuantity": int(request.form.get("maxQuantity")),
            "sortBy": "minPrice",
            "connectedRealmIDs": {},
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/petservers",
            headers=headers,
            json=json_data,
        ).json()

        if "data" not in response:
            return f"Error no matching data with given inputs {response}"
        response = response["data"]

        for row in response:
            del row["connectedRealmID"]
            del row["realmPopulationInt"]
            row["allRealms"] = row["connectedRealmNames"]
            row["connectedRealmNames"] = row["connectedRealmNames"][0]
            link = row["link"]
            del row["link"]
            row["link"] = link
            undermineLink = row["undermineLink"]
            del row["undermineLink"]
            row["undermineLink"] = undermineLink

        fieldnames = list(response[0].keys())

        return render_template(
            "petexport.html", results=response, fieldnames=fieldnames, len=len
        )


@app.route("/regionundercut", methods=["GET", "POST"])
def regionundercut():
    if request.method == "GET":
        return render_template("regionundercut.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        addonData = request.form.get("addonData")
        json_data = {
            "region": request.form.get("region"),
            "homeRealmID": int(request.form.get("homeRealmID")),
            "addonData": json.loads(addonData),
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/regionundercut",
            headers=headers,
            json=json_data,
        ).json()

        if "undercut_list" not in response or "not_found_list" not in response:
            return f"Error no matching data with given inputs, did you pick the right server? {response}"
        undercuts = response["undercut_list"]

        for row in undercuts:
            del row["connectedRealmId"]
            realmName = row["realmName"]
            del row["realmName"]
            row["realmName"] = realmName
            undermineLink = row["link"]
            del row["link"]
            row["undermineLink"] = undermineLink

        undercuts_fieldnames = list(undercuts[0].keys())

        if "not_found_list" not in response:
            return f"Error no matching data with given inputs {response}"
        not_found = response["not_found_list"]

        for row in not_found:
            del row["connectedRealmId"]
            realmName = row["realmName"]
            del row["realmName"]
            row["realmName"] = realmName
            undermineLink = row["link"]
            del row["link"]
            row["undermineLink"] = undermineLink

        not_found_fieldnames = list(not_found[0].keys())

        return render_template(
            "regionundercut.html",
            results=undercuts,
            fieldnames=undercuts_fieldnames,
            results_n=not_found,
            fieldnames_n=not_found_fieldnames,
            len=len,
        )


@app.route("/petimport", methods=["GET", "POST"])
def petimport():
    if request.method == "GET":
        return render_template("petimport.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        petsOnly = request.form.get("petsOnly")
        if petsOnly == "False":
            petsOnly = False
        else:
            petsOnly = True
        json_data = {
            "region": request.form.get("region"),
            "homeRealmID": int(request.form.get("homeRealmID")),
            "ROI": int(request.form.get("ROI")),
            "avgPrice": int(request.form.get("avgPrice")),
            "maxPurchasePrice": int(request.form.get("maxPurchasePrice")),
            "profitAmount": int(request.form.get("profitAmount")),
            "salesPerDay": int(request.form.get("salesPerDay")),
            "includeCategories": [],
            "excludeCategories": [],
            "sortBy": "lowestPrice",
            "petsOnly": petsOnly,
            "connectedRealmIDs": {},
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/petimport",
            headers=headers,
            json=json_data,
        ).json()

        if "data" not in response:
            return f"Error no matching data with given inputs {response}"
        response = response["data"]

        for row in response:
            del row["itemID"]
            del row["lowestPriceRealmID"]
            realm = row["lowestPriceRealmName"]
            del row["lowestPriceRealmName"]
            row["lowestPriceRealmName"] = realm

            link = row["link"]
            del row["link"]
            row["link"] = link

            undermineLink = row["undermineLink"]
            del row["undermineLink"]
            row["undermineLink"] = undermineLink

            warcraftPetsLink = row["warcraftPetsLink"]
            del row["warcraftPetsLink"]
            row["warcraftPetsLink"] = warcraftPetsLink

        fieldnames = list(response[0].keys())

        return render_template(
            "petimport.html",
            results=response,
            fieldnames=fieldnames,
            len=len,
        )


@app.route("/bestdeals", methods=["GET", "POST"])
def bestdeals():
    if request.method == "GET":
        return render_template("bestdeals.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        json_data = {
            "region": request.form.get("region"),
            "type": request.form.get("type"),
            "discount": int(request.form.get("discount")),
            "minPrice": int(request.form.get("minPrice")),
            "salesPerDay": int(request.form.get("salesPerDay")),
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/bestdeals",
            headers=headers,
            json=json_data,
        ).json()

        if "data" not in response:
            return f"Error no matching data with given inputs {response}"
        response = response["data"]

        for row in response:
            del row["itemID"]
            del row["connectedRealmId"]

            minPrice = row["minPrice"]
            del row["minPrice"]
            row["minPrice"] = minPrice

            historicalPrice = row["historicPrice"]
            del row["historicPrice"]
            row["historicPrice"] = historicalPrice

            itemName = row["itemName"]
            del row["itemName"]
            row["itemName"] = itemName

            realmName = row["realmName"]
            del row["realmName"]
            row["realmName"] = realmName

            link = row["link"]
            del row["link"]
            row["link"] = link

        fieldnames = list(response[0].keys())

        return render_template(
            "bestdeals.html",
            results=response,
            fieldnames=fieldnames,
            len=len,
        )


if __name__ == "__main__":
    ## http
    app.run(host="0.0.0.0", debug=True)

    # ## https
    # app.run(host='0.0.0.0',port=443,debug=True, ssl_context=("./certs/full_chain.crt","./certs/private.key"))
