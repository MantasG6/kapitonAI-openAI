import json
from models.Location import Location
from models.Destinations import Destinations

def dict2loc(dict):
    return json.loads(json.dumps(dict), object_hook=Location)

def string2dict(text):
    return json.loads(text)

def dict2dest(dict):
    return json.loads(json.dumps(dict), object_hook=Destinations)