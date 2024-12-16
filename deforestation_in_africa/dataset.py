from pathlib import Path
import os
import folium
import numpy as np
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import geopandas as gpd
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
from IPython.display import Image
from shapely.geometry import MultiPolygon,Polygon
import fiona 
import wget
import typer
from loguru import logger
from tqdm import tqdm
from dotenv import load_dotenv

# from deforestation_in_africa.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from config import PROCESSED_DATA_DIR, RAW_DATA_DIR
# Load environment variables from .env file if it exists
project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')
load_dotenv(dotenv_path)
user = os.environ.get("SENTINEL_USER")
pw = os.environ.get("SENTINEL_PW")

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
    api = SentinelAPI(user,pw,'https://scihub.copernicus.eu/dhus')
    
    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    # main()
    app()
