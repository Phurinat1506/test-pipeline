import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from flask import jsonify


def decrypt(msg):

    key = "xxxadaxxxxadaxxx"
    iv = "xxxxqixxxhxqxxxx"
    iv = iv.encode('utf-8')
    raw = pad(msg.encode(),16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

    enc2 = base64.b64decode(raw)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    body = unpad(cipher.decrypt(enc2),16)

    return json.loads(body)

def encrypt(message,status_code,key,iv):

    key = key
    iv = iv

    iv = iv.encode('utf-8')
    txt = json.dumps(message)
    txt_body = str(txt)
    
    raw = pad(txt_body.encode(),16)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)

    encrypt_res = base64.b64encode(cipher.encrypt(raw))
    test = encrypt_res.decode('utf-8')

    resp = jsonify(test)
    resp.status_code = status_code
    return resp
