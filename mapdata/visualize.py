# # mapdata/visualize.py
# import os
# import webbrowser
# import folium
# import mapdata.catalog as mc
# import osmnx as ox
# import networkx as nx
# from shapely.geometry import LineString

# # load graph from saved graphml
# def load_graph_from_catalog(place_name, network_type):
#     with open("mapdata/catalog.json", "r") as f:
#         catalog = __import__("json").load(f)
#     if place_name not in catalog:
#         raise FileNotFoundError(f"{place_name} not found in catalog.")
#     entry = catalog[place_name]
#     if entry["network_type"] != network_type:
#         raise ValueError("Network type mismatch.")
#     filepath = entry["mapfile"]
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f"GraphML file not found at {filepath}")
#     G = ox.load_graphml(filepath)
#     return G

# def center_of_graph(G):
#     # convert nodes to GeoDataFrame and compute centroid (lat, lon)
#     nodes_gdf, edges_gdf = ox.graph_to_gdfs(G, nodes=True, edges=True)
#     bounds = nodes_gdf.total_bounds  # [minx, miny, maxx, maxy]
#     center_x = (bounds[0] + bounds[2]) / 2.0
#     center_y = (bounds[1] + bounds[3]) / 2.0
#     # osmnx uses x=longitude, y=latitude
#     return (center_y, center_x)

# def _linestring_to_coords(ls: LineString):
#     # convert shapely LineString to list of [lat, lon] pairs for folium
#     coords = []
#     for x, y in ls.coords:
#         coords.append((y, x))
#     return coords

# def visualize_graph(place_name, network_type, output_html=None, open_in_browser=True, sample_edges=None):
#     """
#     Create an interactive HTML with folium showing the map graph.
#     sample_edges: if int, draw only first N edges (helpful for very large graphs)
#     """
#     G = load_graph_from_catalog(place_name, network_type)
#     center = center_of_graph(G)
#     m = folium.Map(location=center, zoom_start=13, control_scale=True)
#     nodes_gdf, edges_gdf = ox.graph_to_gdfs(G, nodes=True, edges=True)

#     # Optionally sample edges (large graphs are heavy to render)
#     if sample_edges and isinstance(sample_edges, int) and sample_edges > 0:
#         edges_iter = edges_gdf.iloc[:sample_edges].itertuples()
#     else:
#         edges_iter = edges_gdf.itertuples()

#     # draw edges
#     for e in edges_iter:
#         geom = e.geometry
#         # A geometry can be LineString or MultiLineString
#         if geom is None:
#             continue
#         if hasattr(geom, "geoms"):  # MultiLineString
#             for part in geom.geoms:
#                 coords = _linestring_to_coords(part)
#                 folium.PolyLine(coords, weight=1, opacity=0.6).add_to(m)
#         else:
#             coords = _linestring_to_coords(geom)
#             folium.PolyLine(coords, weight=1, opacity=0.6).add_to(m)

#     # Add small marker for center
#     folium.CircleMarker(location=center, radius=3, fill=True, tooltip=place_name).add_to(m)

#     if not output_html:
#         safe_name = f"{place_name}_{network_type}_map".replace("/", "_").replace(" ", "_")
#         output_html = f"mapdata/downloads/{safe_name}.html"
#     os.makedirs(os.path.dirname(output_html), exist_ok=True)
#     m.save(output_html)
#     print(f"Saved interactive map to {output_html}")
#     if open_in_browser:
#         webbrowser.open("file://" + os.path.abspath(output_html))
#     return output_html, G, m

# def visualize_path_on_graph(G, path_nodes, output_html="mapdata/downloads/path_map.html", open_in_browser=True):
#     """
#     Given a graph G and a list of node IDs path_nodes (in order), produce an HTML highlighting the path.
#     """
#     center = center_of_graph(G)
#     m = folium.Map(location=center, zoom_start=13, control_scale=True)

#     # draw full graph lightly (we'll sample edges for performance)
#     _, edges_gdf = ox.graph_to_gdfs(G, nodes=False, edges=True)
#     sample = 2000  # draw only first 2000 edges for background (change as needed)
#     for e in edges_gdf.iloc[:sample].itertuples():
#         geom = e.geometry
#         if geom is None:
#             continue
#         if hasattr(geom, "geoms"):
#             for part in geom.geoms:
#                 folium.PolyLine(_linestring_to_coords(part), weight=1, opacity=0.25).add_to(m)
#         else:
#             folium.PolyLine(_linestring_to_coords(geom), weight=1, opacity=0.25).add_to(m)

#     # build path coordinates from node lat/lng
#     path_coords = []
#     for n in path_nodes:
#         node_data = G.nodes[n]
#         lat = node_data.get("y")   # osmnx stores y as latitude
#         lon = node_data.get("x")
#         if lat is None or lon is None:
#             continue
#         path_coords.append((lat, lon))

