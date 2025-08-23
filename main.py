import argparse
import mapdata.down as md
import mapdata.catalog as mc
import mapdata.visualize as mv

def build_parser():
    parser = argparse.ArgumentParser(
        description="Download map data and more functions coming soon.",
        epilog="Example usage:\n"
               "  python main.py --list\n"
               "  python main.py -d -n 'Pune, India' -t drive\n"
               "  python main.py --visualize -n 'Pune, India' -t drive --sample_edges 2000"
    )

    # existing/basic functionality
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
        help="Type of network to download/visualize (e.g., 'drive', 'walk')."
    )

    # visualization & pathfinding
    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Create interactive HTML visualization of the map."
    )
    parser.add_argument("--output", type=str, help="Optional output HTML file path for visualization.")
    parser.add_argument("--sample_edges", type=int, help="If graph is huge, draw only first N edges (performance).")

    # optional path coordinates (for shortest path visualization)
    parser.add_argument("--start_lat", type=float, help="Start latitude for path visualization.")
    parser.add_argument("--start_lon", type=float, help="Start longitude for path visualization.")
    parser.add_argument("--end_lat", type=float, help="End latitude for path visualization.")
    parser.add_argument("--end_lon", type=float, help="End longitude for path visualization.")

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    # LIST maps
    if args.list:
        mc.list_maps()

    # DOWNLOAD map
    if args.download:
        if not args.place_name or not args.network_type:
            print("Please provide both --place_name (-n) and --network_type (-t) to download a map.")
        else:
            md.downmap(args.place_name, args.network_type)

    # VISUALIZE map or visualize shortest path
    if args.visualize:
        if not args.place_name or not args.network_type:
            print("Provide --place_name (-n) and --network_type (-t) for visualization.")
        else:
            # If start/end coordinates provided → compute shortest path and visualize
            if (args.start_lat is not None and args.start_lon is not None and
                args.end_lat is not None and args.end_lon is not None):
                mv.compute_and_visualize_shortest_path(
                    args.place_name, args.network_type,
                    args.start_lat, args.start_lon,
                    args.end_lat, args.end_lon,
                    output_html=args.output
                )
            else:
                mv.visualize_graph(
                    args.place_name, args.network_type,
                    output_html=args.output,
                    open_in_browser=True,
                    sample_edges=args.sample_edges
                )

if __name__ == "__main__":
    main()
