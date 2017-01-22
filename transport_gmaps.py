import googlemaps
import json

class transport():

    def __init__(self, address, apikey, destination = "Flinders St Station" ):
        self.address = address
        self.destination = destination
        self.gmaps = googlemaps.Client(key=apikey)

    def google_maps_request(self,method):
        try:
            directions = self.gmaps.directions(
                self.address,
                self.destination,
                mode = method
            )
            return directions[0]
        except:
            return "Unable to access Google Maps"

    def driving(self):
        return self.google_maps_request("driving")

    def public_transport(self):
        return self.google_maps_request("transit")