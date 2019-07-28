import smartcar
from flask import Flask, redirect, request, jsonify, render_template
from flask_cors import CORS
import geocoder
import math
import requests
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO
import urllib.request
import re


app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id= '',
    client_secret='',
    redirect_uri='http://localhost:8000/exchange',
    scope=['read_vehicle_info', 'read_location'],
    test_mode=True
)


@app.route('/login', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)


@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return '', 200


@app.route('/vehicle', methods=['GET'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    myloc = geocoder.ip("me")
    print(myloc.latlng)
    info = vehicle.info()
    print(info)
    response = vehicle.location()
    print(response)
    print(response["data"]["latitude"])
    car_long = response["data"]["longitude"]
    car_lat = response["data"]["latitude"]
    my_lat = myloc.latlng[0]
    my_long = myloc.latlng[1]

    long_difference = math.radians(my_long - car_long)
    lat_difference = math.radians(my_lat - car_lat)
    lat_average = (my_lat+car_lat)/2
    x = long_difference * math.cos(lat_average)
    vector_dist_from_car = round(math.sqrt(x*x + (lat_difference*lat_difference))*6371000,2)
    print(car_lat)
    print(car_long)

    # ROADS API
    analyze_url = 'https://roads.googleapis.com/v1/nearestRoads?points=' + str(car_lat) + ',' + str(car_long) + ''

    response = requests.post(analyze_url)
    response.raise_for_status()

    analysis = response.json()
    print(json.dumps(response.json()))

    if analysis == {}:
        lat = '43.662300'
        long = '-79.395777'
        car_lat = '43.662300'
        car_long = '-79.395777'

        vector_dist_from_car = 427.48
    else:
        lat = str(analysis['snappedPoints'][0]['location']['latitude'])
        long = str(analysis['snappedPoints'][0]['location']['longitude'])


    # END

    url2='https://maps.googleapis.com/maps/api/streetview?location=' + lat + ',' + long + '&size=456x456&key='
    url = "https://www.google.com/maps/embed/v1/directions?origin=" + str(my_lat) + ",+" + str(my_long) + "&destination=" + str(car_lat)+ ",+" + str(car_long)+ "&key="

    caption = computer_vision(url2)
    print(caption)
    return render_template('MapPage.html',caption=caption, url=url,url2=url2, dist=vector_dist_from_car)


@app.route('/FindMyWhip', methods=['GET'])
def find_my_whip():
    return render_template('HomePage.html')


def html(content):  # Also allows you to set your own <head></head> etc
   return '<html><head>custom head stuff here</head><body>' + content + '</body></html>'


@app.route('/incorrect_pass')
def incorrect_pass():
    return html('Incorrect password. <a href="/">Go back?</a>')


def computer_vision(url: str) -> None:
    # Replace <Subscription Key> with your valid subscription key.
    subscription_key = ""
    assert subscription_key

    vision_base_url = \
        "https://canadacentral.api.cognitive.microsoft.com/vision/v2.0/"

    analyze_url = vision_base_url + "analyze"

    image_url = url

    headers = {'Ocp-Apim-Subscription-Key': subscription_key }
    params = {'visualFeatures': 'Categories,Description,Color'}
    data = {'url': image_url}
    response = requests.post(analyze_url, headers=headers, params=params,
                             json=data)
    response.raise_for_status()

    analysis = response.json()
    print(json.dumps(response.json()))
    image_caption = analysis["description"]["captions"][0]["text"].capitalize()

    return image_caption


if __name__ == '__main__':
    app.run(port=8000)
