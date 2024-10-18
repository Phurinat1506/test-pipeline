from flask import Flask ,jsonify,request
import yaml
import urllib3
urllib3.disable_warnings()


#Blueprint
from module.home import home_bp



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

app = Flask(__name__)
app.config['SECRET_KEY'] = Config['server']['secret_key']

# ปิด log ทั้งหมด
# app.config['PROPAGATE_EXCEPTIONS'] = False
# app.config['LOGGER_HANDLER_POLICY'] = 'never'

### Setting CORS Origin
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, authorization' )
  response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
  return response
#########################

#Register Blueprint
app.register_blueprint(home_bp)





## Error-function ##
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == '__main__':
    if Config['server']['type'] == "dev":
        app.run(host="127.0.0.1", port=Config['server']['port'], debug=True)
    else:
        app.run(host=Config['server']['public'], port=Config['server']['port'], debug=True)