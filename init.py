from datetime import datetime, timedelta
import time
from flask import Flask ,jsonify,request,Blueprint
import yaml
from model.authorization import token_required
from pymongo import MongoClient
from model import init
import json
import sys, getopt

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

CONFIG_FILE = './config.yaml'

try:
    file_stream = open(CONFIG_FILE, "r", encoding='utf-8')
    # Load configuration into config
    Config = yaml.load(file_stream, Loader=Loader)
    file_stream.close()
except Exception as e:
    print("Read configuration file error:", e)
    exit(1)



ignore_coll = [
               "out_case",
               "log_ticket",
               "log_template_mail",
               "waiting_ticket",
               "log_open_ticket",
               "log_error_open_ticket",
               "test"
               ]

def get_argv():
    mode = ""

    # ตรวจสอบว่ามี arguments หรือไม่
    if len(sys.argv) < 2:
        print(0)
        print("Please select Mode")
        print()
        print("python3 cmd.py -I                    Init database")
        print("python3 cmd.py -B                    backup database")
        print()
        print()

    else:
        if sys.argv[1] == "-B":
            return 1
        elif sys.argv[1] == "-I":
            return 2
        else:
            print(1)
            print("Please select Mode")
            print()
            print("python3 cmd.py -I                    Init database")
            print("python3 cmd.py -B                    backup database")
            print()
            print()
            sys.exit(0)

def dropdatabase():
    db = init.database()
    list_coll = db.list_collection_names()

    # with open('mockdatabase.json', 'r') as file:
    #     data = json.load(file)
    for x in list_coll:
        if x not in ignore_coll:
            data = list(db[x].find({},{"_id":0}))
            with open(f'mockup/{x}.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

def init_db():
    import os

    folder_path = 'mockup/'

    file_names = os.listdir(folder_path)
    file_names.remove("README")

    db = init.database()
    for x in file_names:
        print(x.split(".")[0])
        coll = db[x.split(".")[0]]
        coll.drop()

        with open(folder_path+x, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, list):
            coll.insert_many(data)
        else:
            coll.insert_one(data)

    for y in ignore_coll:
        print(y)
        coll = db[y]
        coll.insert_one({"id":"auto_123_mockup_database_1234567890"})
        coll.delete_many({"id":"auto_123_mockup_database_1234567890"})

if __name__ == '__main__':
    mode = get_argv()

    if mode == 1:
        x = input("(Y/N) : ")
        if x in ["y","Y"]:
            dropdatabase()
        else:
            print("Exit.")
            exit()
    elif mode == 2:
        x = input("(Y/N) : ")
        if x in ["y","Y"]:
            init_db()
        else:
            print("Exit.")
            exit()
    else:
        exit()