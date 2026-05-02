import requests
from flowtask.conf import GOOGLE_API_KEY

id_person = 'ChIJS9LH7ve42YgRYbz31IoVQgw'
id_store = 'ChIJ89oZVRK52YgRbakeZxjf8o8'


base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
params = {
    'origins': f"place_id:{id_person}",
    'destinations': f"place_id:{id_store}",
    'key': GOOGLE_API_KEY,
    'mode': 'driving',
    'units': 'imperial'
}

response = requests.get(base_url, params=params)
if response.status_code == 200:
    result = response.json()
    if result['status'] == 'OK':
        data = result['rows'][0]
        element = data['elements'][0]
        distance = element['distance']['text']
        duration = element['duration']['text']
        print('distance: ', distance, 'duration: ', duration)
