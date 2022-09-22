from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import  HttpResponse
from apod.forms import UserForm
from django.conf import settings
import requests
import json
import urllib.request

# Create your views here.

api_key = ""; # paste your api key here.

url ="https://api.nasa.gov/planetary/apod?api_key="+api_key

def index(request):
    response = requests.get(url)
    api = json.loads(response.text)
    image_video_url = api.get('url')
    title = api.get('title')
    explanation = api.get('explanation')
    date = api.get('date')
    copyright = api.get('copyright')
    media_type= api.get('media_type')

    data = {
        'image_video_url': image_video_url,
        'title':title,
        'explanation':explanation,
        'date':date,
        'copyright':copyright,
        'media_type':media_type
    }

    return render(request,"apod/index.html", data)


def earth_image(request):
    
    epic = "https://api.nasa.gov/EPIC/api/natural?api_key="+api_key 

    response = requests.get(epic)
    api = json.loads(response.text)
    print(epic)
    date_with_time = api[0]['date']
    print(date_with_time)
    year = date_with_time[0:4]
    month = date_with_time[5:7]
    date = date_with_time[8:10]
    time = date_with_time[11:]

    whole_data=[]

    for i in api:
        image_id = i['image']
        date_and_time = i['date']
        image_url = "https://epic.gsfc.nasa.gov/archive/natural/"+ year +"/"+ month+ "/"+ date +"/jpg/"+ image_id +".jpg"
        data = {
            'image_url':image_url,
            'image_id':image_id,
            'date_and_time':date_and_time,
        }
        whole_data.append(data)
        
    
    whole_data[0]['image_id']=NULL

    return render(request,"apod/earth_images.html",{"whole_data":whole_data})



def mars(request):
    mars_data = []
    form = UserForm()
    value = UserForm(request.GET)

    if value.is_valid():
        whole_date = value.cleaned_data['date']
        
        date = whole_date.day
        month = whole_date.month
        year = whole_date.year
        # print(date,month, year)

        api="https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date="+str(year)+"-"+str(month)+"-"+str(date)+"&page=1&api_key="+api_key
        response = requests.get(api)
        loaded_json = json.loads(response.text)
        # print(loaded_json)
        # print(api)
        for i in loaded_json['photos']:
            image = i["img_src"]
            id = i['id']
            earth_date = i['earth_date']
            data = {
                'image': image,
                'id':id,
                'earth_date':earth_date
            }
            # print(image)
            mars_data.append(data)
        if len(mars_data)>0:
            mars_data[0]['id']=NULL
            return render(request,"apod/mars_images.html",{"mars_data":mars_data})
        else:
            return render(request,"apod/mars_error.html")


    return render(request, "apod/mars.html",{"form":form})


