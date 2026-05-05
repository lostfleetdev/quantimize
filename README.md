# quantimize

Quantimize is a map intelligence CLI that pulls real OpenStreetMap road networks, stores them as reusable GraphML datasets, and turns them into interactive HTML maps with route overlays.  
It is fast to run, easy to inspect, and already useful for routing experiments and geospatial demos.

## what it can do right now

- Download road networks for any place supported by OSM (`drive`, `walk`, etc.).
- Save networks as GraphML for reuse and offline analysis.
- Keep a local dataset catalog with node/edge counts.
- Generate interactive Folium map visualizations.
- Compute shortest paths by estimated travel time and render the route.

## stack

- Python
- OSMnx + NetworkX
- Folium
- GeoPandas + Shapely

## quick start (uv)

1. Install [uv](https://docs.astral.sh/uv/).
2. From this folder, create and activate a virtual environment:
   - Windows PowerShell:
     ```powershell
     uv venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     uv venv
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## CLI usage

```bash
python main.py -h
```

### list downloaded maps

```bash
python main.py --list
```

### download a map

```bash
python main.py --download --place_name "Pune, India" --network_type drive
```

### visualize full map

```bash
python main.py --visualize --place_name "Pune, India" --network_type drive --sample_edges 2000
```

### visualize shortest path by travel time

```bash
python main.py --visualize --place_name "Pune, India" --network_type drive \
  --start_lat 18.5204 --start_lon 73.8567 \
  --end_lat 18.5314 --end_lon 73.8446
```

This creates an HTML map in `mapdata/downloads/` and opens it in your browser.

## project structure

```
quantimize/
  main.py
  requirements.txt
  mapdata/
    down.py
    catalog.py
    visualize.py
    downloads/        # generated GraphML + HTML output
    catalog.json      # generated local index
```
