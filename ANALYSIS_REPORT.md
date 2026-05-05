# quantimize - project analysis report

## current status

`quantimize` is a working geospatial CLI prototype with real map ingestion, local dataset cataloging, interactive visualization, and shortest-path rendering. The core flow is implemented end to end:

1. Download network data from OpenStreetMap (via OSMnx) and save as GraphML.
2. Track local datasets in `mapdata/catalog.json`.
3. Render full-network HTML maps with Folium.
4. Compute and visualize shortest routes by estimated travel time.

The project is past "idea stage" and already in functional MVP territory.

## what is solid right now

- Clear CLI entrypoint (`main.py`) with list/download/visualize modes.
- Good module split: download (`down.py`), catalog (`catalog.py`), visualization + routing (`visualize.py`).
- Practical compatibility handling for OSMnx API variation in route visualization.
- Useful local-output behavior: GraphML + HTML artifacts in `mapdata/downloads/`.

## gaps and blockers

- `requirements.txt` is currently UTF-16 encoded (BOM + null-separated text). This can break dependency installation in common Linux/container flows.
- No automated tests or CI checks yet.
- No packaging metadata (`pyproject.toml`) and no pinned runtime target (Python version, OS matrix).
- Catalog model is keyed only by `place_name`, so a second download with another `network_type` for the same place overwrites the first entry.
- CLI has no structured logging, no exit codes for error states, and no explicit validation layer.

## code quality notes

- Naming consistency can be improved (`creat_dir`, `creatcatt`, `add_to_catt` typos).
- Path safety is mixed: visualization sanitizes output names, download path currently uses raw `place_name`.
- Error handling is straightforward and readable, but currently print-based and not yet production-grade.

## readiness summary

**Maturity:** Functional prototype / early MVP  
**Strength:** Real geospatial pipeline with tangible outputs  
**Main risk to deployability:** environment reproducibility and dependency/install reliability  
**Best next milestone:** make environment deterministic (`pyproject.toml` or lockfile), fix dependency file encoding, and add smoke tests for CLI flows

