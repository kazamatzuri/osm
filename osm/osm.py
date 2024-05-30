# osm/osm.py

import logging

import matplotlib.pyplot as plt
import shapely.geometry as geom
from pyrosm import OSM, get_data
import gpxpy 

logger = logging.getLogger(__name__)

PBF_FILE = "us-northeast-latest.osm.pbf"

def load_gpx(gpx_file):
    """
    Loads a GPX file and returns a list of coordinates.

    Args:
        gpx_file: Path to the GPX file.

    Returns:
        A list of (longitude, latitude) tuples representing the track.
    """
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)

    trackpoints = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                trackpoints.append((point.longitude, point.latitude))

    return trackpoints

def plot_gpx_track(gpx_file, plt):
    """
    Loads and plots a GPX track on the given matplotlib axes.

    Args:
        gpx_file: Path to the GPX file.
        ax: The matplotlib axes object to plot on.
    """
    trackpoints = load_gpx(gpx_file)
    track_line = geom.LineString(trackpoints)
    plt.plot(*track_line.xy, color="blue", lw=2, alpha=0.8)


def main():
    """
    Main function for osm.py
    """
    logger.info("This is the main function in osm.py")

    bbox = geom.box(-72.08, 43.11, -70.96, 43.84)  # mvtr
    # bbox = geom.box(-71.609054, 42.899562, -71.402407, 43.044809) #bedford
    fp = get_data("New Hampshire")
    osm = OSM(fp, bounding_box=bbox)
    # osm = OSM(filepath=PBF_FILE, bounding_box=bbox)
    # roads = osm.get_network(network_type="driving")

    keys_to_keep = ["highway","place"]
    # Specifying key:value pairs to be filtered - this is the second level of filtering.
    data_filter = dict(
        highway=[            
            "primary","secondary","primary_link","secondary_link","tertiary","tertiary_link",
            "motorway",
            "motorway_link",
        ],
        place=["city"],
        service=["private"],
    )

    # Specifying if the above tags should be kept or removed
    filter_type = "keep"
    map_data = osm.get_data_by_custom_criteria(
        custom_filter=data_filter,
        osm_keys_to_keep=keys_to_keep,
        filter_type=filter_type,
        keep_nodes=False,
        keep_relations=False,
    )
    # roads = osm.get_network(network_type="driving")

    # Create a new figure
    fig, ax = plt.subplots(figsize=(16, 12))

    # Load the GPX track

    gpx_file = "gpx/bbr 101 ride.gpx"  # Replace with your GPX file path


    plot_gpx_track(gpx_file, plt)  # Pass the ax object


    # Plot the roads
    map_data.plot(color="k", ax=ax, lw=0.7, alpha=0.6)

    # Save the figure as an SVG file
    output_file = "roads.svg"
    fig.savefig(output_file, format="svg")

    plt.close(fig)

    # render_svg(roads, output_file)


if __name__ == "__main__":
    main()
