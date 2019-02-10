import folium
import pandas
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def get_locations(file):
    """
    (str) -> zip
    Reads file and returns zip object containing information from file.
    """
    data = pandas.read_csv(file, error_bad_lines=False)
    movies_locations = zip(data["movie"], data["year"], data["location"])
    return movies_locations


def coordinates_by_year(file, year):
    """
    (str, int) -> lst
    Reads file and returns coordinetes of movies filmed in given year.
    """
    movies_locations = get_locations(file)
    coordinates = []
    geolocator = Nominatim(user_agent='name', timeout=None, scheme='http')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)
    for loc in movies_locations:
        try:
            if int(loc[1]) == year:
                location = geolocator.geocode(loc[2])
                coordinates.append([loc[0], location.latitude, location.longitude])
        except:
            continue
    return coordinates


def fg_movies(year):
    """
    (int) -> folium.map.FeatureGroup
    Return a FeatureGroup containing places where films made in given year were filmed.
    """
    fg_mv = folium.FeatureGroup(name="Movies")
    coordinates = coordinates_by_year("locations.csv", year)
    for name, lt, ln in coordinates:
        fg_mv.add_child(folium.Marker(location=[lt, ln], popup=name, icon=folium.Icon()))
    return fg_mv


def fg_population():
    """
    () -> folium.map.FeatureGroup
    Return a FeatureGroup containing countries' boundaries and colors based on their population.
    """
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                                   encoding='utf-8-sig').read(),
                                   style_function=lambda x: {'fillColor': 'green'
                                                             if x['properties']['POP2005'] < 10000000
                                                             else 'orange' if 10000000 <= x['properties']['POP2005'] <
                                                             20000000
                                                             else 'red'}))
    return fg_pp


if __name__ == "__main__":
    map = folium.Map()
    year = int(input("Enter a year to show movies locations: "))
    fg_pp = fg_population()
    fg_mv = fg_movies(year)
    map.add_child(fg_pp)
    map.add_child(fg_mv)
    map.add_child(folium.LayerControl())
    map.save('map.html')
