"""Generate a weather-report based on the user's location.

The script uses GeoIP to determine the user's location based on the IP and
retrieves the weather, which is then returned it in a english sentence.
"""

# Native libraries/modules
import json
import sys
import urllib2

# External libraries/modules
import user_loc


def weather_info(api_key):
    """Retrieve and parse Weather info from wunderground.com.

    :return: list
    """
    currloc = user_loc.loc()
    state = currloc['region_code']
    city = currloc['city']
    tme_zone = currloc['time_zone']

    try:
        data = urllib2.urlopen(
            'http://api.wunderground.com/api/{}/geolookup/conditions'
            '/q/{}/{}.json'.format(api_key, state, city))
    except urllib2.URLError:
        print "Please check to your internet connection"
        exit()
    json_string = data.read()
    parsed_json = json.loads(json_string)
    data.close()

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

    weather_data_lst = [weather, location, str(temp_f), humidity, winddir,
                        str(int(windspeed)), feelslike, visible_condition,
                        visibility, precip, tme_zone]

    return weather_data_lst


def full_summary(weather_lst):
    """Summarize the weather for the TTS (currently not implemented).

    The if statement deletes the feels like sentence if the 'temperature' and
    the 'feels_like' variables are the same.
    :param weather_lst
    :return: string
    """
    if weather_lst[2] == weather_lst[6]:
        report = ("It is {cnd} and {deg} degrees right now in {loc} with winds"
                  " of {wnd} miles per hour. Visibility is {vis} with the "
                  "range of {rng} miles. {pre}".format(
                      cnd=weather_lst[0], deg=weather_lst[2],
                      loc=weather_lst[1], wnd=weather_lst[5],
                      vis=weather_lst[7], rng=weather_lst[8],
                      pre=weather_lst[9]))
    else:
        report = ("It is {cnd} and {deg} degrees right now in {loc} with winds"
                  "of {wnd} miles per hour. So it feels like {flk} degrees "
                  "outside. Visibility is {vis} with the range of {rng} miles."
                  " {pre}".format(
                      cnd=weather_lst[0], deg=weather_lst[2],
                      loc=weather_lst[1], wnd=weather_lst[5],
                      flk=weather_lst[6], vis=weather_lst[7],
                      rng=weather_lst[8], pre=weather_lst[9]))
    return report


def short_summary(weather_lst):
    """Generate a short summary of the weather.

    :param weather_lst
    :return: string
    """
    if weather_lst[2] == weather_lst[6]:
        report = ("It is {cnd} and {deg} degrees right now in {loc} with winds"
                  " of {wnd} miles per hour.".format(
                      cnd=weather_lst[0], deg=weather_lst[2],
                      loc=weather_lst[1], wnd=weather_lst[5]))
    return report


def generate_report(report_length, api_key):
    """Generate the weather report based on the parameter.

    :param report_length:
    :return: string
    """
    weather_data_lst = weather_info(api_key)
    if report_length == "fullReport":
        return full_summary(weather_data_lst)
    elif report_length == "shortReport":
        return short_summary(weather_data_lst)
    else:
        return "Invalid Argument"


if __name__ == '__main__':
    API_KEY = raw_input("Please enter your wunderground api key:")
    if len(sys.argv) != 2:
        print("{} of 2 Argument(s) found. Please enter 'fullReport' or "
              "'shortReport' as argument.".format(sys.argv))
    else:
        print generate_report(sys.argv[1], API_KEY)
