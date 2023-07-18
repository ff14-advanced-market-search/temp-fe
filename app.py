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


@app.route("/ffxiv", methods=["GET", "POST"])
def ffxiv():
    return render_template("ffxiv_index.html", len=len)


@app.route("/wow", methods=["GET", "POST"])
def wow():
    return render_template("wow_index.html", len=len)


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


@app.route("/ffxiv_itemnames", methods=["GET", "POST"])
def ffxivitemnames():
    if request.method == "GET":
        return render_template("ffxiv_itemnames.html")
    elif request.method == "POST":
        raw_items_names = requests.get(
            "https://raw.githubusercontent.com/ffxiv-teamcraft/ffxiv-teamcraft/staging/libs/data/src/lib/json/items.json"
        ).json()
        item_ids = requests.get("https://universalis.app/api/marketable").json()

        resp_list = []
        for id in item_ids:
            resp_list.append({"id": id, "name": raw_items_names[str(id)]["en"]})

        return render_template(
            "ffxiv_itemnames.html",
            results=resp_list,
            fieldnames=["id", "name"],
            len=len,
        )


# {
#   "home_server": "Famfrit",
#   "user_auctions": [
#     { "itemID": 4745, "price": 100, "desired_state": "below", "hq": true }
#   ]
# }
@app.route("/pricecheck", methods=["GET", "POST"])
def ffxiv_pricecheck():
    if request.method == "GET":
        return render_template("ffxiv_pricecheck.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        json_data = json.loads(request.form.get("jsonData"))

        response = requests.post(
            "http://api.saddlebagexchange.com/api/pricecheck",
            headers=headers,
            json=json_data,
        ).json()

        if "matching" not in response:
            return "Error no matching data"
        if len(response["matching"]) == 0:
            return "Error no matching data"

        fixed_response = []
        for row in response["matching"]:
            fixed_response.append(
                {
                    "minPrice": row["minPrice"],
                    "itemName": row["itemName"],
                    "server": row["server"],
                    "dc": row["dc"],
                    "desired_state": row["desired_state"],
                    "hq": row["hq"],
                    "quantity": row["minListingQuantity"],
                    "item-data": f"https://saddlebagexchange.com/queries/item-data/{row['itemID']}",
                    "uniLink": f"https://universalis.app/market/{row['itemID']}",
                }
            )
        fieldnames = list(fixed_response[0].keys())

        return render_template(
            "ffxiv_pricecheck.html",
            results=fixed_response,
            fieldnames=fieldnames,
            len=len,
        )


@app.route("/ffxivcraftsim", methods=["GET", "POST"])
def ffxivcraftsim():
    if request.method == "GET":
        return render_template("ffxiv_craftsim.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        if request.form.get("hide_expert_recipes") == "True":
            hide_expert_recipes = True
        else:
            hide_expert_recipes = False

        json_data = {
            "home_server": request.form.get("home_server"),
            "cost_metric": request.form.get("cost_metric"),
            "revenue_metric": request.form.get("revenue_metric"),
            "sales_per_week": int(request.form.get("sales_per_week")),
            "median_sale_price": int(request.form.get("median_sale_price")),
            "max_material_cost": int(request.form.get("max_material_cost")),
            "job": int(request.form.get("job")),
            "filters": [int(request.form.get("filters"))],
            "stars": int(request.form.get("stars")),
            "lvl_lower_limit": int(request.form.get("lvl_lower_limit")),
            "lvl_upper_limit": int(request.form.get("lvl_upper_limit")),
            "yields": int(request.form.get("yields")),
            "hide_expert_recipes": hide_expert_recipes,
        }

        craftsim_post_json = requests.post(
            "http://api.saddlebagexchange.com/api/recipelookup",
            headers=headers,
            json=json_data,
        ).json()

        example = {
            "cost_metric": "material_median_cost",
            "crafting_list_hq": {},
            "crafting_list_nq": {},
            "home_server": "Famfrit",
            "revenue_metric": "revenue_home_min_listing",
            "max_material_cost": 100000,
        }
        # catch errors from the main craftsim
        if example.keys() != craftsim_post_json.keys():
            return craftsim_post_json

        return craftsim_results_table(craftsim_post_json, "ffxiv_craftsim.html")


@app.route("/ffxivcraftsimcustom", methods=["GET", "POST"])
def ffxivcraftsimcustom():
    if request.method == "GET":
        return render_template("ffxiv_craftsimcustom.html")
    elif request.method == "POST":
        return craftsim_results_table(
            json.loads(request.form.get("jsonData")), "ffxiv_craftsimcustom.html"
        )


def craftsim_results_table(craftsim_post_json, html_file_name):
    headers = {"Accept": "application/json"}
    craftsim_results = requests.post(
        "http://api.saddlebagexchange.com/api/craftsim",
        headers=headers,
        json=craftsim_post_json,
    ).json()

    if "data" not in craftsim_results:
        return craftsim_results

    craftsim_results = craftsim_results["data"]

    for item_data in craftsim_results:
        del item_data["itemID"]
        hq = item_data["hq"]
        del item_data["hq"]
        yields = item_data["yieldsPerCraft"]
        del item_data["yieldsPerCraft"]

        se_link = item_data["itemData"]
        del item_data["itemData"]
        universalisLink = item_data["universalisLink"]
        del item_data["universalisLink"]

        costEst = item_data["costEst"]
        del item_data["costEst"]
        revenueEst = item_data["revenueEst"]
        del item_data["revenueEst"]

        item_data["hq"] = hq
        item_data["yields"] = yields
        item_data["item-data"] = se_link
        item_data["universalisLink"] = universalisLink

        item_data["material_min_listing_cost"] = costEst["material_min_listing_cost"]
        item_data["material_median_cost"] = costEst["material_median_cost"]
        item_data["material_avg_cost"] = costEst["material_avg_cost"]

        item_data["revenue_home_min_listing"] = revenueEst["revenue_home_min_listing"]
        item_data["revenue_region_min_listing"] = revenueEst[
            "revenue_region_min_listing"
        ]
        item_data["revenue_median"] = revenueEst["revenue_median"]
        item_data["revenue_avg"] = revenueEst["revenue_avg"]

    fieldnames = list(craftsim_results[0].keys())

    return render_template(
        html_file_name,
        results=craftsim_results,
        fieldnames=fieldnames,
        len=len,
    )


@app.route("/ffxivcraftsimconfig", methods=["GET", "POST"])
def ffxivcraftsimconfig():
    if request.method == "GET":
        return render_template("ffxiv_craftsimconfig.html")
    elif request.method == "POST":
        headers = {"Accept": "application/json"}

        if request.form.get("hide_expert_recipes") == "True":
            hide_expert_recipes = True
        else:
            hide_expert_recipes = False

        json_data = {
            "home_server": request.form.get("home_server"),
            "cost_metric": request.form.get("cost_metric"),
            "revenue_metric": request.form.get("revenue_metric"),
            "sales_per_week": int(request.form.get("sales_per_week")),
            "median_sale_price": int(request.form.get("median_sale_price")),
            "max_material_cost": int(request.form.get("max_material_cost")),
            "job": int(request.form.get("job")),
            "filters": [int(request.form.get("filters"))],
            "stars": int(request.form.get("stars")),
            "lvl_lower_limit": int(request.form.get("lvl_lower_limit")),
            "lvl_upper_limit": int(request.form.get("lvl_upper_limit")),
            "yields": int(request.form.get("yields")),
            "hide_expert_recipes": hide_expert_recipes,
        }

        craftsim_post_json = requests.post(
            "http://api.saddlebagexchange.com/api/recipelookup",
            headers=headers,
            json=json_data,
        ).json()

        return craftsim_post_json


#### WOW ####
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
            "itemID": int(request.form.get("petID")),
            "maxPurchasePrice": int(request.form.get("maxPurchasePrice")),
            "connectedRealmIDs": {},
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/shoppinglist",
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
            "itemID": int(request.form.get("itemID")),
            "populationWP": int(request.form.get("populationWP")),
            "populationBlizz": int(request.form.get("populationBlizz")),
            "rankingWP": int(request.form.get("rankingWP")),
            "minPrice": int(request.form.get("minPrice")),
            "maxQuantity": int(request.form.get("maxQuantity")),
            "sortBy": "minPrice",
            "connectedRealmIDs": {},
        }

        response = requests.post(
            "http://api.saddlebagexchange.com/api/wow/export",
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
            "salesPerDay": float(request.form.get("salesPerDay")),
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
            "salesPerDay": float(request.form.get("salesPerDay")),
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