#     # draw path
#     folium.PolyLine(path_coords, weight=6, opacity=0.9).add_to(m)
#     # mark start and end
#     if path_coords:
#         folium.Marker(location=path_coords[0], popup="start").add_to(m)
#         folium.Marker(location=path_coords[-1], popup="end").add_to(m)

#     os.makedirs(os.path.dirname(output_html), exist_ok=True)
#     m.save(output_html)
#     print(f"Saved path map to {output_html}")
#     if open_in_browser:
#         webbrowser.open("file://" + os.path.abspath(output_html))
#     return output_html, m

# def compute_and_visualize_shortest_path(place_name, network_type, start_lat, start_lon, end_lat, end_lon,
#                                         output_html=None, open_in_browser=True):
#     """
#     Find nearest nodes to start/end coords, compute shortest path by 'length', and visualize it.
#     start_lon, start_lat order matters for osmnx.nearest_nodes: (G, X, Y) with X=lon, Y=lat
#     """
#     G = load_graph_from_catalog(place_name, network_type)
#     # find nearest nodes
#     try:
#         orig_node = ox.nearest_nodes(G, start_lon, start_lat)
#         dest_node = ox.nearest_nodes(G, end_lon, end_lat)
#     except Exception:
#         # fallback using networkx helper (older/newer osmnx differences)
#         orig_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
#         dest_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

#     # compute shortest path
#     path = nx.shortest_path(G, orig_node, dest_node, weight="length")
#     # visualize path
#     if not output_html:
#         safe_name = f"{place_name}_{network_type}_path".replace("/", "_").replace(" ", "_")
#         output_html = f"mapdata/downloads/{safe_name}.html"
#     return visualize_path_on_graph(G, path, output_html=output_html, open_in_browser=open_in_browser)











# mapdata/visualize.py
import os
import webbrowser
from typing import Optional, Tuple, List

import folium
import osmnx as ox
import networkx as nx
from shapely.geometry import LineString
import json

CATT_PATH = "mapdata/catalog.json"


def _safe_filename(name: str) -> str:
    # remove chars that often cause issues in filenames
    return name.replace("/", "_").replace(",", "").replace(" ", "_")


def load_graph_from_catalog(place_name: str, network_type: str):
    """Load a graphml filepath stored in catalog.json for place_name."""
    if not os.path.exists(CATT_PATH):
        raise FileNotFoundError(f"Catalog not found at {CATT_PATH}")
    with open(CATT_PATH, "r") as f:
        catalog = json.load(f)
    if place_name not in catalog:
        raise FileNotFoundError(f"{place_name} not found in catalog.")
    entry = catalog[place_name]
    if entry.get("network_type") != network_type:
        raise ValueError("Network type mismatch.")
    filepath = entry.get("mapfile")
    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"GraphML file not found at {filepath}")
    G = ox.load_graphml(filepath)
    return G


def center_of_graph(G) -> Tuple[float, float]:
    """Return (lat, lon) center of the graph's bounding box."""
    nodes_gdf, edges_gdf = ox.graph_to_gdfs(G, nodes=True, edges=True)
    bounds = nodes_gdf.total_bounds  # [minx, miny, maxx, maxy]
    center_x = (bounds[0] + bounds[2]) / 2.0
    center_y = (bounds[1] + bounds[3]) / 2.0
    # osmnx uses x=lon, y=lat
    return (center_y, center_x)


def _linestring_to_coords(ls: LineString):
    coords = []
    for x, y in ls.coords:
        coords.append((y, x))
    return coords


def visualize_graph(
    place_name: str,
    network_type: str,
    output_html: Optional[str] = None,
    open_in_browser: bool = True,
    sample_edges: Optional[int] = None,
):
    """
    Create an interactive HTML with folium showing the map graph.
    If sample_edges is provided (int), only first N edges are drawn (helps performance).
    """
    G = load_graph_from_catalog(place_name, network_type)
    center = center_of_graph(G)
    m = folium.Map(location=center, zoom_start=13, control_scale=True)

    nodes_gdf, edges_gdf = ox.graph_to_gdfs(G, nodes=True, edges=True)

    if sample_edges and isinstance(sample_edges, int) and sample_edges > 0:
        edges_iter = edges_gdf.iloc[:sample_edges].itertuples()
    else:
        edges_iter = edges_gdf.itertuples()

    for e in edges_iter:
        geom = e.geometry
        if geom is None:
            continue
        if hasattr(geom, "geoms"):
            for part in geom.geoms:
                coords = _linestring_to_coords(part)
                folium.PolyLine(coords, weight=1, opacity=0.6).add_to(m)
        else:
            coords = _linestring_to_coords(geom)
            folium.PolyLine(coords, weight=1, opacity=0.6).add_to(m)

    folium.CircleMarker(location=center, radius=3, fill=True, tooltip=place_name).add_to(m)

    if not output_html:
        safe_name = _safe_filename(f"{place_name}_{network_type}_map")
        output_html = f"mapdata/downloads/{safe_name}.html"
    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    m.save(output_html)
    print(f"Saved interactive map to {output_html}")
    if open_in_browser:
        webbrowser.open("file://" + os.path.abspath(output_html))
    return output_html, G, m


