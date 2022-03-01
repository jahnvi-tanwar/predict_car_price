import re
from django.http import HttpResponse
from django.shortcuts import render
import joblib
from datetime import date

def home(request):
    return render(request,"home.html")

def answer(request,list,ans):
    return render(request,"answer.html",{"list":list, "ans":ans})

def result(request):

    if request.method == 'POST':
        
        model = joblib.load('random_forest_regression_model.sav')

        curr_year = date.today().year

        param = []

        param.append(int(request.POST['showroom-price']))
        param.append(int(request.POST['mileage']))
        param.append(int(request.POST['prev-owners']))
        param.append(curr_year-int(request.POST['year']))
        
        fuel = request.POST['fuel']

        if(fuel=='petrol'):
            param.append(0)
            param.append(1)
        elif fuel=='diesel':
            param.append(1)   
            param.append(0) 
        else:
            param.append(0)
            param.append(0)
        

        seller = request.POST['seller-type']

        if(seller=='Dealer'):
            param.append(0)
        else :
            param.append(1)

        trans = request.POST['transmission']

        if trans=='Manual':
            param.append(1)
        else:
            param.append(0)

        ans = model.predict([param])

        return answer(request,param,ans)

    return render(request,"form.html")
