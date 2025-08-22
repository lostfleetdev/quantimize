import os
import json

catt = "mapdata/catalog.json"

def creatcatt():
    if not os.path.exists(catt):
        # creates a catalog file if it does not eist already
        with open(catt, 'w') as f:
            json.dump({}, f)


def add_to_catt(place_name, network_type, mapfilepath):
    creatcatt()
    with open(catt, 'r+') as f:
        catalog = json.load(f)
        catalog[place_name] = {
            "network_type": network_type,
            "mapfile": mapfilepath
        }
        f.seek(0)
        json.dump(catalog, f)