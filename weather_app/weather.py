import requests


def request(api_key, location_key):
    language = 'ru-RU'

    url_cur = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}'
    data = {
        'apikey': api_key,
        'lanquage': language,
        'details': 'true'
    }

    response_current_weather = requests.get(url_cur, params=data)
    current_response = response_current_weather.json()[0]
    if response_current_weather.status_code != 200:
        print("ошибка:", response_current_weather.status_code)

    url_forc = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}'
    data = {
        'apikey': api_key,
        'lanquage': language,
        'details': 'true',
        'metric': 'true'
    }
    response_forecast_weather = requests.get(url_forc, params=data)

    forecast_response = response_forecast_weather.json()[0]

    if response_forecast_weather.status_code != 200:
        print("ошибка:", response_forecast_weather.status_code)

    return get_weather_by_data(current_response, forecast_response)


def get_weather_by_data(data1, data2):
    temperature_celsius = data1['Temperature']['Metric']['Value']
    humidity = data1['RelativeHumidity']
    wind_speed_kph = data1['Wind']['Speed']['Metric']['Value']
    rain_probability = data2['PrecipitationProbability']

    # Создаем словарь с нужными параметрами
    weather_data = {
        'temperature': temperature_celsius,
        'humidity': humidity,
        'wind_speed': wind_speed_kph,
        'rain_probability': rain_probability
    }

    return weather_data


def get_location_key_by_coors(coordinates, apikey, language="ru-RU"):

    url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
    data = {
        'apikey': apikey,
        'q': ','.join(list(map(str, list(coordinates)))),
        'lanquage': language
    }

    try:
        response = requests.get(url, params=data)
        data = response.json()
        return data["Key"]
    except KeyError:
        raise KeyError('Возможно, допущена ошибка при введении координат или произошла'
                       ' ошибка на стороне API AccuWeather, проверьте лимит запросов')
    except TypeError:
        raise TypeError('Скорее всего произошла ошибка на стороне API AccuWeather, проверьте лимит запросов')
    except IndexError:
        raise IndexError('Скорее всего произошла ошибка на стороне API AccuWeather, проверьте лимит запросов')


def get_location_key_by_name(api_key, name, lanquage='ru-RU'):

    url = 'http://dataservice.accuweather.com/locations/v1/cities/search'
    data = {
        'apikey': api_key,
        'q': name,
        'lanquage': lanquage,
        'alias': 'Always'
    }

    try:
        response = requests.get(url, params=data)
        data = response.json()

        return data[0]['Key']
    except KeyError:
        raise KeyError('Такого города нет или произошла ошибка на стороне API AccuWeather, проверьте лимит запросов')
    except TypeError:
        raise TypeError('Скорее всего произошла ошибка на стороне API AccuWeather, проверьте лимит запросов')
    except IndexError:
        raise IndexError('Скорее всего произошла ошибка на стороне API AccuWeather, проверьте лимит запросов')


def check_bad_weather(data_conditions):
    bad_request = "Условия не являются благоприятными, выходить на улицу не стоит"
    good_request = "Условия крайне хорошие, на улице классная погода"

    temprature = data_conditions['temperature']
    rain_prob = data_conditions['rain_probability']
    wind_speed = data_conditions["wind_speed"]

    if temprature < -10 or temprature > 30:
        return bad_request
    elif rain_prob > 75:
        return bad_request
    elif wind_speed > 50:
        return bad_request
    else:
        return good_request



