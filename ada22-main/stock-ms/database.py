from pymongo import MongoClient
import os

client = MongoClient(os.environ["MONGO_HOST"])
db = client.stocks