from pathlib import Path
import os
from pystac_client import Client  # Import the Client class from pystac_client library #https://pystac-client.readthedocs.io/en/stable/api.html#pystac_client.Client.search
from odc.stac import load  # Import the load function from the odc.stac module
import matplotlib.pyplot as plt  # Import the pyplot module from the matplotlib library
from IPython.display import Image

import typer
from loguru import logger
from tqdm import tqdm

# from deforestation_in_africa.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()

@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    # input_path: Path = RAW_DATA_DIR  / "test.nc",
    input_path: Path = RAW_DATA_DIR  / "test.csv",
    output_path: Path = PROCESSED_DATA_DIR, # / "dataset.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    # Connect to the STAC API endpoint
    client = Client.open("http://earth-search.aws.element84.com/v1")

    # Specify the desired collection
    collection = "sentinel-2-l2a"
    # collection = "landsat-c2-l2"

    # Define a bounding box for the search area [min_lon, min_lat, max_lon, max_lat]
    # ant_bbox = [30.444946, 36.804887, 30.933837, 37.059561]
    # ant_bbox = [3.8, 4.3, 14.7, 13.9]
    ant_bbox = [8.0, 4.5, 10.0, 6.8]

    # Perform a search using the specified parameters
    search = client.search(collections=[collection], bbox=ant_bbox, datetime="2019-12")
    logger.info("Searching API complete")
    
    
    # Load data using the odc.stac load function based on the search results
    data = load(search.items(), bbox=ant_bbox, groupby="solar_day", chunks={})
    logger.info("Loading data complete")
    
    # data.to_netcdf(input_path)
    data.to_dataframe().to_csv(input_path)

    # Select a single time slice (e.g., the first time step) from the loaded data
    data_slice = data.isel(time=0)
    
    # Plotting the "red", "green", and "blue" bands individually
    plt.figure(figsize=(15, 5))  # Adjusted the total size of the figure

    # Adjusting the space between subplots
    plt.subplots_adjust(wspace=0.4)  # Change the value according to your preference

    # Subplot 1
    plt.subplot(131)
    data_slice["red"].plot.imshow(robust=True)
    plt.title("Red Band")

    # Subplot 2
    plt.subplot(132)
    data_slice["green"].plot.imshow(robust=True)
    plt.title("Green Band")

    # Subplot 3
    plt.subplot(133)
    data_slice["blue"].plot.imshow(robust=True)
    plt.title("Blue Band")

    plt.show()
    
    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    # main()
    app()
