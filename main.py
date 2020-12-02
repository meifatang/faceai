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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
api = Api(app)
db = SQLAlchemy(app)
CORS(app, resources={r'/*': {'origins': '*'}})


class People(db.Model):
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(50), nullable=False)

    def get(self):
        return {
            'datetime': self.datetime,
            'location': self.location,
            'username': self.username,
            'image_url': self.image_url
        }

class Find(Resource):
    def post(self):
        tmp = list()
        for i in People.query.all():
            tmp.append(i.get())
        print(tmp[-3:])
        return "test"

api.add_resource(Find, '/find')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
