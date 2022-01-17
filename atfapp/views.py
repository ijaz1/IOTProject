from email.mime import image
from importlib.resources import path
from django.http import response
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from atfapp.models import Transaction, UserDetails
from datetime import date
from . models import *
from django.views.decorators.csrf import csrf_exempt
import imagehash
from PIL import Image



# vending machine function
@csrf_exempt
def CheckExist(request):
    if request.method=='POST':

        # getting fingerprint and image

        res_fingerprint=request.FILES['fingerprint']
        photo=request.FILES['photo']
        hash_fingerprint=imagehash.average_hash(Image.open(res_fingerprint)) 
        print('hashed fingerprint',hash_fingerprint)
        existing_fingerprints_in_user=UserDetails.objects.all()
        existing_fingerprints_in_transaction=Transaction.objects.all()
        for user_tb_finger in existing_fingerprints_in_user:
            hash_user_tb_finger=imagehash.average_hash(Image.open(user_tb_finger.fingerprint))
            if hash_fingerprint==hash_user_tb_finger:
                print('**old user**')
                print('old user tb finger path',user_tb_finger.fingerprint)
                for trans_tb_finger in existing_fingerprints_in_transaction:
                    hash_trans_finger=imagehash.average_hash(Image.open(trans_tb_finger.fingerprint))
                    if hash_fingerprint==hash_trans_finger:
                        print('**confirmed user**')
                        print('old trans tb finger path',trans_tb_finger.fingerprint)
                        get_row=Transaction.objects.get(fingerprint=trans_tb_finger.fingerprint)
                        print(get_row.id)
                        if get_row.status<3:
                            Transaction.objects.filter(id=get_row.id).update(CurrentDate=date.today(),status=get_row.status+1)
                            return JsonResponse({'Access':'Allowed'})
                        elif get_row.status==3:
                            todayDate=date.today()
                            d0 = get_row.CurrentDate
                            d1 = todayDate
                            delta = d1 - d0
                            if delta.days>30:
                                Transaction.objects.filter(id=get_row.id).update(status=1)
                                return JsonResponse({'Access':'Allowed'})
                            else:
                                return JsonResponse({'Access':'Denied'})


        for user_tb_finger_new in existing_fingerprints_in_user:
            hash_user_tb_finger_new=imagehash.average_hash(Image.open(user_tb_finger_new.fingerprint))
            if hash_fingerprint!=hash_user_tb_finger_new:
                print("**New user**")
                UserDetails(fingerprint=res_fingerprint,photo=photo).save()
                Transaction(fingerprint=res_fingerprint,photo=photo,CurrentDate=date.today(),status=1).save()
                return JsonResponse({'Access':'Allowed'})

    else:
        return HttpResponse("Need post request")
























            
        #     for finger in existing_fingers:
        #         exisitng_finger=imagehash.average_hash(Image.open(finger.fingerprint))
        #         if received_finger==exisitng_finger:
        #             print('user tb matched finger',exisitng_finger)
        #             print('user tb matched finger path',finger.fingerprint)
        #             for finger_2nd_table in existing_finger_in_2nd_tb:
        #                 exist_finger_2nd=imagehash.average_hash(Image.open(finger_2nd_table.fingerprint))
        #                 if received_finger==exist_finger_2nd:
        #                     print('transaction td matched finger',exist_finger_2nd)
        #                     print("**old user**")
        #                     print('transaction tb matched finger path',finger_2nd_table.fingerprint)
        #                     Checkphoto=Transaction.objects.get(fingerprint=finger_2nd_table.fingerprint)
        #                     print('transaction tb row get',Checkphoto)
        #                     if Checkphoto.status<3:
        #                         Transaction.objects.filter(id=Checkphoto.id).update(CurrentDate=date.today(),status=Checkphoto.status+1)
        #                         return JsonResponse({'Access':'Allowed'})
        #                     elif Checkphoto.status==3:
        #                     # check the date diffrence between last accessed date and current date
        #                         todayDate=date.today()
        #                         d0 = Checkphoto.CurrentDate
        #                         d1 = todayDate
        #                         delta = d1 - d0
        #                     # if date diffrence is graterthan 30 days
        #                         if delta.days>30:
        #                             # update the status as 1 in transaction table
        #                             Transaction.objects.filter(id=Checkphoto.id).update(status=1)
        #                             # give true output to the raspberry pi 
        #                             return JsonResponse({'Access':'Allowed'})
        #                         # if date diffrence is lessthan 30 
        #                         else:
        #                             # give false output to the raspberry pi
        #                             return JsonResponse({'Access':'Denied'})
                
        #         else:
        #             print("**New user**")
        #             # save fingerprint and image into the usertable
        #             UserDetails(fingerprint=fingerprints,photo=photo).save()
        #             # and also saving to the Transaction table with current date and store status value as 1
        #             Transaction(fingerprint=fingerprints,photo=photo,CurrentDate=date.today(),status=1).save()
        #             # give true output to the raspberry pi
        #             return JsonResponse({'Access':'Allowed'})

        # except Exception as e:print(e)




