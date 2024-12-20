# https://code.earthengine.google.com/register
# https://www.youtube.com/watch?v=_6JOA-iiEGU
# https://github.com/google/earthengine-community/blob/master/tutorials/beginners-cookbook/index.md
from pathlib import Path
import os
import numpy as np
import planetary_computer as pc
from pystac_client import Client
import typer
from loguru import logger
from tqdm import tqdm
from dotenv import load_dotenv
from shapely.geometry import Point, Polygon
import rasterio
from IPython.display import Image
from pystac.extensions.eo import EOExtension as eo
import folium
import webbrowser

import ee
import geehydro
import geemap


# from deforestation_in_africa.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from config import PROCESSED_DATA_DIR, RAW_DATA_DIR
# Load environment variables from .env file if it exists

ee.Authenticate()
ee.Initialize(project='ee-ms-deforestation')

app = typer.Typer()

@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    # input_path: Path = RAW_DATA_DIR  / "test.nc",
    input_path: Path = RAW_DATA_DIR ,# / "test.csv",
    output_path: Path = PROCESSED_DATA_DIR, # / "dataset.csv",
    # ----------------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Processing dataset...")
    start_date = '2005-05-01'
    end_date = '2005-05-04'
    # random region 
    roi = ee.Geometry.Rectangle([4.3, 3.8, 13.9, 14.7])
    # roi = ee.Geometry.Rectangle([-26.5, 43.2, -11.5, 50.5])
    # roi = ee.Geometry.Rectangle([-104.05, 49.05, -96.55, 45.05])

    # Filter the Landsat collection
    landsat = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").filterDate(start_date, end_date).filterBounds(roi)
    
    print(landsat.size().getInfo())
    # 10 -  number of images found

    # Create the folder if it doesn't exist
    # input_path = 'Landsat_Tiles'
    # if not os.path.exists(input_path):
    #     os.makedirs(input_path)
    # out_dir = os.path.join(os.getcwd(), input_path)


    # download images
    geemap.download_ee_image_collection(landsat, input_path, scale=30)

    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    # main()
    app()
