'''
DB_Manager.py
by Daniel McDonough
8/9/19

Manages database connection and CRUD for Crawler fetches

Note: Ideally the Job_Manager DB and Instrument DB would be separate databases

To run
sudo docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:4.0.4

To remove
sudo docker stop mongodb
sudo docker rm mongodb

To enter docker bash:
sudo docker exec -it mongodb bash

To enter mongo bash
 mongo

'''

import time
import pymongo
from threading import Thread



class InstrumentDatabase:

    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client["Instruments"]
        self.mycol = self.db["Active"]

        a = Thread(target=self.search, name='InstrumentDatabaseDaemon', daemon=True)
        a.start()

    # Adds Job to the job DB
    def createEntry(self,jsondata):
        array = jsondata["items"]
        for i in array:
            self.mycol.insert(i)
            print("Added Crawler Entry to server")

    # Reads Job and translates it to readable format for web crawlers
    def readEntry(self,jsondata):
        print("Reading Jobs")
        self.mycol.find(jsondata)

    # Updates Job in the cache
    def updateEntry(self,jsondata):
        print("Job Updated!")
        self.mycol.updateOne(jsondata)

    # Deletes job from Job cache
    def deleteEntry(self,jsondata):
        self.mycol.deleteOne(jsondata)
        print("Job Deleted")

    # Search through Job database for jobs that haven't been searched for in two days (arbitrary day count)
    def search(self):
        print("Starting Database Daemon")
        while True:
            curr_time = int(round(time.time() * 1000))

            resp = self.mycol.deleteOne({"endTime": {'$lt': curr_time}})

