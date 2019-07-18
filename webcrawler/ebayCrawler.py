import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection



category = {
            "Musical Instruments & Gear":619,
            "Brass": 16212,
            "DJ Equipment": 48458,
            "Equipment": 180008,
            "Guitars & Basses": 3858,
            "Instruction Books, CDs & Video": 182150,
            "Karaoke Entertainment": 175696,
            "Other Musical Instruments": 308,
            "Percussion": 180012,
            "Pianos, Keyboards & Organs": 180010,
            "Pro Audio Equipment":  180014,
            "Sheet Music & Song Books": 180015,
            "Stage Lighting & Effects" : 12922,
            "String":180016,
            "Vintage Musical Instruments ": 181162,
            "Wholesale Lots": 52555,
            "Wind & Woodwind": 10181
            }

def Main():
    print("Running app...")
    request = {
        'categoryId': '619',
        'paginationInput': {
            'entriesPerPage': 500,
            'pageNumber': 1
        },
        'sortOrder': 'PricePlusShippingLowest'
    }
    try:
        api = Connection(config_file='ebay.yaml', siteid="EBAY-US")
        response = api.execute('findItemsByCategory', request)

        assert (response.reply.ack == 'Success')

        item = response.reply.searchResult.item

        print(item)


    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == "__main__":
    Main()