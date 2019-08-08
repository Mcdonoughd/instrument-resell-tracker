'''

Client.py
by Daniel McDonough 8/7/19

This simulates the website as it sends JSON data to the Server_Manager

'''


import json
import requests


def Send_Data():
    # This is the expected format from the website
    payload = {
        "ID": 1,
        "Serial": "A-13645",  # This is not guaranteed by ebay or craigslist
        "Instrument": "Sunburst Archtop Electric Guitar",  # This is not guaranteed by the user
        "Description": "N/A",
        "Make": "Gibson",
        "Model": "ES-175",
        "Year": "1953",  # This is not guaranteed by the user
        "Status": "Stolen",
        "Location": "Worcester, MA",  # This is not guaranteed by the user
        "Date": "7/20/19"  # This is not guaranteed by the user
    }

    s = json.dumps(payload)

    # Send signal to localhost server
    res = requests.post("http://127.0.0.1:90/Job_Request/", json=s).json()

    # Print response
    printRes(res)


def printRes(jsondata):
    # Prints the given response data
    array = jsondata["items"]
    for i in array:
        print(i)

if __name__ == '__main__':
    Send_Data()