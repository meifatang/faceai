import requests
import datetime
import json
import time
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///sqlite.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class People(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    location = Column(String(10), nullable=False)
    username = Column(String(20), nullable=False)
    image_url = Column(String(50), nullable=False)


cameras = [
    { "url": "192.168.31.151", "location": "702A" },
    { "url": "192.168.31.181", "location": "702B" },
    { "url": "192.168.31.153", "location": "703A" },
    { "url": "192.168.31.134", "location": "703B" },
]
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

last_time = datetime.datetime.now()
while True:
    now_time = datetime.datetime.now()
    print(last_time.strftime('%Y-%m-%d %H:%M:%S'), " -> " ,now_time.strftime('%Y-%m-%d %H:%M:%S'))
    payload = {
        "start_time": (last_time - datetime.timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S'),
        "end_time": now_time.strftime('%Y-%m-%d %H:%M:%S')
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
                bunch.append( { "datetime": people["datetime"], "location": people["location"], "username": people["username"], "image_url": "http://192.168.31.7:5000/static/33cn/"+people["username"]+".jpg" } )
        else:
            pass

    def takeDatetime(e):
        return e['datetime']

    bunch.sort(key=takeDatetime)

    session = Session()
    for b in bunch:
        print(b)
        tmp = People(datetime=datetime.datetime.strptime(b['datetime'], '%Y-%m-%d %H:%M:%S'), location=b['location'], username=b['username'], image_url=b['image_url'])
        session.add(tmp)
        session.commit()

    time.sleep(1)
    last_time = now_time
