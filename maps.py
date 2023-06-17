import googlemaps
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("MAPS_API_KEY")
gmaps = googlemaps.Client(key=api_key)

# Maps JavaScript API, Geocoding API, Places API:
def get_nearest_hospital(longitude, latitude):
    reverse_geocode = gmaps.reverse_geocode((latitude, longitude))
    address = reverse_geocode[0]['formatted_address']

    places_result = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=2000,  # Specify the radius in meters, adjust as needed
        type='hospital'
    )

    nearest_hospital = places_result['results'][0]
    name = nearest_hospital['name']
    place_id = nearest_hospital['place_id']

    details = gmaps.place(place_id=place_id, fields=['formatted_phone_number'])
    phone_number = details['result'].get('formatted_phone_number', 'Phone number not available')

    print(f"Your location: {address}")
    print(f"Nearest hospital: {name}")
    print(f"Contact number: {phone_number}")

    return name, phone_number, address


def get_google_maps_url(latitude, longitude):
    base_url = "https://www.google.com/maps/search/?api=1&query="

    # Create the coordinates part of the URL
    coordinates = f"{latitude},{longitude}"

    # Combine the base URL with the coordinates
    google_maps_url = base_url + coordinates

    return google_maps_url

