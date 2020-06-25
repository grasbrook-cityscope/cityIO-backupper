import os
import json

# returns the config
def get_config():
    dir = os.path.dirname(__file__)
    # settings for the static input data
    with open(dir + '/config.json') as config_file:
        return json.load(config_file)
