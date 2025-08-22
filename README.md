# quantimize

## current progress
cli tool can download a specific map and save it as graphml dataset and list current catalog

```
❯ py .\main.py -h
usage: main.py [-h] [-l] [-d] [-n PLACE_NAME] [-t NETWORK_TYPE]

Download map data and more functions coming soon.

options:
  -h, --help            show this help message and exit
  -l, --list            List all available maps.
  -d, --download        Download the map data.
  -n PLACE_NAME, --place_name PLACE_NAME
                        Name of the place to download the map for.
  -t NETWORK_TYPE, --network_type NETWORK_TYPE
                        Type of network to download (e.g., 'drive', 'walk').

Example usage: python main.py --list python main.py -d -n 'Pune, India' -t 'drive'
```

## things to add
- [ ] ability to visualize path and output html
- [ ] the real fukin thing QUANTUM THINGY MAGIC  