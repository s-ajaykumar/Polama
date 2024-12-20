import subprocess
import json 

def search_places(ambiguous_address):
    text = f'{{"textQuery" : "{ambiguous_address}"}}'
    curl_command = [
        "curl",
        "-X", "POST", "https://places.googleapis.com/v1/places:searchText",
        "-H", "Content-Type: application/json",
        "-H", 'X-Goog-Api-Key: AIzaSyBleud1_wi7WpsveLreqq-sDSOL2nJKDPQ',
        "-H", 'X-Goog-FieldMask: places.displayName,places.formattedAddress,places.priceLevel',
        "-d", text
    ]
    try:
        response = subprocess.run(curl_command, capture_output = True, text = True)
        j = json.loads(response.stdout)
        print(j['places'][0]['formattedAddress'])
    except Exception as e:
        print(response.stderr)
        print(e)
search_places("bose hospital, madurai")











'''gmaps = googlemaps.Client(key = 'AIzaSyBleud1_wi7WpsveLreqq-sDSOL2nJKDPQ')

response = gmaps.geocode("chinnakanmai street, madurai")
print(response)'''