import requests
import json
import urllib2
import datetime
from urllib2 import urlopen



    

def get_weather_now():

    f = urllib2.urlopen('http://api.wunderground.com/api/b32ef3297d82b842/geolookup/conditions/q/Ontario/Toronto.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)

    location = parsed_json['location']['city']
    weathercondition = parsed_json['current_observation']['weather']
    temp_c = parsed_json['current_observation']['temp_c']
    feelslike_c = parsed_json['current_observation']['feelslike_c']
    icon_url = parsed_json['current_observation']['icon_url']
    forecast_url = parsed_json['current_observation']['forecast_url']
    wind = parsed_json['current_observation']['wind_string']
    wind_dir = parsed_json['current_observation']['wind_dir']
    wind_kph = parsed_json['current_observation']['wind_kph']
    wind_metric = int(filter(unicode.isdigit, wind))
    rain = parsed_json['current_observation']['precip_today_metric']

    rain_line = "We've had %smm of rain today" % (rain) if float(rain) > 0 else ''
    bbq = 'FUCK YEAH BBQ TIME :hamburger: :beer:' if float(feelslike_c) > 15 and (weathercondition) == "Sunny" else ''

    now = datetime.date.today().strftime("%A")

    url = "https://hooks.slack.com/services/FUCKYOU"
    
    payload = {'username': "%s WeatherBot" % (now), 'text':"<%s|%s Weather>" % (forecast_url, location), 'icon_emoji': ":robot_face:", 
          'attachments':[
          {
             "fallback": "Weather Report",
             "title":'%s' % (now),
             "text": ('%s with a Temp of %s' + u"\u00B0" ' right meow' + '\nIt Really Feels like %s' + u"\u00B0" '\nExpect winds from the %s at %s km/h.' + '\n%s') % (weathercondition, temp_c, feelslike_c, wind_dir, wind_kph, rain_line) + bbq,
             "color":"#D00000",
             "thumb_url":'%s' % (icon_url),
          }
       ]}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
  

def get_weather_forecast():

    f = urllib2.urlopen('http://api.wunderground.com/api/b32ef3297d82b842/forecast/q/Ontario/Toronto.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)

    myweather_sum = parsed_json['forecast']['simpleforecast']['forecastday']

    now = datetime.date.today().strftime("%A")

    #def day1(myforday, myfctxt, icon_url):

    r = requests.get('http://api.wunderground.com/api/b32ef3297d82b842/forecast/q/Ontario/Toronto.json')
    data = r.json()

    url = "https://hooks.slack.com/services/FUCKYOU"

    payload = {'username': "%s WeatherBot" % (now), 'text':"Weather Report", 'icon_emoji': ":robot_face:", 
          'attachments':[]}

    colors = ["#F00000", "#0F0000", "#00F000", '#D00000']
    for i, day in enumerate(data['forecast']['simpleforecast']['forecastday']):
        rain = float(day['qpf_allday']['mm'])
        payload['attachments'].append({
             "fallback": "Weather Report",
             "title":'%s' % (day['date']['weekday']),
             "text": ('%s' " with a high of " + '%s' + u"\u00B0" + " and low of " + '%s' + u"\u00B0" + '\n%s') % (day['conditions'], day['high']['celsius'], day['low']['celsius'], "It will rain %s" % (rain) if (rain) > 0 else ''),
             "color":colors[i],
             "thumb_url":'%s' % (day['icon_url']),
          })

        #myforday = day['date']['weekday']
        #mycond = day['conditions']
        #mytemphigh = day['high']['celsius']
        #mytemplow = day['low']['celsius']
        #myiconurl = day['icon_url']
        #myrain = day['qpf_allday']['mm']




    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)
        

#get_weather_now()   
get_weather_forecast()
