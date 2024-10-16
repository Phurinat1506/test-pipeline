from flask import Flask ,jsonify,request,Blueprint
import yaml
from model.authorization import token_required
from model import init

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

home_bp = Blueprint('home_bp', __name__,)

@home_bp.route('/' , methods=['GET'])
@token_required
def home():
    try:
        coll_template_mail = init.database()['template_mail']
        message = {
            'status': 200,
            'message': 'This is api auto ticket inet ms',
        }
        resp = jsonify(message)
        resp.status_code = 200

        return resp

    except Exception as e:
        message = {
        'status': 500,
        'message': 'Server error',
        }
        resp = jsonify(message)
        resp.status_code = 500

        return resp