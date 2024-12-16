from django.shortcuts import render
import requests
from .models import City

# Create your views here.
from django.http import HttpResponse
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=32139ba8be0ceec44d3a35984cf1d944'

    cities = City.objects.all() #return all the cities in the database
    
    if request.method == 'POST':  # Only true if form is submitted
        form = CityForm(request.POST)  # Add actual request data to form for processing
        if form.is_valid():  # Check if form data is valid
            form.save()  # Save the form data to the database

    # if request.method == 'POST': # only true if form is submitted
    #     form = CityForm(request.POST) # add actual request data to form for processing
    #     form.save() # will validate and save if validate

    form = CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()  # Request API data

        #Add a check for the API response status (city_weather['cod'] == 200) to ensure the city is valid and the API call is successful. If not, skip that city.
        if city_weather.get('cod') != 200:  # Skip if the city is not found or there's an error
            continue
    
        weather = {
            'city': city.name,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
        }
        weather_data.append(weather)  # Add the data for the current city to the list


    # for city in cities:

    #     city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

    #     weather = {
    #         'city' : city,
    #         'temperature' : city_weather['main']['temp'],
    #         'description' : city_weather['weather'][0]['description'],
    #         'icon' : city_weather['weather'][0]['icon']
    #     }

    #     weather_data.append(weather) #add the data for the current city into our list

    
    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'details/index.html',context)

