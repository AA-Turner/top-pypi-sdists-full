import requests
import json
from flowtask.conf import GOOGLE_API_KEY

traveler = (25.7529793, -80.32231159999999)
stores = [
    (25.685314, -80.448545),
    (25.787051, -80.335332),
    (25.858609, -80.325508),
    (25.746027, -80.332788),
    (25.623903, -80.395205)
]


base_url = 'https://maps.googleapis.com/maps/api/directions/json'
params = {
    'origin': ",".join([str(x) for x in traveler]),
    'destination': ",".join([str(x) for x in traveler]),
    'key': GOOGLE_API_KEY,
    'waypoints': "optimize:true" + "|".join([",".join([str(x) for x in store]) for store in stores]),
    'mode': 'driving',
    'departure_time': 'now',
    'units': 'imperial'
}

response = requests.get(base_url, params=params)
if response.status_code == 200:
    result = response.json()
    print(json.dumps(result))
    if result['status'] == 'OK':
        # Extracting route, duration, and distance information
        route = result['routes'][0]
        total_duration = 0
        total_distance = 0

        for leg in route['legs']:
            total_duration += leg['duration']['value']  # Duration in seconds
            total_distance += leg['distance']['value']  # Distance in meters

        total_duration_min = total_duration / 60  # Convert duration to minutes
        total_distance_miles = total_distance / 1609.34  # Convert distance to miles

        print('Best Route:')
        for i, leg in enumerate(route['legs']):
            step = leg['steps'][0]
            print(f"Leg {i+1}: {step['html_instructions']} for {leg['distance']['text']}")

        print(
            f'Total Duration: {total_duration_min:.2f} minutes'
        )
        print(
            f'Total Distance: {total_distance_miles:.2f} miles'
        )