# def visualize_path_on_graph(
#     G,
#     path_nodes: List[int],
#     output_html: str = "mapdata/downloads/path_map.html",
#     open_in_browser: bool = True,
#     background_sample: int = 2000,
# ):
#     """
#     Given a graph G and a list of node IDs path_nodes (in order), produce an HTML highlighting the path.
#     background_sample: number of edges to draw faintly as the map background for context.
#     """
#     center = center_of_graph(G)
#     m = folium.Map(location=center, zoom_start=13, control_scale=True)

#     # draw a sampled background of edges lightly
#     _, edges_gdf = ox.graph_to_gdfs(G, nodes=False, edges=True)
#     sample = min(len(edges_gdf), background_sample)
#     for e in edges_gdf.iloc[:sample].itertuples():
#         geom = e.geometry
#         if geom is None:
#             continue
#         if hasattr(geom, "geoms"):
#             for part in geom.geoms:
#                 folium.PolyLine(_linestring_to_coords(part), weight=1, opacity=0.15).add_to(m)
#         else:
#             folium.PolyLine(_linestring_to_coords(geom), weight=1, opacity=0.15).add_to(m)

#     # build path coordinates from nodes
#     path_coords = []
#     for n in path_nodes:
#         node_data = G.nodes[n]
#         # osmnx typically stores x=lon, y=lat but some graphs may use 'lat'/'lon'
#         lat = node_data.get("y") or node_data.get("lat") or node_data.get("latitude")
#         lon = node_data.get("x") or node_data.get("lon") or node_data.get("longitude")
#         if lat is None or lon is None:
#             continue
#         path_coords.append((lat, lon))

#     # draw path
#     if path_coords:
#         folium.PolyLine(path_coords, weight=6, opacity=0.9).add_to(m)
#         folium.Marker(location=path_coords[0], popup="start").add_to(m)
#         folium.Marker(location=path_coords[-1], popup="end").add_to(m)

#     os.makedirs(os.path.dirname(output_html), exist_ok=True)
#     m.save(output_html)
#     print(f"Saved path map to {output_html}")
#     if open_in_browser:
#         webbrowser.open("file://" + os.path.abspath(output_html))
#     return output_html, m

def visualize_path_on_graph(
    G,
    path_nodes: List[int],
    output_html: str = "mapdata/downloads/path_map.html",
    open_in_browser: bool = True,
    background_sample: int = 2000,
):
    """
    Given a graph G and a list of node IDs path_nodes (in order), produce an HTML highlighting the path.
    background_sample: number of edges to draw faintly as the map background for context.
    This implementation robustly handles multiple osmnx versions when calling graph_to_gdfs().
    """
    center = center_of_graph(G)
    m = folium.Map(location=center, zoom_start=13, control_scale=True)

    # --- robustly get edges_gdf from osmnx.graph_to_gdfs ---
    try:
        res = ox.graph_to_gdfs(G, nodes=False, edges=True)
        # res may be a GeoDataFrame, or a tuple/list containing one or more items.
        if isinstance(res, (tuple, list)):
            # try to find the GeoDataFrame-like object (has 'geometry' attribute)
            edges_gdf = None
            for item in res:
                if hasattr(item, "geometry"):
                    edges_gdf = item
                    break
            if edges_gdf is None:
                # fallback: assume last item is edges
                edges_gdf = res[-1]
        else:
            edges_gdf = res
    except Exception:
        # fallback: call full nodes+edges and take the edges (works for all versions)
        try:
            nodes_gdf, edges_gdf = ox.graph_to_gdfs(G, nodes=True, edges=True)
        except Exception as e:
            # as a last resort, raise a helpful error
            raise RuntimeError("Failed to extract edges GeoDataFrame from graph with osmnx.") from e

    # draw a sampled background of edges lightly
    sample = min(len(edges_gdf), background_sample) if edges_gdf is not None else 0
    if sample > 0:
        for e in edges_gdf.iloc[:sample].itertuples():
            geom = e.geometry
            if geom is None:
                continue
            if hasattr(geom, "geoms"):
                for part in geom.geoms:
                    folium.PolyLine(_linestring_to_coords(part), weight=1, opacity=0.15).add_to(m)
            else:
                folium.PolyLine(_linestring_to_coords(geom), weight=1, opacity=0.15).add_to(m)

    # build path coordinates from nodes
    path_coords = []
    for n in path_nodes:
        node_data = G.nodes[n]
        lat = node_data.get("y") or node_data.get("lat") or node_data.get("latitude")
        lon = node_data.get("x") or node_data.get("lon") or node_data.get("longitude")
        if lat is None or lon is None:
            continue
        path_coords.append((lat, lon))

    # draw path
    if path_coords:
        folium.PolyLine(path_coords, weight=6, opacity=0.9).add_to(m)
        folium.Marker(location=path_coords[0], popup="start").add_to(m)
        folium.Marker(location=path_coords[-1], popup="end").add_to(m)

    os.makedirs(os.path.dirname(output_html), exist_ok=True)
    m.save(output_html)
    print(f"Saved path map to {output_html}")
    if open_in_browser:
        webbrowser.open("file://" + os.path.abspath(output_html))
    return output_html, m


