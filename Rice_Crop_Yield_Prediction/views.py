from django.http import HttpResponse
from django.shortcuts import render
import joblib
import json
import requests
import pandas as pd
# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
# STATIC_DIR=BASE_DIR.joinpath('static')


def index(request):
    return render(request,"index.html")

def predict(request):

    #import model
    model=joblib.load("./static/misc/model")

    #input district and area values
    # district=input("Enter district name: ")
    # ar=input("Enter area: ")
    district=request.GET.get('district')
    ar=request.GET.get('area')

    #weather data import
    try:
        weather='http://api.weatherapi.com/v1/current.json?key=797939893d564e7cbbf130055210910&q='+district
        r = requests.get(weather)
        response = r.json()
        temp=response['current']['temp_c']
        preci=response['current']['precip_mm']
        humi=response['current']['humidity']
    except:
        district='pune'
        temp=0
        preci=0
        humi=0

    #creating data input array
    parameter=['temperature','precipitaion','humidity','area','AHMEDNAGAR','AKOLA','AMRAVATI','AURANGABAD','BEED','BHANDARA','BULDHANA','CHANDRAPUR','DHULE','GADCHIROLI','GONDIA','HINGOLI','JALGAON','JALNA','KOLHAPUR','LATUR','NAGPUR','NANDED','NANDURBAR','NASHIK','OSMANABAD','PALGHAR','PARBHANI','PUNE','RAIGAD','RATNAGIRI','SANGLI','SATARA','SINDHUDURG','SOLAPUR','THANE','WARDHA','WASHIM','YAVATMAL']
    index_dict=dict(zip(parameter,range(len(parameter))))
    vect={}
    for key, val in index_dict.items():
        vect[key]=0

    #enter user input to the array
    try:
        district=district.upper()
        vect[district] = 1
    except Exception as e:
        print("Exception occered for DISTRICT!", e)    
    try:
        vect['area'] = ar
    except Exception as e:
        print("Exception occered for AREA!", e)
    try:
        vect['temperature'] = temp
    except Exception as e:
        print("Exception occered for TEMPERATURE!", e)
    try:
        vect['precipitaion'] = preci
    except Exception as e:
        print("Exception occered for PRECIPITATION!", e)
    try:
        vect['humidity'] = humi
    except Exception as e:
        print("Exception occered for HUMIDITY!", e)
    df = pd.DataFrame.from_records(vect, index=[0])
    prediction=model.predict((df))
    # print ("The yield prediction for rice crop is {} tons".format(prediction[0]))
    return HttpResponse(prediction[0])