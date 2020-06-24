import json
import requests
from config_loader import get_config

def getCurrentState(endpoint, topic="", token=None):
    config = get_config()
    get_address = config['table_urls'][endpoint]+topic

    try:

        if token is None or endpoint == -1 or endpoint is None:
            r = requests.get(get_address, headers={'Content-Type': 'application/json'})
        else:
            r = requests.get(get_address, headers={'Content-Type': 'application/json',
                                                   'Authorization': 'Bearer {}'.format(token).rstrip()})
        if not r.status_code == 200:
            print("could not get from cityIO", get_address)
            print("Error code", r.status_code)
            return {}
    # exit on request execption (cityIO down)
    except requests.exceptions.RequestException as e:
        print("CityIO seems down." + str(e))

        return None

    return r.json()