# ------------------- routing utilities -------------------


def add_travel_time(G, default_speeds=None):
    """
    Ensure each edge has a 'travel_time' attribute in seconds.
    default_speeds: dict mapping highway type -> speed_kph
    """
    if default_speeds is None:
        default_speeds = {
            "motorway": 80,
            "trunk": 70,
            "primary": 60,
            "secondary": 50,
            "tertiary": 40,
            "residential": 30,
            "service": 20,
            None: 30,
        }

    # iterate over multi-edges with keys where available
    if G.is_multigraph():
        edge_iter = G.edges(keys=True, data=True)
        for u, v, k, data in edge_iter:
            length_m = data.get("length")
            if length_m is None:
                data["travel_time"] = float("inf")
                continue

            speed_kph = None
            if "speed_kph" in data:
                try:
                    speed_kph = float(data["speed_kph"])
                except Exception:
                    speed_kph = None
            elif "maxspeed" in data:
                try:
                    speed_kph = float(str(data["maxspeed"]).split()[0])
                except Exception:
                    speed_kph = None

            if speed_kph is None:
                hw = data.get("highway")
                if isinstance(hw, list):
                    hw = hw[0]
                speed_kph = default_speeds.get(hw, default_speeds.get(None))

            speed_mps = max(0.1, float(speed_kph) * 1000.0 / 3600.0)
            data["travel_time"] = length_m / speed_mps
    else:
        for u, v, data in G.edges(data=True):
            length_m = data.get("length")
            if length_m is None:
                data["travel_time"] = float("inf")
                continue

            speed_kph = None
            if "speed_kph" in data:
                try:
                    speed_kph = float(data["speed_kph"])
                except Exception:
                    speed_kph = None
            elif "maxspeed" in data:
                try:
                    speed_kph = float(str(data["maxspeed"]).split()[0])
                except Exception:
                    speed_kph = None

            if speed_kph is None:
                hw = data.get("highway")
                if isinstance(hw, list):
                    hw = hw[0]
                speed_kph = default_speeds.get(hw, default_speeds.get(None))

            speed_mps = max(0.1, float(speed_kph) * 1000.0 / 3600.0)
            data["travel_time"] = length_m / speed_mps

    return G


def shortest_path_by_time(G, origin_point: Tuple[float, float], dest_point: Tuple[float, float]) -> List[int]:
    """
    origin_point, dest_point are (lat, lon).
    Returns list of node ids representing the shortest path by travel_time.
    """
    # find nearest nodes (handle osmnx API changes)
    try:
        orig = ox.nearest_nodes(G, origin_point[1], origin_point[0])
        dest = ox.nearest_nodes(G, dest_point[1], dest_point[0])
    except Exception:
        orig = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])
        dest = ox.distance.nearest_nodes(G, dest_point[1], dest_point[0])

    # if no travel_time attribute exists, add it
    if not any("travel_time" in d for _, _, d in G.edges(data=True)):
        G = add_travel_time(G)

    path = nx.shortest_path(G, orig, dest, weight="travel_time")
    return path


def compute_and_visualize_shortest_path(
    place_name: str,
    network_type: str,
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    output_html: Optional[str] = None,
    open_in_browser: bool = True,
):
    """
    Find nearest nodes to start/end coords, compute shortest path by 'travel_time', and visualize it.
    """
    G = load_graph_from_catalog(place_name, network_type)
    origin = (start_lat, start_lon)
    dest = (end_lat, end_lon)

    path_nodes = shortest_path_by_time(G, origin, dest)

    if not output_html:
        safe_name = _safe_filename(f"{place_name}_{network_type}_path")
        output_html = f"mapdata/downloads/{safe_name}.html"

    return visualize_path_on_graph(G, path_nodes, output_html=output_html, open_in_browser=open_in_browser)
