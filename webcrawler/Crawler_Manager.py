'''

Crawler_Manager.py
by Daniel McDonough
8/7/19

This handles the crawlers on a thread basis and adds the results to a DB

'''


from threading import Thread
from ebayCrawler import ebayCrawler
from queue import Queue
from Instrument_DB import InstrumentDatabase

class CrawlerManager:

    def __init__(self):
        self.Result_queue = Queue()
        self.InstrumentDB = InstrumentDatabase()

    def RunEbay(self,jsondata):
        spider = ebayCrawler()
        results = spider.run(jsondata)
        self.Result_queue.put(results)

    # TODO add Craigslist and Reverb crawlers

    def sendtoDB(self,data):
        self.InstrumentDB.createEntry(data)
        return

    def RunCrawlers(self,jsondata):
        ebay = Thread(target=self.RunEbay, args=(jsondata, ), name='Ebay_Crawler')
        ebay.start()
        # ebay.join()
        result = self.Result_queue.get()

        print(result)

        # addata = Thread(target=self.sendtoDB,args=(result, ), name='Instrument_DB')
        # addata.start()


        return result