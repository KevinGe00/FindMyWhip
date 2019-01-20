import smartcar
from flask import Flask, redirect, request, jsonify, render_template
from flask_cors import CORS
import geocoder


app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None

client = smartcar.AuthClient(
    client_id= '7126d3ad-f1bf-4712-b484-2e450efa1d5f',
    client_secret='36f18730-00e6-4b36-ae24-adbb44b59fa8',
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
    car_lat = response["data"][ "latitude"]
    my_lat = myloc.latlng[0]
    my_long = myloc.latlng[1]
    url = "https://www.google.com/maps/embed/v1/directions?origin=" + str(my_lat) + ",+" + str(my_long) + "&destination=" + str(car_lat)+ ",+" + str(car_long)+ "&key=AIzaSyA7J_WSo3Cefq_Q9-NhUW8ievnZw7J2cHE&"
    return render_template('MapPage.html', url=url)


@app.route('/FindMyWhip', methods=['GET'])
def find_my_whip():
    return render_template('HomePage.html')


def html(content):  # Also allows you to set your own <head></head> etc
   return '<html><head>custom head stuff here</head><body>' + content + '</body></html>'


@app.route('/incorrect_pass')
def incorrect_pass():
    return html('Incorrect password. <a href="/">Go back?</a>')





if __name__ == '__main__':
    app.run(port=8000)
