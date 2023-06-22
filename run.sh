#!/bin/bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=8080

# http
sleep 1 && open -a Google\ Chrome "http://127.0.0.1:8080" &
flask run 

# # https
# sleep 1 && open -a Google\ Chrome "https://127.0.0.1:8080" &
# flask run --cert="certs/full_chain.crt" --key="certs/private.key"