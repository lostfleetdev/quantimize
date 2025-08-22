import os
import osmnx as ox
import mapdata.catalog as mc

def creat_dir():
    if not os.path.exists("mapdata/downloads"):
        os.makedirs("mapdata/downloads")


def downmap(place_name, network_type):
    creat_dir()
    if mc.check_map_exists(place_name, network_type):
        print(f"Map for {place_name} with network type '{network_type}' already exists.")
        return
    else:
        print(f"Downloading map data for {place_name} with network type '{network_type}'...")
        G = ox.graph_from_place(place_name, network_type=network_type)
        filepath = f"mapdata/downloads/{place_name}_{network_type}_network.graphml"
        ox.save_graphml(G, filepath=filepath)

        print(f"Graph data for {place_name} saved successfully to '{filepath}'")
        print(f"Nodes: {len(G.nodes())}, Edges: {len(G.edges())}")
        
        # downloads the map and adds it to catalog
        mc.add_to_catt(place_name, network_type, filepath, len(G.nodes()), len(G.edges()))