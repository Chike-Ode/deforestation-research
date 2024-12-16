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


# from deforestation_in_africa.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from config import PROCESSED_DATA_DIR, RAW_DATA_DIR
# Load environment variables from .env file if it exists
project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')
load_dotenv(dotenv_path)
user = os.environ.get("SENTINEL_USER")
pw = os.environ.get("SENTINEL_PW")

app = typer.Typer()

def get_aoi(latitude, longitude, buffer):
  
  # the first step is to create a point from the lat and long degrees, using shapely
  point = Point(latitude, longitude)

  # add the required distance/buffer around the lat lon
  bbox = point.buffer(buffer).bounds

  # next create a polygon from the bounding box
  polygon = Polygon([(bbox[0], bbox[1]), (bbox[0], bbox[3]), (bbox[2], bbox[3]), (bbox[2], bbox[1])])

  min_lat = latitude - buffer
  max_lat = latitude + buffer
  min_lon = longitude - buffer
  max_lon = longitude + buffer

  return polygon, min_lat, max_lat, min_lon, max_lon


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
    catalog = Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1", modifier=pc.sign_inplace
    )
    bbox, min_lat, max_lat, min_lon, max_lon = get_aoi(39.080319, -86.430867, 0.1) # here we are taking 0.01 degrees buffer, which is equivalent to around 1 km in distance

    
    # Create a folium map object and set the center to the original latitude and longitude coordinates
    m = folium.Map(location=[39.080319, -86.430867], zoom_start=15)

    # Add a bounding box to the map using the calculated minimum and maximum latitude and longitude values

    folium.Rectangle(
        bounds=[[min_lat, min_lon], [max_lat, max_lon]],
        color='red',
        fill=False,
    ).add_to(m)

    m
    m.save("map.html")
    webbrowser.open("map.html")


    # time_of_interest = "2022-05-01/2022-05-30"

    # bbox, min_lat, max_lat, min_lon, max_lon = get_aoi(39.080319, -86.430867, 0.1) # here we are taking 0.01 degrees buffer, which is equivalent to around 1 km in distance



    # search = catalog.search(
    #     collections=["sentinel-2-l2a"],
    #     intersects=bbox,
    #     datetime=time_of_interest,
    #     query={"eo:cloud_cover": {"lt": 20}},
    # )

    # # Check how many items were returned
    # items = search.item_collection()
    
    # least_cloudy_item = min(items, key=lambda item: eo.ext(item).cloud_cover)

    # print(
    #     f"Choosing {least_cloudy_item.id} from {least_cloudy_item.datetime.date()}"
    #     f" with {eo.ext(least_cloudy_item).cloud_cover}% cloud cover"
    # )
    # print(f"Returned {len(items)} Items")
    
    # # What assets are available?
    # for asset_key, asset in least_cloudy_item.assets.items():
    #     print(f"{asset_key:<25} - {asset.title}")
        
        
    # Image(url=least_cloudy_item.assets["rendered_preview"].href)
    
    # # figure(figsize=(8, 6), dpi=80)

    # tiff = rasterio.open(least_cloudy_item.assets['SCL'].href)
    # rasterio.plot.show(tiff, title = "scene classification layer of our AOI")
    logger.success("Processing dataset complete.")
    # -----------------------------------------


if __name__ == "__main__":
    # main()
    app()
