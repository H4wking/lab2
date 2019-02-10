from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


geolocator = Nominatim(user_agent='name', timeout=None, scheme='http')
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)
location = geolocator.geocode("Tennessee USA")
print((location.latitude, location.longitude))