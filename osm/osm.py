# osm/osm.py

import logging
import os

import matplotlib.pyplot as plt
import shapely.geometry as geom
from pyrosm import OSM, get_data
import gpxpy 

logger = logging.getLogger(__name__)

PBF_FILE = "us-northeast-latest.osm.pbf"

def load_gpx(gpx_file):
    """
    Loads a GPX file and returns a list of LineString objects, one for each track.

    Args:
        gpx_file: Path to the GPX file.

    Returns:
        A list of shapely.geometry.LineString objects representing the tracks.
    """
    with open(gpx_file, 'r') as f:
        gpx = gpxpy.parse(f)

    tracks = []  # List to store LineString objects for each track

    for track in gpx.tracks:
        trackpoints = []  # List to store points for the current track
        for segment in track.segments:
            for point in segment.points:
                trackpoints.append((point.longitude, point.latitude))

        # Create a LineString for the current track and add it to the list
        track_line = geom.LineString(trackpoints)
        tracks.append(track_line)

    return tracks


def plot_gpx_track(gpx_file, plt):
    """
    Loads and plots GPX tracks on the given matplotlib axes.

    Args:
        gpx_file: Path to the GPX file.
        ax: The matplotlib axes object to plot on.
    """
    tracks = load_gpx(gpx_file)  # Get the list of LineString objects

    for track in tracks:  # Iterate through tracks
        plt.plot(*track.xy, color="blue", lw=2, alpha=0.8)



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


    # Plot the roads
    map_data.plot(color="k", ax=ax, lw=0.7, alpha=0.6)

    # ... (rest of your code)
    
    city_labels = []
    for index, row in map_data.iterrows():
        if row.geometry.geom_type == "Point" and "place" in row and row["place"] == "city":
            # Extract city name and coordinates from the 'row'
            city_name = row.get("name", "Unnamed City")
            city_labels.append((row.geometry.x, row.geometry.y, city_name))

    

    
    # Plot city labels
    for x, y, label in city_labels:
        plt.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points")
    
    # Load the GPX track

    gpx_dir = "gpx"

    # Loop through GPX files
    for filename in os.listdir(gpx_dir):
        if filename.endswith(".gpx"):
            gpx_file = os.path.join(gpx_dir, filename)
            plot_gpx_track(gpx_file, plt)  # Pass the ax object





    # Save the figure as an SVG file
    output_file = "roads.svg"
    fig.savefig(output_file, format="svg")

    plt.close(fig)

    # render_svg(roads, output_file)


if __name__ == "__main__":
    main()
