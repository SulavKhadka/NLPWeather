import requests
import json


def loc():
    """Automatically geolocate the connecting IP
    :return: json string
    """
    try:
        f = requests.get('http://freegeoip.net/json/')
    except (requests.exceptions.ConnectionError,
            requests.exceptions.SSLError,
            requests.exceptions.Timeout) as e:

        print("Could not get IP. Error message: \n{}".format(e))
        exit()

    json_string = f.text
    f.close()
    location = json.loads(json_string)

    return location
