import folium
import pandas
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# map = folium.Map()
# map.save("map.html")

def get_locations(file):
    data = pandas.read_csv(file, error_bad_lines=False)
    locations = data["location"]
    return locations
locations = get_locations("locations.csv")


geolocator = Nominatim(user_agent="specify_your_app_name_here")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
for loc in locations:
    location = geolocator.geocode(loc)
    if location != None:
        print((location.latitude, location.longitude))
