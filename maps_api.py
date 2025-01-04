import googlemaps

class GoogleMapsAPI:
    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)

    def get_distance_matrix(self, origins, destinations):
        response = self.client.distance_matrix(origins, destinations)
        return response

    def get_route(self, origin, destination):
        response = self.client.directions(origin, destination)
        return response

    def validate_address(self, address):
        geocode_result = self.client.geocode(address)
        if geocode_result:
            return geocode_result[0]["formatted_address"]
        return None

def debug_response(response):
    import json
    return json.dumps(response, indent=2)
