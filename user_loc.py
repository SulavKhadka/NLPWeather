import urllib2
import json


def loc():
    """Automatically geolocate the connecting IP
    :return: json string
    """
    try:
        f = urllib2.urlopen('http://freegeoip.net/json/')
    except urllib2.URLError:
        print "Please check to your internet connection"
        exit()
    json_string = f.read()
    f.close()
    location = json.loads(json_string)

    return location
