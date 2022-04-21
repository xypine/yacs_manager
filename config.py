import os
import toml

config_path = "../../yacsms_config.toml"

allowed_token = os.getenv('YACSMS_TOKEN', 'UNSECUREDEFAULTTOKEN2179')

def parseData():
    try:
        return toml.load(config_path)
    except:
        return {}

def writeData(data):
    with open(config_path, "w") as f:
        toml.dump(data, f)

def getToken():
    data = parseData()
    if "password" in data:
        return data["password"]
    return None

def setToken(password):
    data = parseData()
    data["password"] = password
    writeData(data)

def get_allowed_token():
    t = getToken()
    if t == None:
        t = allowed_token
    return t