import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):

    API_KEY = '622707fcbf18c29ba748d73c0bd634c0'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=' + API_KEY + '&lang=sp'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "Ciudad no encontrada"
            else:
                err_msg = "Ciudad ya existe"

        if err_msg:
            message = err_msg
            message_class = "is-danger"
        else:
            message = "Ciudad agregada con exito"
            message_class = "is-success"

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
 
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': round(r['main']['temp'], 1),
            'feels_like': round(r['main']['feels_like'], 1),
            'description': r['weather'][0]['description'].capitalize(),
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data,
               'form': form,
               'message': message,
               'message_class': message_class}

    return render(request, 'index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')
