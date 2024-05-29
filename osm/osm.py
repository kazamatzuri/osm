# osm/osm.py

from pyrosm import get_data, OSM
import svgwrite
import shapely.geometry as geom
import matplotlib.pyplot as plt
import logging
logger = logging.getLogger(__name__)

PBF_FILE="us-northeast-latest.osm.pbf"


def main():
    """
    Main function for osm.py
    """    
    logger.info("This is the main function in osm.py")

    bbox = geom.box(-71.5771,43.1367,-71.022833,43.46155)
    osm = OSM(filepath=PBF_FILE, bounding_box=bbox)
    roads = osm.get_network(network_type="driving")
    # roads.plot(color="k", figsize=(12,12), lw=0.7, alpha=0.6)
    # Create a new figure
    fig, ax = plt.subplots(figsize=(12,12))

    # Plot the roads
    roads.plot(color="k", ax=ax, lw=0.7, alpha=0.6)

    # Save the figure as an SVG file
    output_file="roads.svg"
    fig.savefig(output_file, format='svg')

    plt.close(fig)


    # render_svg(roads, output_file)

    
if __name__ == "__main__":
    main()