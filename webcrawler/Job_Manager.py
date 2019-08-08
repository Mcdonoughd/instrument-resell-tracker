'''

Job_Manager.py
by Daniel McDonough
8/7/19

This handles the CRUD of the DB and background daemons

'''

from queue import Queue
from threading import Thread
import pymongo
import time
import json
import requests


class JobManager:

    def __init__(self):
        print("Initializing Job Manager")
        self.queue = Queue()  # Job Queue

        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client["Jobs"]
        self.mycol = self.db["Active"]

        a = Thread(target=self.peak, name='QueueDaemon', daemon=True)
        a.start()

        b = Thread(target=self.search, name='DatabaseDaemon', daemon=True)
        b.start()

    # runs Job from the search queue
    def runJob(self, payload):
        print("Running Job")
        s = json.dumps(payload)
        # Send signal to localhost server
        requests.post("http://127.0.0.1:90/Job_Update/", json=s).json()

    # Adds Job to the job DB
    def createJob(self, jsondata):
        print("Added Job to server")
        self.mycol.insert(jsondata)

    # Reads Job and translates it to readable format for web crawlers
    def readJob(self, jsondata):
        print("Reading Jobs")
        self.mycol.find(jsondata)

    # Updates Job in the cache
    def updateJob(self, jsondata, newvals):
        print("Job Updated!")
        self.mycol.updateOne(jsondata,newvals)

    # Deletes job from Job cache
    def deleteJob(self, jsondata):
        self.mycol.deleteOne(jsondata)
        print("Job Deleted")

    # Look at the Job Queue for jobs that need to be completed
    def peak(self):
        print("Starting Job Queue Daemon")
        while True:
            if not self.queue.empty():
                job = self.queue.get()
                self.runJob(job)

    # Search through Job database for jobs that haven't been searched for in two days (arbitrary day count)
    def search(self):
        print("Starting Database Daemon")
        while True:
            curr_time = int(round(time.time() * 1000))

            min_time = curr_time - 172800000

            resp = self.mycol.find({"Last_Search": {'$lt': min_time}})

            for x in resp:
                self.queue.put(x)
                # The program does not immediately run the jobs to prevent blocking


if __name__ == "__main__":
    JobManager()