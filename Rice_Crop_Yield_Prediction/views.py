import matplotlib.pyplot as plt
import seaborn as sb
from django.http import HttpResponse
from django.shortcuts import render
import joblib
import json
import requests
import pandas as pd
import numpy as np
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Scatter



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
    parameter=['temperature','precipitation','humidity','area','AHMEDNAGAR','AKOLA','AMRAVATI','AURANGABAD','BEED','BHANDARA','BULDHANA','CHANDRAPUR','DHULE','GADCHIROLI','GONDIA','HINGOLI','JALGAON','JALNA','KOLHAPUR','LATUR','NAGPUR','NANDED','NANDURBAR','NASHIK','OSMANABAD','PALGHAR','PARBHANI','PUNE','RAIGAD','RATNAGIRI','SANGLI','SATARA','SINDHUDURG','SOLAPUR','THANE','WARDHA','WASHIM','YAVATMAL']
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
        vect['precipitation'] = preci
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

def pairplot(data):
    pairplot_chart=sb.pairplot(data,hue='humidity')
    pairplot_chart.savefig("./static/graphs/pairplot.png")
    pairplot_chart.figure.clf()

def heatmap(data):    
    out=data.corr()
    heatmap=sb.heatmap(out,cmap='coolwarm',annot=True)
    heatmap.figure.savefig("./static/graphs/heatmap.png")
    heatmap.figure.clf()

def regplot(data):
    lregplot=sb.regplot(data.area,data.production,robust=True)
    lregplot.figure.savefig("./static/graphs/lregplot.png") 
    lregplot.figure.clf()

@login_required(login_url="admin/login/?next=/dashboard")
def dashboard(request):
    #importing the data and selecting the row
    data=pd.read_csv('./static/misc/rice.csv')

    #drop column that are not important
    cols_to_drop=['state_name','crop_year','season','crop']
    data=data.drop(cols_to_drop,axis=1)

    data.production=data.production.fillna(0)

    pairplot(data)
    heatmap(data)
    regplot(data)

    # #pairplot graph
    # pairplot_chart=sb.pairplot(data,hue='humidity')
    # pairplot_chart.savefig("./static/graphs/pairplot.png")

    #heatmap graph
    # out=data.corr()
    # heatmap=sb.heatmap(out,cmap='coolwarm',annot=True)
    # heatmap.figure.savefig("./static/graphs/heatmap.png")

    #regplot
    # lregplot=sb.regplot(data.area,data.production,robust=True)
    # lregplot.figure.savefig("./static/graphs/lregplot.png")

    return render(request,"dashboard.html")

@login_required(login_url="/")
def logout(request):
    logout(request)
    return HttpResponseRedirect('index')