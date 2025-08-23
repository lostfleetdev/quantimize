import os
import json

catt = "mapdata/catalog.json"

def creatcatt():
    if not os.path.exists(catt):
        # creates a catalog file if it does not eist already
        with open(catt, 'w') as f:
            json.dump({}, f)

# pass a dictionary with map name and type
def list_maps():
    with open(catt, 'r') as f:
        catalog = json.load(f)
        if not catalog:
            print("No maps available in the catalog.")
            return
        print("-" * 40)
        for place, details in catalog.items():
            print(f"Place: {place}")
            print(f"  Network Type: {details['network_type']}")
            print(f"  Map File: {details['mapfile']}")
            print(f"  Nodes: {details['nodes']}, Edges: {details['edges']}")
            print("-" * 40)


# function to check if the map file exists at the path mentioned in catalog
# def check_map_exists(place_name, network_type):
#     creatcatt()
#     with open(catt, 'r') as f:
#         catalog = json.load(f)
#         if place_name in catalog:
#             if catalog[place_name]["network_type"] == network_type:
#                 return True
#     return False

def check_map_exists(place_name, network_type):
    creatcatt()
    with open(catt, 'r') as f:
        catalog = json.load(f)
    if place_name in catalog:
        entry = catalog[place_name]
        # ensure both network type matches AND file exists on disk
        if entry.get("network_type") == network_type and os.path.exists(entry.get("mapfile", "")):
            return True
    return False


# def add_to_catt(place_name, network_type, mapfilepath, nodes, edges):
#     creatcatt()
#     with open(catt, 'r+') as f:
#         catalog = json.load(f)
#         catalog[place_name] = {
#             "network_type": network_type,
#             "mapfile": mapfilepath,
#             "nodes": nodes,
#             "edges": edges
#         }
#         f.seek(0)
#         json.dump(catalog, f)

def add_to_catt(place_name, network_type, mapfilepath, nodes, edges):
    creatcatt()
    with open(catt, 'r+') as f:
        catalog = json.load(f)
        catalog[place_name] = {
            "network_type": network_type,
            "mapfile": mapfilepath,
            "nodes": nodes,
            "edges": edges
        }
        f.seek(0)
        json.dump(catalog, f, indent=2)
        f.truncate()
