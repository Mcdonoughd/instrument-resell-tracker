'''

Server_Manager.py
by Daniel McDonough 8/7/19

Manages packages sent from a website

'''


from flask import Flask
from flask import request
import json
from flask import jsonify
import time
from Job_Manager import JobManager
from Job_Cleaner import JobCleaner
from Crawler_Manager import CrawlerManager
from threading import Thread

# Before server gate opens, make sure DBs and daemons are up and
cleaner = JobCleaner()  # Load Cleaner
Crawler = CrawlerManager() # load Crawler Manager
JobManager = JobManager() # Load Job manager

app = Flask(__name__) # Load Flask Server


@app.route('/Job_Request/', methods = ['POST'])
def Job_Request():
    print("Incoming Job...")
    jsondata = request.get_json()
    data = json.loads(jsondata)

    cleandata = cleaner.cleanJob(data)  # Clean Job

    # In new thread, send to job manager
    # job_thread = Thread(target=JobManager.createJob(cleandata), name='Thread-JobManager', daemon=False)
    # job_thread.start()

    # send the cleaned data to the crawler manager
    result = Crawler.RunCrawlers(cleandata)
    print(result)
    return result


@app.route('/Job_Update/')
def Job_Update():
    print("Updating Job...")
    jsondata = request.get_json()
    data = json.loads(jsondata)

    newvalues = {"$set": {"Last_Search": int(round(time.time() * 1000))}}
    JobManager.updateJob(data,newvalues)




@app.route('/')
def hello():
    return

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=90)