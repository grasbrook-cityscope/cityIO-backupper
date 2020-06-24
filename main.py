import cityio_socket
import json
import time
import config_loader
import os
from _datetime import datetime

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


def write_file_to_disk(target_dir, table, json_to_be_saved):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(target_dir + '/' + table + '.json', 'w') as outfile:
        json.dump(json_to_be_saved, outfile)
    print("backup written for ", table, "to", target_dir)


if __name__ == "__main__":
    number_of_endpoints = 8
    old_grid_hashes = [{}] * number_of_endpoints

    cwd = os.path.dirname(os.path.abspath(__file__))
    backups_dir = cwd + "/backups"

    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)

    sleep_interval = 10
    city_io_down_interval = 1800

    while True:
        for endpoint in range (0,8):
            table_name = config_loader.get_config()['table_names'][endpoint]
            token = getToken(endpoint)

            oldHash = old_grid_hashes[endpoint]

            gridHash = cityio_socket.getCurrentState(int(endpoint), "meta/hashes/grid", token)

            if not gridHash: # cityIO has crashed
                timestamp = datetime.now().strftime("%Y-%m-%d__%H:%M")
                permanent_backup_dir = backups_dir + '/' + str(timestamp)
                print("permanent backup to ", permanent_backup_dir)

                # loaded latest saved file for table and save it to a permanent backup directory
                with open(backups_dir + '/' + table_name + '.json', 'r') as jsonfile:
                    json_to_backup = json.load(jsonfile)

                write_file_to_disk(permanent_backup_dir, table_name, json_to_backup) # write backup to disk
                sleep_interval = city_io_down_interval # wait half an hour before checking again

            if gridHash != {} and gridHash != oldHash: # table state has changed
                endpoint_json = cityio_socket.getCurrentState(int(endpoint), "", token)
                write_file_to_disk(backups_dir, table_name, endpoint_json) # write lastest file to disk

                old_grid_hashes[endpoint] = gridHash
                sleep_interval = 10
            else: # table state has not changed
                print(table_name, "did not change")

        if sleep_interval == city_io_down_interval:
            print("wait for cityIO to come up again")
        else:
            print("waiting for changes in grids")

        time.sleep(sleep_interval)
