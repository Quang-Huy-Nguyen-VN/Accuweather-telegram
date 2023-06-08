from django.shortcuts import render, redirect
from .models import Project, Topic
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import ProjectForm
from django.http import HttpResponse
import json
import urllib.request
import urllib.parse

# Create your views here.

#projects = [
#    {'id':1, 'name':'Topic 1 '},
#    {'id':2, 'name':'Topic 2 '},
#    {'id':3, 'name':'Topic 3 '},
#]

################################# LOGIN ##############################################
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)

################################# LOGOUT ##############################################
def logoutUser(request):
    logout(request)
    return redirect('home')

################################# HOME PAGE ##############################################
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    projects = Project.objects.filter(topic__name__icontains=q)
   
    topics = Topic.objects.all()

    ###### Phu Ly Weather ######

    source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?id=1570449&lang=vi&appid=6599a7ee10534ac937d4a6ce1e8f73a3').read()

    list_of_data = json.loads(source)

    data = {
        "name": str(list_of_data['name']),
        "country_code": str(list_of_data['sys']['country']),
        "timezone": str(list_of_data['timezone']),
        "coordinate": str(list_of_data['coord']['lon']) + 'N' + ' - ' + str(list_of_data['coord']['lat']) + 'B',
        "temp": str(round(list_of_data['main']['temp'] - 273.15, 2)) + '°C',
        "pressure": str(list_of_data['main']['pressure']) + ' hPa',
        "feels_like": str(round(list_of_data['main']['feels_like'] - 273.15)) + '°C',
        "temp_min": str(round(list_of_data['main']['temp_min'] - 273.15)) + '°C',
        "temp_max": str(round(list_of_data['main']['temp_max'] - 273.15)) + '°C',
        "humidity": str(list_of_data['main']['humidity']) + '%',
        # "weather" : str(list_of_data['weather']),
        "weather_description": str(list_of_data['weather'][0]['description']),
        "icon": str(list_of_data['weather'][0]['icon']),
    }

    context = {'projects': projects, 'topics': topics, 'data': data}
    return render(request, 'base/home.html', context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    context = {'project': project}
    return render(request, 'base/project.html', context)

################################# CREATE PROJECT ##############################################
@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'base/project_form.html', context)

################################# UPDATE PROJECT ##############################################
@login_required(login_url='login')
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    topics = Topic.objects.all()

    if request.user != project.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic = Topic.objects.get_or_create(name=topic_name)
        project.name = request.POST.get('name')
        project.topic = topic
        project.description = request.POST.get('description')
        project.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'project': project}
    return render(request, 'base/project_form.html', context)

################################# DELETE PROJECT ##############################################
@login_required(login_url='login')
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)

    if request.user != project.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        project.delete()
        return redirect('/')
    
    return render(request, 'base/delete.html', {'obj': project})

################################# SEARCH WEATHER ##############################################
def index1(request):
    if request.method == 'POST':
        city = request.POST['city']

        source1 = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&lang=vi&appid=6599a7ee10534ac937d4a6ce1e8f73a3').read()

        list_of_data1 = json.loads(source1)

        data1 = {
            "name": str(list_of_data1['name']),
            "country_code": str(list_of_data1['sys']['country']),
            "timezone": str(list_of_data1['timezone']),
            "coordinate": str(list_of_data1['coord']['lon']) + ' ' + str(list_of_data1['coord']['lat']),
            "temp": str(round(list_of_data1['main']['temp'] - 273.15)) + '°C',
            "pressure": str(list_of_data1['main']['pressure']) + ' hPa',
            "feels_like": str(round(list_of_data1['main']['feels_like'] - 273.15)) + '°C',
            "temp_min": str(round(list_of_data1['main']['temp_min'] - 273.15)) + '°C',
            "temp_max": str(round(list_of_data1['main']['temp_max'] - 273.15)) + '°C',
            "humidity": str(list_of_data1['main']['humidity']) + '%',
            "weather_description": str(list_of_data1['weather'][0]['description']),
            "icon": str(list_of_data1['weather'][0]['icon']),
        }
        print(data1)
    else:
        data1 = {}
    return render(request, "base/index1.html", data1)


################################# WEATHER ##############################################
huyen = [
    {'id':2, 'name':'Phủ Lý', 'lat':'20.5411', 'lon':'105.9139', 'telegram_id': '-819622414'},
    {'id':3, 'name':'Bình Lục', 'lat':'20.48944', 'lon':'106.00917', 'telegram_id': '-819622414'},
    {'id':4, 'name':'Duy Tiên', 'lat':'20.625808', 'lon':'105.963256', 'telegram_id': '-819622414'},
    {'id':5, 'name':'Lý Nhân', 'lat':'20.585867', 'lon':'106.073996', 'telegram_id': '-819622414'},
    {'id':6, 'name':'Kim Bảng', 'lat':'20.581667', 'lon':'105.873333', 'telegram_id': '-819622414'},
    {'id':7, 'name':'Thanh Liêm', 'lat':'20.54389', 'lon':'105.9119', 'telegram_id': '-819622414'},
    ]


def index(request): 
    data = []
    for item in huyen : 
        id = item['id']
        name = item['name']
        coordinate = (item['lat'], item['lon'], item['name'])

        data.append(fetch(request,coordinate))
        
    dict = {"data": data}
    return render(request, "base/index.html", dict)

def fetch(request, coordinate):
    source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?lat=' + coordinate[0] + '&lon=' + coordinate[1] + '&lang=vi&appid=6599a7ee10534ac937d4a6ce1e8f73a3').read()

    list_of_data3 = json.loads(source)

    return {
            "name": str(coordinate[2]),
            "country_code": str(list_of_data3['sys']['country']),
            "timezone": str(list_of_data3['timezone']),
            "coordinate": str(list_of_data3['coord']['lon']) + 'N' + ' - ' + str(list_of_data3['coord']['lat']) + 'B',
            "temp": str(round(list_of_data3['main']['temp'] - 273.15)) + '°C',
            "pressure": str(list_of_data3['main']['pressure']) + ' hPa',
            "feels_like": str(round(list_of_data3['main']['feels_like'] - 273.15)) + '°C',
            "temp_min": str(round(list_of_data3['main']['temp_min'] - 273.15)) + '°C',
            "temp_max": str(round(list_of_data3['main']['temp_max'] - 273.15)) + '°C',
            "humidity": str(list_of_data3['main']['humidity']) + '%',
            #"weather" : str(list_of_data['weather']),
            "weather_description" : str(list_of_data3['weather'][0]['description']),
            "icon": str(list_of_data3['weather'][0]['icon']),
        }