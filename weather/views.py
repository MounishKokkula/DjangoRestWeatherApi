from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.template import loader


def homepage(request):
    return HttpResponse("Weather Homepage ")


def weather_error(request):
    template = loader.get_template('weather/UrlError.html')
    context = {}
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Weather report App. Please check the Url and try again.")


def weather_report(request, weather_station, lat, long):
    try:
        filter_input = str(weather_station).split("-")
        filter_output = {}
        lat_long = [lat, long]
        avg_temp_f = []
        avg_temp_c = []

        if 'noaa' in filter_input:
            data = get_req('noaa', lat_long[0], lat_long[1]).json()
            avg_temp_f1 = round(float(data['today']['current']['fahrenheit']),2)
            avg_temp_c1 = round(float(data['today']['current']['celsius']),2)
            avg_temp_f.append(avg_temp_f1)
            avg_temp_c.append(avg_temp_c1)
            filter_output['noaa'] = [avg_temp_f1, avg_temp_c1]

        if 'accuweather' in filter_input:
            data = get_req('accuweather', lat_long[0], lat_long[1]).json()
            avg_temp_f2 = round(float(data['simpleforecast']['forecastday'][0]['current']['fahrenheit']),2)
            avg_temp_c2 = round(float(data['simpleforecast']['forecastday'][0]['current']['celsius']),2)
            avg_temp_f.append(avg_temp_f2)
            avg_temp_c.append(avg_temp_c2)
            filter_output['accuweather'] = [avg_temp_f2, avg_temp_c2]

        if 'weatherdotcom' in filter_input:
            data = post_req('weatherdotcom', lat_long[0], lat_long[1]).json()
            temp = data['query']['results']['channel']['condition']['temp']
            format = data['query']['results']['channel']['units']['temperature']
            temp_f = ''
            temp_c = ''
            if format == 'F':
                temp_f = temp
                temp_c = (float(temp) - 32) * 5.0 / 9.0

            elif format == 'C':
                temp_f = 9.0 / 5.0 * float(temp) + 32
                temp_c = temp

            avg_temp_f3 = round(float(temp_f), 2)
            avg_temp_c3 = round(float(temp_c), 2)
            avg_temp_f.append(avg_temp_f3)
            avg_temp_c.append(avg_temp_c3)
            filter_output['weatherdotcom'] = [avg_temp_f3, avg_temp_c3]

        avg_temp_f = round((sum(avg_temp_f) / len(filter_output.keys())), 2)
        avg_temp_c = round((sum(avg_temp_c) / len(filter_output.keys())), 2)

        template = loader.get_template('weather/index.html')
        context = {
            'filter_input': filter_output,
            'avg_temp_f': avg_temp_f,
            'avg_temp_c': avg_temp_c,
        }
        return HttpResponse(template.render(context, request))
        # return HttpResponse("Weather station report from " + "&".join(filter_input) + " \n Celsius: "+str(avg_temp_c)+'/ Fahrenheit: '+str(avg_temp_f))
    except:
        template = loader.get_template('weather/UrlError.html')
        context = {}
        return HttpResponse(template.render(context, request))

def get_req(provider, lat, long):
    """
    :param provider: Selected provider (accuweather/noaa)
    :param lat: Input latitude
    :param long: Input longitude
    :return: json response
    """
    url_ext = ''
    url = 'http://127.0.0.1:5000/'
    if provider == 'noaa':
        url_ext='noaa?latlon=' + lat + ',' + long
    elif provider == 'accuweather':
        url_ext='accuweather?latitude=' + lat + '&longitude=' + long
    print(url + url_ext)
    return requests.get(url + url_ext)


def post_req(provider,lat,long):
    """

    :param provider: Selected provider (weatherdotcom)
    :param lat: Input latitude
    :param long: Input longitude
    :return: json response
    """
    url_ext = ''
    url = 'http://127.0.0.1:5000/'
    if provider == 'weatherdotcom':
        url_ext = 'weatherdotcom'
    print(url + url_ext)
    return requests.post(url + url_ext, json={"lat":lat,"lon":long})


