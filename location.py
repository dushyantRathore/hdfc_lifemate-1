import requests
import json

from googleplaces import GooglePlaces, types
import googlemaps

url = 'https://maps.googleapis.com/maps/api/place/details/output?parameters'

YOUR_API_KEY = 'AIzaSyBJuXDLb0vwzRtI8a_xZLEjxojylfJ6GiE'


# print 'fetching....'


def find_contacts(location, type):
    gmaps = googlemaps.Client(key='AIzaSyDph9boEoD8gqNKmQvvai3c8Dpp20grxP0')
    print 'LOCCC', str(location)
    google_places = GooglePlaces(YOUR_API_KEY)

    loc_type = {'insurance': [types.TYPE_INSURANCE_AGENCY],
                'police': [types.TYPE_POLICE],
                'fire_station': [types.TYPE_FIRE_STATION],
                'all': [types.TYPE_HOSPITAL, types.TYPE_POLICE, types.TYPE_FIRE_STATION]
                }

    query_result = google_places.nearby_search(
        lat_lng=location,
        types=loc_type[type],
        keyword="HDFC",
        rankby="distance")

    results = []

    for place in query_result.places:
        # Returned places from a query are place summaries.
        # print place.name
        # print place.geo_location
        # print place.place_id


        # The following method has to make a further API call.
        place.get_details()
        # Referencing any of the attributes below, prior to making a call to
        # get_details() will raise a googleplaces.GooglePlacesAttributeError.
        # print place.details # A dict matching the JSON response from Google.
        # print place.local_phone_number
        # print place.international_phone_number
        # print place.website
        # print place.url
        image_url = ""
        # # Getting place photos
        for photo in place.photos:
            print photo
            # 'maxheight' or 'maxwidth' is required
            photo.get(maxheight=500, maxwidth=500)
            # # MIME-type, e.g. 'image/jpeg'
            photo.mimetype
            # # Image URL
            image_url = photo.url
            print image_url
            # Original filename (optional)
            photo.filename
            # Raw image data
            photo.data
        url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&language=en-EN&sensor=false" % (
        str(location['lat']) + ',' + str(location['lng']),
        str(place.geo_location['lat']) + ',' + str(place.geo_location['lng']))
        # print url
        req = requests.get(url)
        res = json.loads(req.text)
        driving_time = ''
        distance = ''
        try:
            driving_time = res['rows'][0]['elements'][0]['duration']['text']
            distance = res['rows'][0]['elements'][0]['distance']['text']
        except:
            pass
        nav_url = "https://www.google.co.in/maps/dir/%s/%s" % (str(location['lat']) + ',' + str(location['lng']),
                                                               str(place.geo_location['lat']) + ',' + str(place.geo_location['lng']))
        components = place.details["address_components"]
        city = "India"
        if components:
          try:
            for c in components:
              if "locality" in c["types"]:
                city = c["short_name"]
          except:
            pass
        if city=="India":
          try:
            for c in components:
              if "administrative_area_level_1" in c["types"]:
                city = c["short_name"]
          except:
            pass
        if place.local_phone_number:
          results.append({
              'name': place.name,
              'location': {'lat': str(place.geo_location['lat']), 'lng': str(place.geo_location['lng'])},
              'phone': place.local_phone_number,
              'address': place.formatted_address,
              'distance': distance,
              'time': driving_time,
              'url': nav_url,
              'city': city,
              'image_url': image_url
          })
        if len(results) > 2:
            return json.dumps(results)
    return json.dumps(results)

#print find_contacts({"lat":19.1163957, "lng":72.9047135}, "insurance")