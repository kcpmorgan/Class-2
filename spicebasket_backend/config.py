import pymongo
import certifi

con_str = "mongodb+srv://petrakc:Mitchell01#$@cluster0.0cxin.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("SpiceStore")
