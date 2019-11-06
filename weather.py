#reach out to weather APIs and grab temperatures

from flask import Flask, render_template, request
import os
from api_key import get_api_key
import requests
from pprint import pprint
import json
from buoy_system import get_buoy_info

app = Flask(__name__)

locations_try = {'Seattle':'98117', 'Redmond':'98052', 'Bellevue':'98008', 'Renton':'98055', 'Tacoma':'98402'}
locations_coastal = {}
buoys = ['WPOW1', '46120']

api_token = "charlie265"
api_key = get_api_key(1)

def knots_conversion(speed):
    try:
        return round(speed *1.944,1)
    except:
        return speed

@app.route('/', methods = ['GET'])
def home():
    gathered_info = {}
    sorted_buoy_info = {}
    for city_name, zip_code in locations_try.items():
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&APPID={api_key}"
        response = requests.get(url).json()
        temp = round(((response['main']['temp'] - 273.15) * 9/5 + 32),1)
        wind_spd_knots = knots_conversion(response['wind']['speed'])
        weather_main = response['weather'][0]['main']
        weather_description = response['weather'][0]['description']
        gathered_info.update({response['name']:{
            'temp':temp,
            'wind_speed':wind_spd_knots,
            'weather_description':weather_description,
            'weather_main':weather_main
            }})
    buoy_info = get_buoy_info()
    for buoy in buoys:
        buoy_i = buoy_info[buoy]
        sorted_buoy_info.update({
            buoy:{
                'atmo_temp':buoy_i['atmo_temp'],
                'water_temp':buoy_i['water_temp'],
                'wind_speed':buoy_i['wind_speed'],
                'wind_dir':buoy_i['wind_dir'],
                'wind_dir_cardinal':buoy_i['wind_dir_cardinal'],
            }
        })
    return render_template('show_weather.jinja2',weathers=gathered_info,buoy_info=sorted_buoy_info)

"""
    3 = year
    4 = month
    5 = day
    6 = hour
    7 = minute
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
