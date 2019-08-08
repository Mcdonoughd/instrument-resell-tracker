'''

Job_Cleaner.py
by Daniel McDonough
8/9/19

This manages the act of cleaning jobs into a form for data storage and Crawler parsing

'''

import time


class JobCleaner:
    def __init__(self):
        print("Job Cleaner Initialized...")

    def addTime(self,d):
        currtime = int(round(time.time() * 1000))
        # date_added is to potentially check for a limit to how long a job should be searched for
        d["Date_Added"] = currtime

        # This is time the last search conducted
        d["Last_Search"] = currtime
        return d

    def cleanJob(self,jsondata):
        print("Cleaning Job")
        cleaned_data = {
            "Make": jsondata["Make"],
            "Model": jsondata["Model"],
            "Instrument": jsondata["Instrument"],
            }

        added_Time = self.addTime(cleaned_data)

        # any additional data cleaning here

        return added_Time

