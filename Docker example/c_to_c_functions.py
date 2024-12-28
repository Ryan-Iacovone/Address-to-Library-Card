import requests
import math
from geopy.geocoders import Nominatim
import pandas as pd

# Using the geopy library to take a street address as input and return lat and long coordinates
def get_coordinates(street_address):
    geolocator = Nominatim(user_agent="my_app")

    location = geolocator.geocode(street_address, timeout=5)

    if location:
        latitude = round(location.latitude, 5)
        longitude = round(location.longitude, 5)

        return latitude, longitude

# Takes coordinates and returns county subdivision

# Function to take latitude and longitude and return tile coordinates (which is what census reporter uses)
# Tile coordinates, also known as tiling or grid coordinates, are a way to divide a geographic area into small, rectangular tiles, typically used in web mapping applications like Google Maps or 
#       OpenStreetMap. Each tile has a unique identifier that can be used to locate the corresponding piece of map data.
# Latitude and longitude, on the other hand, are geographic coordinates that describe the location of a point on the Earth's surface in terms of its angular distance from the equator 
#       (latitude) and the Prime Meridian (longitude).

def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom
    x_tile = int((lon + 180.0) / 360.0 * n)
    y_tile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return x_tile, y_tile

def coordinates_to_csubdivision(latitude, longitude):
    # Static Parameters
    release = "latest"
    sumlevel = "060"  # Summary level for county subdivisions
    zoom = 20  # Higher zoom level for more detail
    # latitude, longitude values taken dynamically from get_coordinates() function

    # Convert latitude and longitude to tile x and y
    x, y = latlon_to_tile(latitude, longitude, zoom)

    # URL format from census reporter API Docs https://github.com/censusreporter/census-api/blob/master/API.md
    url = f"https://api.censusreporter.org/1.0/geo/{release}/tiles/{sumlevel}/{zoom}/{x}/{y}.geojson"

    # Making request to census reporter 
    response = requests.get(url)
    data = response.json()

    # Parsing the returned GeoJson output, only returning county subdivision
    full_name = data['features'][0]['properties']['name']
    county_subdivision = full_name.split(",")[0]

    return county_subdivision, full_name

# List repository: 

## list of KDL townships to search against
kdl_townships = ['ada township', 'algoma township', 'alpine township', 'bowne township',
                  'byron township', 'caledonia charter township', 'cannon township', 'cascade charter township',
                  'courtland township', 'east grand rapids city', 'gaines charter township', 'grand rapids charter township',
                  'grandville city', 'grattan township', 'kentwood city', 'lowell charter township',
                  'lowell city', 'nelson township', 'oakfield township', 'plainfield charter township',
                  'rockford city', 'spencer township', 'tyrone township', 'vergennes township',
                  'walker city', 'wyoming city']
                  
## list of LLC townships to search against          
table = pd.read_excel("LLC service.xlsx", sheet_name="try") # calls charter townships just townships 

table["CountySub"] = table["Name"] + ' ' + table["City/Township/Village"]

llc = table[~table["Served by"].isin(["Kent District Library", "Grand Rapids Public Library"])]

# lowering the case of the CountySub variable to match output 
llc['CountySub'] = llc['CountySub'].str.lower()

# Need to change llc_townships from a series to a list because otherwise I won't be able to proper search in it
llc_townships_list = llc['CountySub'].tolist()

# Creating dictionary with county sub and the library they serve
llc_dict = llc.set_index("CountySub")["Served by"].to_dict()