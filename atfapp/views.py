from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render

from atfapp.models import Transaction, UserDetails
from datetime import date,timedelta
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework .parsers import JSONParser
# from .serializers import UserDetailsSerializer,TransactionSerializer
# from django.http.response import JsonResponse
from . models import *
from django.views.decorators.csrf import csrf_exempt





def test_call(request):
    location = request.GET.get("address")
    print(location)
    return  HttpResponse("Hello")
# Create your views here.



@csrf_exempt
def food(request):
    if request.method == 'POST':
        
        fingerprint = request.POST.get('fingerprint')
        print(fingerprint)
        img = request.FILES['photo']
        print(img.name)


    return HttpResponse('food')

def ph(request):
    if request.method=='POST':
        photo=request.POSt.get('photo')
        print(photo)




# vending machine function
@csrf_exempt
def CheckExist(request):
    if request.method=='POST':
        try:
            # getting fingerprint and image unique values
            fingerprint=request.POST.get('fingerprint')
            print(fingerprint)
            photo=request.FILES['photo']
            # ph=request.POST.get('ph')
            print(photo.name)
            # checking if fingerprint is exists or not 
            CheckFinger=UserDetails.objects.filter(fingerprint=fingerprint).exists()
            # if fingerprint doesn't exists 
            if CheckFinger==False:
                # save fingerprint and image into the usertable
                UserDetails(fingerprint=fingerprint,photo=photo).save()
                # and also saving to the Transaction table with current date and store status value as 1
                Transaction(fingerprint=fingerprint,photo=photo,CurrentDate=date.today(),status=1).save()
                # give true output to the raspberry pi
                return JsonResponse({'Access':'Allowed'})
            # if fingerprint exists 
            else:
                # check the image 
                Checkphoto=Transaction.objects.get(fingerprint=fingerprint,photo=photo)
                print(Checkphoto.id)
                # if image match equal to true
                
                # then check if status is lessthan 3 
                if Checkphoto.status<3:
                    # update the values of current date and status in transaction table
                    Transaction.objects.filter(id=Checkphoto.id).update(CurrentDate=date.today(),status=Checkphoto.status+1)
                    # give true output to raspberry pi
                    return JsonResponse({'Access':'Allowed'})
                # if status become as 3 in tarascation table
                elif Checkphoto.status==3:
                    # check the date diffrence between last accessed date and current date
                    todayDate=date.today()
                    d0 = Checkphoto.CurrentDate
                    d1 = todayDate
                    delta = d1 - d0
                    # if date diffrence is graterthan 30 days
                    if delta.days>30:
                        # update the status as 1 in transaction table
                        Transaction.objects.filter(id=Checkphoto.id).update(status=1)
                        # give true output to the raspberry pi 
                        return JsonResponse({'Access':'Allowed'})
                    # if date diffrence is lessthan 30 
                    else:
                        # give false output to the raspberry pi
                        return JsonResponse({'Access':'Denied'})
        except Exception as e:print(e)
   
# Checkphoto.CurrentDate

