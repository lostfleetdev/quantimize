import mapdata.down as md
import argparse
import mapdata.catalog as mc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download map data and more functions coming soon.",
        epilog="Example usage: \n"
               "python main.py --list \n"
               "python main.py -d -n 'Pune, India' -t 'drive'"
    )
    parser.add_argument(
        "-l", "--list", 
        action="store_true",
        help="List all available maps."
    )
    parser.add_argument(
        "-d", "--download", 
        action="store_true",
        help="Download the map data."
    )
    parser.add_argument(
        "-n", "--place_name",
        type=str,
        help="Name of the place to download the map for."
    )
    parser.add_argument(
        "-t", "--network_type",
        type=str,
        help="Type of network to download (e.g., 'drive', 'walk')."
    )

    args = parser.parse_args()

    if args.list:
        mc.list_maps()
    if args.download and not args.place_name and not args.network_type:
        print("Please provide both --place_name and --network_type to download a map.")
    elif args.download:
        md.downmap(args.place_name, args.network_type)