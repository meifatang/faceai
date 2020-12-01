import requests
import time
import json
import datetime

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.static_folder = 'static'

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/find', methods=['GET', "POST"])
def find():
    if request.method == "GET":
        return "to get info, please use post method."
    else:
        urls = [
            "192.168.31.151",
            # "192.168.31.181",
            # "192.168.31.153",
            # "192.168.31.134",
        ]

        payload = {
            "start_time": datetime.datetime.now() - datetime.timedelta(seconds=1800),
            "end_time": datetime.datetime.now() + datetime.timedelta(seconds=1)
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        for url in urls:
            response = requests.request("POST", "http://" + url + "/person/record/query/time", headers=headers, data=payload)
            content = response.text
            data = json.loads(content)
            if data["data"]:
                bunch = list()
                for people in data["data"]:
                    if people["username"] == "曹jing":
                        people["username"] = "曹競"
                    if people["username"] == "周min":
                        people["username"] = "周旻"
                    bunch.append( { "datetime": people["datetime"], "username": people["username"], "image_url": "http://localhost:5000/static/33cn/"+people["username"]+".jpg" } )
                result = dict()
                result["data"] = bunch
                return result
            else:
                return "nobody"


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')