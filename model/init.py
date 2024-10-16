import yaml
from pymongo import MongoClient

### Get Config YAML File
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
# File configuration path
CONFIG_FILE = './config.yaml'
# Load Configuration File config
try:
    file_stream = open(CONFIG_FILE, "r", encoding='utf-8')
    # Load configuration into config
    Config = yaml.load(file_stream, Loader=Loader)
    file_stream.close()
except Exception as e:
    print("Read configuration file error:", e)
    exit(1)

def database():
    if Config['server']['type'] == "prd":
        #url = "mongodb://"+Config['mongodb']['username']+":"+Config['mongodb']['password']+"@"+Config['mongodb']['server']+"/?authMechanism=DEFAULT"
        url = "mongodb://10.70.56.21:27017,10.70.56.22:27017,10.70.56.23:27017/database?authSource=admin"
        client = MongoClient(url)
        #db = client[Config['mongodb']['dbname']]
        return client
    else:
        url = "mongodb://localhost:27017/"
        client = MongoClient(url)
        #db = client[Config['mongodb']['dbname']]

        return client
    

