import requests
import time
import json
import datetime

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/main.db'
api = Api(app)
db = SQLAlchemy(app)
CORS(app, resources={r'/*': {'origins': '*'}})


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Find(Resource):
    def post(self):
        cameras = [
            { "url": "192.168.31.151", "location": "702A" },
            { "url": "192.168.31.181", "location": "702B" },
            { "url": "192.168.31.153", "location": "703A" },
            { "url": "192.168.31.134", "location": "703B" },
        ]

        payload = {
            "start_time": datetime.datetime.now() - datetime.timedelta(seconds=1800),
            "end_time": datetime.datetime.now() + datetime.timedelta(seconds=1)
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        bunch = list()
        for camera in cameras:
            response = requests.request("POST", "http://" + camera["url"] + "/person/record/query/time", headers=headers, data=payload)
            content = response.text
            data = json.loads(content)
            if data["data"]:
                for people in data["data"]:
                    if people["username"] == "曹jing":
                        people["username"] = "曹競"
                    if people["username"] == "周min":
                        people["username"] = "周旻"
                    people["location"] = camera["location"]
                    bunch.append( { "datetime": people["datetime"], "location": people["location"], "username": people["username"], "image_url": "http://localhost:5000/static/33cn/"+people["username"]+".jpg" } )
            else:
                return "nobody"
        def takeDatetime(e):
            return e['datetime']
        bunch.sort(key=takeDatetime)



        result = dict()
        result["data"] = bunch
        return result

api.add_resource(Find, '/find')


if __name__ == '__main__':
    app.run(debug=True)
