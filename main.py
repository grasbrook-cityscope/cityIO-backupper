import cityio_socket
import json
import time
import config_loader
import os

# returns the token for the endpoint
# tokens.txt is to be requested from admin
def getToken(endpoint=0):
    try:
        with open("token.txt") as f:
            token = f.readline()
        if token == "": token = None  # happens with empty file
    except IOError:
        token = None

    return token

if __name__ == "__main__":
    number_of_endpoints = 8
    old_grid_hashes = [{}] * number_of_endpoints

    cwd = os.path.dirname(os.path.abspath(__file__))
    backups_dir = cwd + "/backups"

    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)

    while True:
        for endpoint in range (0,8):
            table_name = config_loader.get_config()['table_names'][endpoint]
            token = getToken(endpoint)

            print("endpoint", endpoint)
            print(table_name)

            oldHash = old_grid_hashes[endpoint]

            gridHash = cityio_socket.getCurrentState(int(endpoint), "meta/hashes/grid", token)
            print(gridHash)
            if gridHash != {} and gridHash != oldHash:
                endpoint_json = cityio_socket.getCurrentState(int(endpoint), "", token)
                with open(backups_dir + '/' + table_name + '.json', 'w') as outfile:
                    json.dump(endpoint_json, outfile)
                print("backup written for ", table_name, "to", backups_dir)

                old_grid_hashes[endpoint] = gridHash
            else:
                print("waiting for grid change")
                time.sleep(180)
