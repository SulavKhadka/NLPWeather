"""Native libraries/modules"""
import urllib2
import json
import sys

"""External libraries/modules"""
import user_loc


def weather_info(API_KEY):
    """Retrieves Weather info from wunderground.com and parses the json and stores necessary items in a list
    :return: list
    """

    currloc = user_loc.loc()
    state = currloc['region_code']
    city = currloc['city']
    tz = currloc['time_zone']

    try:
        f = urllib2.urlopen('http://api.wunderground.com/api/%s/geolookup/conditions/q/%s/%s.json' % (API_KEY, state, city))
    except urllib2.URLError:
        print "Please check to your internet connection"
        exit()
    json_string = f.read()
    parsed_json = json.loads(json_string)
    f.close()

    try:
        location = parsed_json['location']['city']
    except KeyError:
        print "Invalid API key. please try again."
        exit()
    temp_f = parsed_json['current_observation']['temp_f']
    weather = parsed_json['current_observation']['weather']
    humidity = parsed_json['current_observation']['relative_humidity']
    windspeed = parsed_json['current_observation']['wind_mph']
    winddir = parsed_json['current_observation']['wind_dir']
    feelslike = parsed_json['current_observation']['feelslike_f']
    visibility = parsed_json['current_observation']['visibility_mi']
    if float(visibility) >= 10.0:
        visible_condition = "excellent"
    elif float(visibility) >= 5.0 < 10.0:
        visible_condition = "good"
    elif float(visibility) >= 2.0 < 5.0:
        visible_condition = "fair"
    elif float(visibility) > 0.5 < 2.0:
        visible_condition = "bad"
    else:
        visible_condition = "very bad"
    precip = parsed_json['current_observation']['precip_today_in']

    if float(precip) <= 0.0:
        precip = "It seems there is no rain in the forecast today."
    else:
        precip = "It is supposed to rain " + precip + " inches today."

    weather_data_lst = [weather, location, str(temp_f), humidity, winddir, str(int(windspeed)), feelslike, visible_condition, visibility, precip, tz]

    return weather_data_lst


def full_summary(weather_lst):
    """Summary of the weather for the TTS(currently not implemented).

    The if statement deletes the feels like sentence if the 'temperature' and the 'feels_like' variables are the same.
    :param weather_lst
    :return: string
    """

    if weather_lst[2] == weather_lst[6]:
        report = "It is " + weather_lst[0] + " and " + weather_lst[2] + " degrees right now in " + weather_lst[1] + " with winds of " + weather_lst[5] + " miles per hour. Visibility is " + weather_lst[7] + " with the range of " + weather_lst[8] + " miles. " + weather_lst[9]
    else:
        report = "It is " + weather_lst[0] + " and " + weather_lst[2] + " degrees right now in " + weather_lst[1] + " with winds of " + weather_lst[5] + " miles per hour. So it feels like " + weather_lst[6] + " degrees outside. Visibility is " + weather_lst[7] + " with the range of " + weather_lst[8] + " miles. " + weather_lst[9]

    return report


def short_summary(weather_lst):
    """Short summary of the weather for the TTS(currently not implemented).

    :param weather_lst
    :return: string
    """
    if weather_lst[2] == weather_lst[6]:
        report = "It is " + weather_lst[0] + " and " + weather_lst[2] + " degrees right now in " + weather_lst[1] + " with winds of " + weather_lst[5] + " miles per hour."
    return report


def report(reqData, API_KEY):
    """Receives the weather report based on the parameter
    :param reqData:
    :return: string
    """
    weather_data_lst = weather_info(API_KEY)
    if reqData == "fullReport":
        return full_summary(weather_data_lst)
    elif reqData == "shortReport":
        return short_summary(weather_data_lst)
    else:
        return "Invalid Argument"


if __name__ == '__main__':
    API_KEY = raw_input("Please enter your wunderground api key:")
    if len(sys.argv) != 2:
        print "%d of 2 Argument(s) found. Please enter 'fullReport' or  'shortReport' as argument." % len(sys.argv)
    else:
        print report(sys.argv[1], API_KEY)
