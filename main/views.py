from django.shortcuts import render, redirect
from random import *
from .models import *
from django.db import connection
from django.urls import reverse
from django.db.models import Q # Q는 Django내 Model을 관리할 때 사용되는 ORM으로 SQL의 WHERE절과 같은 조건문을 추가할 때 사용한다.
from .forms import *
from datetime import datetime
from django.http import HttpResponse, JsonResponse

#from google.protobuf import descriptor as _descriptor

from PIL import Image
import tensorflow as tf
import os,glob
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input

from django.core.files.uploadedfile import InMemoryUploadedFile

import main.visualization as visual #시각화 데이터 함수

def home(request):
    items = Item.objects.all().order_by('-pk') 
    context = visual.data_visualization()

    user_name = request.session.get('user_name')
    if user_name:
        user = user_name
        context['user'] = user
        context['items'] = items
        return render(request, 'home.html', context)
    else:
        context['nonuser'] = 'nonuser'
        context['items'] = items
        return render(request, 'home.html', context)

def signup(request):
    context = dict()
    context['nonuser'] = 'nonuser'
    return render(request, 'signup.html', context)

def join(request):
    
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    pw_check = request.POST['signupPWcheck']
    gender = request.POST['signupGender']
    age = request.POST['signupAge']

    items = Item.objects.all().order_by('-pk') 
    context = visual.data_visualization()
    context['items'] = items

    if pw==pw_check:
        user = Users(user_name = name, user_email = email, user_password = pw, user_gender = gender, user_age = age)
        user.save()

        return render(request, 'home.html', context)

    else:
        return render(request, 'signup.html')

def signin(request):
    context = dict()
    context['nonuser'] = 'nonuser'
    return render(request, 'signin.html', context)

def login(request):
    loginEmail = request.POST['loginEmail'] # signin.html <input name=loginEmail> 사용을 위해
    loginPW = request.POST['loginPW']  # signin.html <input name=loginPW> 사용을 위해
    user = Users.objects.get(user_email = loginEmail)

    if user.user_password == loginPW:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        
        return redirect('home')
    else:
        return redirect('signin')  


def logout(request):
    if request.session.get('user_name'):
        del request.session['user_name']
        del request.session['user_email']

    context = dict()
    context['nonuser'] = 'nonuser'

    return render(request,'signin.html', context)


def upload(request):
    return render(request, 'upload.html')

#가격예측버튼 누르면 실행되는 함수
#epoch100.h5는 모델 파일(git 업로드x)

UPLOAD_DIR = r'C:\projects\albo\media\images'
def predict_price(request):
    #predict_img = request.POST['predict_img']

    if 'file1' in request.FILES:
        file = request.FILES['file1']
        file_name = file.name
        fp = open("%s%s" % (UPLOAD_DIR, file_name), 'wb')

    for chunk in file.chunks():
        fp.write(chunk)
        fp.close()

    model_weight_path = r'C:\projects\albo\epoch100.h5'
    img = Image.open("%s%s"%(UPLOAD_DIR,file_name))


    #가격예측함수
    def predict(model_path, img):
        
        model_saved = load_model(model_path)

        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)

        prediction = model_saved.predict(img)
        label = np.argmax(prediction[0])

        if label == 0:
            return '10만원 이상 45만원 미만'
        elif label == 1:
            return '45만원 이하 80만원 미만'
        else:
            return '80만원 이상 160만원 미만'

    
    
    context = dict()
    context['predict'] = predict(model_weight_path, img)

    return render(request, 'upload.html', context) 


def posting(request):
    
    #items = Item.objects.all().order_by('-pk') 
    if request.FILES.get('item_img'):
        users = Users.objects.get(user_name=request.session['user_name']) #fk추가

        item_name = request.POST.get('item_name',False)
        item_price =request.POST.get('item_price',False)
        item_content = request.POST.get('item_content',False)
        item_img= request.FILES.get('item_img')
        now_HMS = datetime.today().strftime('%Y.%H.%M.%S')
        item_upload_name  = now_HMS + '.jpeg'
        item_img.name = item_upload_name  


        new_name = Item(item_name=item_name, item_price=item_price, 
                        item_content=item_content, item_img = item_img, 
                        user_name= users)
        new_name.save()



    items = Item.objects.all().order_by('-pk') 
    context = visual.data_visualization()
    context['items'] = items

    return render(request, 'home.html', context) 

