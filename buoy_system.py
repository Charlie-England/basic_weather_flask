import requests
from pprint import pprint
from urllib import request

def wind_direction(degree):
    try:
        degree = float(degree)
    except:
        return degree
    if 0 <= degree < 11.25 or degree >= 348.75:
        return 'North'
    elif 11.25 <= degree < 33.75:
        return 'North-Northeast'
    elif 33.75 <= degree < 56.25:
        return "Northeast"
    elif 56.25 <= degree < 78.75:
        return "East-Northeast"
    elif 78.75 <= degree < 101.25:
        return "East"
    elif 101.25 <= degree < 123.75:
        return "East-Southeast"
    elif 123.75 <= degree < 146.25:
        return "Southeast"
    elif 146.25 <= degree < 168.75:
        return "South-Southeast"
    elif 168.75 <= degree < 191.25:
        return "South"
    elif 191.25 <= degree < 213.75:
        return "South-Southwest"
    elif 213.75 <= degree < 236.25:
        return "Southwest"
    elif 236.25 <= degree < 258.75:
        return "West-Southwest"
    elif 258.75 <= degree < 281.25:
        return "West"
    elif 281.25 <= degree < 303.75:
        return "West-Northwest"
    elif 303.75 <= degree < 325.25:
        return "Northwest"
    elif 325.25 <= degree < 348.75:
        return "North-Northwest"
    else:
        return f"Error in Wind_direction fxn {degree} given as {type(degree)}"
    
def fc(celcius):
    try:
        return (float(celcius)*(9/5)+32)
    except:
        return 'NAI'
def kc(speed):
    try:
        return round(float(speed) *1.944,1)
    except:
        return 'NAI'

def get_buoy_info():
    buoy_dict = {}
    response = request.urlopen("https://www.ndbc.noaa.gov/data/latest_obs/latest_obs.txt")
    # with open('latest_obs.txt','r') as response:
    for line in response.readlines()[2:]:
        line = line.decode('utf-8')
        txt_lst = line.split()
        buoy_dict.update({
            txt_lst[0]:{'lat':txt_lst[1],'lon':txt_lst[2],
            'year':txt_lst[3],'month':txt_lst[4],'day':txt_lst[5],
            'hour':txt_lst[6],'minute':txt_lst[7],'wind_dir':txt_lst[8],
            'wind_dir_cardinal':wind_direction(txt_lst[8]),'wind_speed':kc(txt_lst[9]),
            'atmo_temp':fc(txt_lst[17]),'water_temp':fc(txt_lst[18])
        }})

    return buoy_dict

# pprint(get_buoy_info())

