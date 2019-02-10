import folium
import pandas
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

def get_locations(file):
    data = pandas.read_csv(file, error_bad_lines=False)
    movies_locations = zip(data["movie"], data["year"], data["location"])
    return movies_locations


# movies_locations = get_locations("locations.csv")


def coordinates_by_year(file, year):
    movies_locations = get_locations(file)
    coordinates = []
    geolocator = Nominatim(user_agent='name', timeout=None, scheme='http')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)
    for loc in movies_locations:
        try:
            if int(loc[1]) == year:
                location = geolocator.geocode(loc[2])
                print((location.latitude, location.longitude))
                coordinates.append([loc[0], location.latitude, location.longitude])
        except:
            continue
    return coordinates


map = folium.Map()

fg_movies = folium.FeatureGroup(name="Movies")
coordinates = coordinates_by_year("locations.csv", 1904)
for name, lt, ln in coordinates:
    fg_movies.add_child(folium.Marker(location=[lt, ln], popup=name, icon=folium.Icon()))


fg_pp = folium.FeatureGroup(name="Population")
fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                               encoding='utf-8-sig').read(),
                               style_function=lambda x: {'fillColor': 'green'
                                                         if x['properties']['POP2005'] < 10000000
                                                         else 'orange' if 10000000 <= x['properties']['POP2005'] <
                                                         20000000
                                                         else 'red'}))


map.add_child(fg_pp)
map.add_child(fg_movies)
map.add_child(folium.LayerControl())
map.save('map.html')



