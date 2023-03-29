from pymongo import MongoClient

# Local db
# db_name : local
# db_client = MongoClient().local


# Atlas db
db_client = MongoClient(
    "mongodb+srv://test:testpass@clusterfastapi.s48ifyg.mongodb.net/?retryWrites=true&w=majority").test