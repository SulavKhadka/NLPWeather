# NLPWeather

A very simple python script that uses your GeoIP to determine your location and retrieve your weather and return it in a english sentence. Works from command line or can be used to integrate into another project.

This script is a part of a bigger project I have called CHESTER. Currently I am using this in my Alarm Module.

## Requirements


wunderground.com api key: https://www.wunderground.com/weather/api/
  
## Usage


**Commad line:**
```
python Weather.py fullReport
python Weather.py shortReport
```
**Code Integration:**
```
import Weather
print Weather.report(fullReport, API_KEY) #Gets full weather report
print Weather.report(shortReport, API_KEY) #Gets basic weather report
```
