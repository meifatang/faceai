import requests
import datetime
import json
import time
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

Base = declarative_base()
engine = create_engine('sqlite:///sqlite.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class People(Base):
    __tablename__ = "faceai"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    location = Column(String(10), nullable=False)
    username = Column(String(20), nullable=False)
    status = Column(String(20))


cameras = [
    { "url": "192.168.31.151", "location": "702A" },
    { "url": "192.168.31.181", "location": "702B" },
    { "url": "192.168.31.153", "location": "703A" },
    { "url": "192.168.31.134", "location": "703B" }
]
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

last_time = datetime.datetime.now()
while True:
    time1 = datetime.datetime.now()
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
                bunch.append({ 
                    "date": datetime.datetime.strptime(people["datetime"], '%Y-%m-%d %H:%M:%S').date(), 
                    'time': datetime.datetime.strptime(people["datetime"], '%Y-%m-%d %H:%M:%S').time(), 
                    "location": people["location"], 
                    "username": people["username"], 
                })
        else:
            pass

    bunch = sorted(bunch, key=lambda x: x['date'])
    bunch = sorted(bunch, key=lambda x: x['time'])

    for b in bunch:
        status = ''
        if not session.query(People).filter_by(date=b['date'], username=b['username']).first():
            status = "First"
        
        tmp = People(date=b['date'], time=b['time'], location=b['location'], username=b['username'], status=status)
        session.add(tmp)
        session.commit()

    last_time = now_time

    time2 = datetime.datetime.now()
    if time2 - time1 < datetime.timedelta(seconds=1):
        time.sleep(time2 - time1)
    else:
        pass
