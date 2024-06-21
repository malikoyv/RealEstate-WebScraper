from pymongo import MongoClient
from pymongo.server_api import ServerApi

# MongoDB's connection
# root - is the username and 1234567890 - is the password
uri = "mongodb+srv://root:1234567890@atlascluster.hpyo9qg.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['real_estate']  # Replace with yours database name
collection = db['data']  # Replace with yours collection name
