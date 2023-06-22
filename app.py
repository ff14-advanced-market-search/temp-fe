from flask import Flask
from flask import render_template
from flask import request
import json
import requests

app = Flask(__name__)

def str_to_bool(bool_str):
    if bool_str == "True":
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
def root(): 
    return render_template('index.html', len=len)


@app.route('/scan', methods=['GET', 'POST'])
def scan(): 
    if request.method == 'GET':
        return render_template('oldscan.html')
    elif request.method == 'POST':
        results = []
        
        scan_hours = request.form.get("scan_hours")
        sale_amt = request.form.get("sale_amt")
        roi = request.form.get("roi")
        home_server = request.form.get("home_server")
        stack_size = request.form.get("stack_size")
        hq_only = request.form.get("hq_only")
        profit_amt = request.form.get("profit_amt")
        min_desired_avg_ppu = request.form.get("min_desired_avg_ppu")
        # language = request.form.get("language")
        game_wide = request.form.get("game_wide")
        include_vendor = request.form.get("include_vendor")
        out_stock = request.form.get("out_stock")
        filters = request.form.get("filters")

        # response = json.load(open("test.json"))
        headers = {'Accept': 'application/json',}
        json_data = {
            "preferred_roi": int(roi),
            "min_profit_amount": int(profit_amt),
            "min_desired_avg_ppu": int(min_desired_avg_ppu),
            "min_stack_size": int(stack_size),
            "hours_ago": int(scan_hours),
            "min_sales": int(sale_amt),
            "hq": str_to_bool(hq_only),
            "home_server": home_server,
            "filters": int(filters),
            "region_wide": str_to_bool(game_wide),
            "include_vendor": str_to_bool(include_vendor),
            "show_out_stock": str_to_bool(out_stock)
        }

        # {
        #     "preferred_roi": 50, 
        #     "min_profit_amount": 10000,
        #     "min_desired_avg_ppu": 10000,
        #     "min_stack_size": 1,
        #     "hours_ago": 24,
        #     "min_sales": 5,
        #     "hq": false,
        #     "home_server": "Famfrit",
        #     "filters": "all",
        #     "region_wide": false,
        #     "include_vendor": false,
        #     "show_out_stock": true
        # }
        print (json_data)
        response = requests.post('http://api.saddlebagexchange.com/api/scan/', headers=headers, json=json_data).json()

        print(response)

        ## grab the fields and values automatically and dont format list
        # fieldnames = list(list(response.values())[0].keys())
        # item_list = list(response.values())

        # change default order of table columns
        fieldnames = [
            "real_name",
            "ppu",
            "home_server_price",
            "profit_amount",
            "sale_rates",
            "avg_ppu",
            "server",
            "ROI",
            "profit_raw_percent",
            "stack_size",
            "update_time",
            "home_update_time",
            "url",
            "npc_vendor_info",
        ]
        item_list = [
            {
                "real_name": item["real_name"],
                "ppu": item["ppu"],
                "home_server_price": item["home_server_price"],
                "profit_amount": item["profit_amount"],
                "sale_rates": item["sale_rates"],
                "avg_ppu": item["avg_ppu"],
                "server": item["server"],
                "ROI": item["ROI"],
                "profit_raw_percent": item["profit_raw_percent"],
                "stack_size": item["stack_size"],
                "update_time": item["update_time"],
                "home_update_time": item["home_update_time"],
                "url": item["url"],
                "npc_vendor_info": item["npc_vendor_info"],
            } for item in list(response.values())
        ]

        return render_template('home.html', results=item_list, fieldnames=fieldnames, len=len)


if __name__ == '__main__':
    ## http
    app.run(host='0.0.0.0',debug=True)

    # ## https
    # app.run(host='0.0.0.0',port=443,debug=True, ssl_context=("./certs/full_chain.crt","./certs/private.key"))



