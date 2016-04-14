import requests
import json
import urllib2
import datetime


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
rain = parsed_json['current_observation']['precip_today_metric']

rain_line = "We've had %smm of rain today" % (rain) if float(rain) > 0 else ''
bbq = 'FUCK YEAH BBQ TIME :hamburger: :beer:' if float(feelslike_c) > 15 and (weathercondition) == "Sunny" else ''

now = datetime.datetime.now()

url = "https://hooks.slack.com/services/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"
payload = {'username': "%s WeatherBot" % (now.strftime("%A")), 'text':"<%s|%s Weather>" % (forecast_url, location), 'icon_emoji': ":robot_face:", 'attachments':[
      {
         "fallback": "Weather Report",
         "title":'%s' % (now.strftime("%A")),
         "text": ('%s with a Temp of %s' + u"\u00B0" ' right meow' + '\nIt Really Feels like %s' + u"\u00B0" '\nExpect winds %s' + '\n%s') % (weathercondition, temp_c, feelslike_c, wind, rain_line) + bbq,
         "color":"#D00000",
         "thumb_url":'%s' % (icon_url),
      }
   ]}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(payload), headers=headers)   


myweather = json.load(urllib2.urlopen("http://api.wunderground.com/api/b32ef3297d82b842/forecast/q/Ontario/Toronto.json"))
myweather_sum = myweather['forecast']['txt_forecast']['forecastday']

for period in myweather_sum:
    if period['period'] == 1:
        myforday = period['title']
        myfctxt = period['fcttext_metric']
        

url = "https://hooks.slack.com/services/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"
payload = {'username': "%s WeatherBot" % (now.strftime("%A")), 'icon_emoji': ":robot_face:", 'attachments':[
      {
         "fallback": "Weather Report",
         "title":'%s' % (myforday),
         "text": '%s' % (myfctxt),
         "color":"#D00000",
         "thumb_url":'%s' % (icon_url),
      }
   ]}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(payload), headers=headers)




f.close()