def new_post(request, pk):
    items = Item.objects.get(pk=pk)
    context = dict()

    #로그인 유무 확인
    user_name = request.session.get('user_name')
    if user_name:
    	login_user = user_name
    else:
        login_user = 'non-member'
        context['nonuser'] = 'nonuser'

    post_user = str(items.user_name)

    comments = CommentForm() #forms.py

    context['items'] = items
    context['comments'] = comments
    context['login_user'] = str(login_user)
    context['post_user'] =  str(post_user)
    context['trade_status'] = items.trade_status

                                 
    return render(request, 'new_post.html', context)



def remove_post(request, pk):
    post = Item.objects.get(pk=pk)
  
    post.delete()

    items = Item.objects.all().order_by('-pk') 
    context = visual.data_visualization()
    context['items'] = items

        
    return render(request, 'home.html', context)
    


def boardEdit(request, pk):
  
    items = Item.objects.get(pk=pk)
   
     
    if request.method == "POST":
       
        items.item_name = request.POST.get('item_name')
        items.item_content = request.POST.get('item_content')
        items.item_price = request.POST.get('item_price')
        items.trade_status =request.POST.get('trade_status')

        
        items.save()

        items = Item.objects.get(pk=pk)
        users = Users.objects.get(pk=pk)
     
        if items.trade_status == "거래완료" :
            
            #image의 파일 형태가 PIL 형태
            image = items.item_img
            

            # PIL 파일 또는 경로는 save할수 없기 때문에 InMemoryUploadedFile 함수를 이용하여 request해온
            # 이미지 파일 형식과 동일하게 맞춰줘야한다.(불러올 이미지, 새로 저장할 이미지 이름, 저장할 이미지 경로)
            heat_file = InMemoryUploadedFile(image, None, 'heat.jpeg', 'trade_images/jpeg',
                                     None, None)
            
            item_price = items.item_price
            user_gender = users.user_gender
            user_age = users.user_age

            status = Trade(item_img=heat_file ,item_price=item_price, 
                           user_gender=user_gender, user_age = user_age)
            status.save()
        

    items = Item.objects.all().order_by('-pk') 
    context = visual.data_visualization()
    context['items'] = items

    return render(request, 'home.html', context)


def create_comment(request, items_id):
    user_name = request.session.get('user_name')
    if user_name:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data['comment']
            parent=None
            

        user = Users.objects.get(user_name=request.session['user_name'])
        items = Item.objects.get(pk=items_id)
        

        new_comment = Comment(comment=comment, user_name=user, item_id=items, parent=parent)
        new_comment.save()
        return redirect('new_post', items_id)
    else:
        return JsonResponse({"message":"please, login"}, status=401) 

    
def create_reply(request, items_id):
    reply_form = ReplyForm(request.POST) 
    user_name = request.session.get('user_name')
    if user_name:
        if reply_form.is_valid():
            parent = reply_form.cleaned_data['parent']
            reply = reply_form.cleaned_data['comment']
            

        user = Users.objects.get(user_name=request.session['user_name'])
        items = Item.objects.get(pk=items_id)

        new_comment = Comment(comment=reply, user_name=user, item_id=items, parent=parent)
        new_comment.save()

        return redirect('new_post', items_id)
    else:
        return JsonResponse({"message":"please, login"}, status=401) 


def trade(request, item_id):
    filled_form = Trade(request.POST) #POST 요청이 들어오면,
    if filled_form.is_valid(): #유효성 검사 성공시 진행
        
        temp_form = filled_form.save(commit=False)
        
        temp_form.item_id = Item.objects.get(id=item_id)
        temp_form.user_name = Users.objects.get(user_name=request.session['user_name'])
        temp_form.item_status = "거래상태"
        temp_form.save()
    return redirect('posting', {'trade':trade})

def css(request):
    return render(request, 'main/css.html')