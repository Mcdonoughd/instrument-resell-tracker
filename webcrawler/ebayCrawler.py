'''

ebayCrawler.py
by Daniel McDonough 8/7/19

This handles the the crawling and parsing of ebay listings

'''


from datetime import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json

'''
Example Request:

request = {
    'keywords': 'laptop',
    'categoryId' : ['177', '111422'],
    'itemFilter': [
        {'name': 'Condition', 'value': 'Used'},
        {'name': 'MinPrice', 'value': '200', 'paramName': 'Currency', 'paramValue': 'GBP'},
        {'name': 'MaxPrice', 'value': '400', 'paramName': 'Currency', 'paramValue': 'GBP'}
    ],
    'paginationInput': {
        'entriesPerPage': '25',
        'pageNumber': '1' 	 
    },
    'sortOrder': 'CurrentPriceHighest'
}

'''


class ebayCrawler:
    def __init__(self):
        print("Ebay Crawler Initialized...")

    # Parses the request query from website to ebay's format
    def ObtainRequest(self,jsondata):
        request = {
            'categoryId': '619',
            'paginationInput': {
                'entriesPerPage': '5',
                'pageNumber': '1'
            }
        }

        request["keywords"] = [jsondata["Make"], jsondata["Model"]]
        '''
        The serial number is not a keyword as most listers don't put the 
        serial number of the instrument as part of the listing. 
        '''
        return request

    def run(self,jsondata):
        print("Running ebay crawler...")
        request = self.ObtainRequest(jsondata)

        try:
            api = Connection(config_file='ebay.yaml', siteid="EBAY-US")
            # ebay.yaml contains the ebay credentials to allow the crawler to work


            response = api.execute('findItemsAdvanced', request)

            assert (response.reply.ack == 'Success')

            data = self.cleanData(response.json(), jsondata["Make"], jsondata["Model"])

            return data

        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    ''' ebay.yaml
    name: ebay_api_config

    # Trading API Sandbox - https://www.x.com/developers/ebay/products/trading-api
    api.sandbox.ebay.com:
        compatability: 719
        appid: ENTER_YOUR_APPID_HERE
        certid: ENTER_YOUR_CERTID_HERE
        devid: ENTER_YOUR_DEVID_HERE
        token: ENTER_YOUR_TOKEN_HERE

    # Trading API - https://www.x.com/developers/ebay/products/trading-api
    api.ebay.com:
        compatability: 719
        appid: ENTER_YOUR_APPID_HERE
        certid: ENTER_YOUR_CERTID_HERE
        devid: ENTER_YOUR_DEVID_HERE
        token: ENTER_YOUR_TOKEN_HERE

    # Finding API - https://www.x.com/developers/ebay/products/finding-api (THIS IS THE ONE YOU NEED)
    svcs.ebay.com:
        appid: ENTER_YOUR_APPID_HERE
        version: 1.0.0

    # Shopping API - https://www.x.com/developers/ebay/products/shopping-api
    open.api.ebay.com:
        appid: ENTER_YOUR_APPID_HERE
        version: 671
    '''

    # Reduces Raw Json from ebay into standard format
    def cleanData(self,response, make, model):
        print("Reducing Data...")
        jsondata = json.loads(response)
        # print(jsondata)
        searchResult = jsondata["searchResult"]["item"]
        numResponses = int(jsondata["searchResult"]["_count"])

        CleanedItems = []

        for item in range(numResponses):
            cleanedData = {}
            cleanedData["title"] = searchResult[item]["title"]  # The title of the listing

            cleanedData["year"],cleanedData["make"],cleanedData["model"] = \
                self.parseTitle(cleanedData["title"], make, model)

            cleanedData["category"] = searchResult[item]["primaryCategory"]["categoryName"]
            cleanedData["url"] = searchResult[item]["viewItemURL"]
            cleanedData["location"] = searchResult[item]["location"]
            cleanedData["image"] = searchResult[item]["galleryURL"]

            cleanedData["endTime"] = self.parseTime(searchResult[item]["listingInfo"]["endTime"])
            # the time the listing disappears

            CleanedItems.append(cleanedData)

        FoundItems = {"items": CleanedItems}
        return FoundItems

    # Parses the Title to obtain the year, make and model
    def parseTitle(self, title, make, model):

        maxyear = int(datetime.now().year) + 1  # the guitar could not be make next year

        numbers = [int(s) for s in title.split() if s.isdigit()]  # all numbers in the listing

        year = "Unknown"

        # Check if year is valid
        for i in numbers:
            if i > 1900 and i < maxyear:
                if type(year) == "int":
                    if year > i:
                        year = i
                else:
                    year = i

        # Check for make
        if make in title:
            make = make
        else:
            make = "Not relevant"
        model += " "  # Added space to prevent the case of ES-175D appearing as ES-175

        # Check for model
        if model in title:
            model = model
        else:
            model = "Not relevant"
        return year, make, model

    # convert String time to milliseconds
    def parseTime(self,time):
        ymd = time.split('T')[0]
        ymd = ymd.split('-')
        year = int(ymd[0]) * 31557600000
        month = int(ymd[1]) * 2629800000
        day = int(ymd[2]) * 86400000
        return year + month + day


'''

Ebay category codes:
category = {
    "Musical Instruments & Gear": 619, (Note this one includes all the ones below)
    "Brass": 16212,
    "DJ Equipment": 48458,
    "Equipment": 180008,
    "Guitars & Basses": 3858,
    "Instruction Books, CDs & Video": 182150,
    "Karaoke Entertainment": 175696,
    "Other Musical Instruments": 308,
    "Percussion": 180012,
    "Pianos, Keyboards & Organs": 180010,
    "Pro Audio Equipment": 180014,
    "Sheet Music & Song Books": 180015,
    "Stage Lighting & Effects": 12922,
    "String": 180016,
    "Vintage Musical Instruments ": 181162,
    "Wholesale Lots": 52555,
    "Wind & Woodwind": 10181
}

'''