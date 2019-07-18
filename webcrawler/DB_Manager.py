'''
DB_Manager.py

Manages database connection

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

import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')

print(client)

db = client["testDB"]

db = db.test


dict = {"Hello": "Wolrd"}

result = db.insert_one(dict)
print(result)