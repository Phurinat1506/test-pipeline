from flask import Flask ,jsonify,request
import datetime
import yaml
from functools import wraps

### Get Config YAML File
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
# File configuration path
CONFIG_FILE = './config.yaml'
try:
    file_stream = open(CONFIG_FILE, "r", encoding='utf-8')
    # Load configuration into config
    Config = yaml.load(file_stream, Loader=Loader)
    file_stream.close()
except Exception as e:
    print("Read configuration file error:", e)
    exit(1)
###

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({
                'message': 'Token is missing',
                'status':403
                }), 403

        try:
            bearer = token.split()[0]
            token = token.split()[1]
            if bearer == "Bearer" and token == "test123":
                pass
            else:
                return jsonify({
                    'message': 'Unauthorized',
                    'status': 401
                }), 401
        except Exception as err:
            # print(err)
            return jsonify({
                    'message': 'Token is exp',
                    'status':500
                }), 500

        return f(*args, **kwargs)

    return decorated
