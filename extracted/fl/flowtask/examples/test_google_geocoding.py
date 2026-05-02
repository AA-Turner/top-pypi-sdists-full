import requests
from flowtask.conf import GOOGLE_API_KEY

address = '5445 Knoll Creek Drive Apt K, Hazelwood, MO, 63042'
base_url = "https://maps.googleapis.com/maps/api/geocode/json"

params = {
    "address": address,
    "key": GOOGLE_API_KEY
}

response = requests.get(base_url, params=params)
if response.status_code == 200:
    result = response.json()
    print('RAW RESULT ', result)
    if result['status'] == 'OK':
        print('RESULT ', result['results'][0]['geometry']['location'])
