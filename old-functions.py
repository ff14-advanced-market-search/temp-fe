#### FFXIV RESELLING SEARCH ####
# just used for initial test of temp flask pod not maintained

# @app.route("/scan", methods=["GET", "POST"])
# def scan():
#     if request.method == "GET":
#         return render_template("oldscan.html")
#     elif request.method == "POST":
#         scan_hours = request.form.get("scan_hours")
#         sale_amt = request.form.get("sale_amt")
#         roi = request.form.get("roi")
#         home_server = request.form.get("home_server")
#         stack_size = request.form.get("stack_size")
#         hq_only = request.form.get("hq_only")
#         profit_amt = request.form.get("profit_amt")
#         min_desired_avg_ppu = request.form.get("min_desired_avg_ppu")
#         game_wide = request.form.get("game_wide")
#         include_vendor = request.form.get("include_vendor")
#         out_stock = request.form.get("out_stock")
#         filters = [int(request.form.get("filters"))]

#         headers = {"Accept": "application/json"}
#         json_data = {
#             "preferred_roi": int(roi),
#             "min_profit_amount": int(profit_amt),
#             "min_desired_avg_ppu": int(min_desired_avg_ppu),
#             "min_stack_size": int(stack_size),
#             "hours_ago": int(scan_hours),
#             "min_sales": int(sale_amt),
#             "hq": str_to_bool(hq_only),
#             "home_server": home_server,
#             "filters": filters,
#             "region_wide": str_to_bool(game_wide),
#             "include_vendor": str_to_bool(include_vendor),
#             "show_out_stock": str_to_bool(out_stock),
#             "universalis_list_uid": "",
#         }

#         response = requests.post(
#             "http://api.saddlebagexchange.com/api/scan/",
#             headers=headers,
#             json=json_data,
#         ).json()

#         if "data" not in response:
#             return f"Error no matching data with given inputs {response}"
#         response = response["data"]

#         fieldnames = list(response[0].keys())

#         return render_template(
#             "oldscan.html", results=response, fieldnames=fieldnames, len=len
#         )


#### WOW IMPORT SEARCH ####
# obsolete with cross realm trading

# @app.route("/petimport", methods=["GET", "POST"])
# def petimport():
#     if request.method == "GET":
#         return render_template("petimport.html")
#     elif request.method == "POST":
#         headers = {"Accept": "application/json"}
#         petsOnly = request.form.get("petsOnly")
#         if petsOnly == "False":
#             petsOnly = False
#         else:
#             petsOnly = True
#         json_data = {
#             "region": request.form.get("region"),
#             "homeRealmID": int(request.form.get("homeRealmID")),
#             "ROI": int(request.form.get("ROI")),
#             "avgPrice": int(request.form.get("avgPrice")),
#             "maxPurchasePrice": int(request.form.get("maxPurchasePrice")),
#             "profitAmount": int(request.form.get("profitAmount")),
#             "salesPerDay": float(request.form.get("salesPerDay")),
#             "includeCategories": [],
#             "excludeCategories": [],
#             "sortBy": "lowestPrice",
#             "petsOnly": petsOnly,
#             "connectedRealmIDs": {},
#         }

#         response = requests.post(
#             "http://api.saddlebagexchange.com/api/wow/petimport",
#             headers=headers,
#             json=json_data,
#         ).json()

#         if "data" not in response:
#             return f"Error no matching data with given inputs {response}"
#         response = response["data"]
#         if len(response) == 0:
#             return f"No item found with given inputs, try lowering price or sale amount {json_data}"

#         for row in response:
#             del row["itemID"]
#             del row["lowestPriceRealmID"]
#             realm = row["lowestPriceRealmName"]
#             del row["lowestPriceRealmName"]
#             row["lowestPriceRealmName"] = realm

#             link = row["link"]
#             del row["link"]
#             row["link"] = link

#             undermineLink = row["undermineLink"]
#             del row["undermineLink"]
#             row["undermineLink"] = undermineLink

#             warcraftPetsLink = row["warcraftPetsLink"]
#             del row["warcraftPetsLink"]
#             row["warcraftPetsLink"] = warcraftPetsLink

#         fieldnames = list(response[0].keys())

#         return render_template(
#             "petimport.html",
#             results=response,
#             fieldnames=fieldnames,
#             len=len,
#         )
