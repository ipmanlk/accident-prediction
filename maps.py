import googlemaps

api_key = ""
gmaps = googlemaps.Client(key=api_key)


# Maps JavaScript API, Geocoding API, Places API:
def get_nearest_hospital(longitude, latitude):
    reverse_geocode = gmaps.reverse_geocode((latitude, longitude))
    address = reverse_geocode[0]['formatted_address']

    places_result = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=5000,  # Specify the radius in meters, adjust as needed
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
