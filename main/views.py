from django.shortcuts import render, redirect
from random import *
from .models import *
from django.db import connection
from django.urls import reverse
from django.db.models import Q # Q는 Django내 Model을 관리할 때 사용되는 ORM으로 SQL의 WHERE절과 같은 조건문을 추가할 때 사용한다.
from .forms import *
from datetime import datetime
from google.protobuf import descriptor as _descriptor

from PIL import Image
import tensorflow as tf
import os,glob
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
from django.core.files.uploadedfile import InMemoryUploadedFile




# 메인화면 데이터 시각화 start
def data_visualization():
    df_item = pd.DataFrame(list(Item.objects.all().values()))
    filt_1 = ((df_item['item_price'] >= 100000) & (df_item['item_price'] < 450000))
    filt_2 = ((df_item['item_price'] >= 450000) & (df_item['item_price'] < 800000))
    filt_3 = ((df_item['item_price'] >= 800000) & (df_item['item_price'] < 1600000))
    df_item_1 = df_item[filt_1]
    df_item_2 = df_item[filt_2]
    df_item_3 = df_item[filt_3]

    labels = ['10만원~45만원', '45만원~80만원', '80만원~160만원']
    values = [len(df_item_1['item_price']), len(df_item_2['item_price']),len(df_item_3['item_price'])]

    fig = go.Pie(labels=labels, values=values, hoverinfo='percent+label', insidetextorientation='radial', hole=.3)

    graphs2 = []
    graphs2.append(fig)

    layout_pie = {'title': '지금 이만큼이나 거래 중이에요 :0',
                    'height': 480,
                    'width': 1270,}
                    
    fig_div = plot({'data':graphs2, 'layout' : layout_pie}, output_type='div')
    

    df_trade = pd.DataFrame(list(Trade.objects.all().values()))
   
    Filt_1 = ((df_trade['item_price'] >= 100000) & (df_trade['item_price'] < 450000))
    Filt_2 = ((df_trade['item_price'] >= 450000) & (df_trade['item_price'] < 800000))
    Filt_3 = ((df_trade['item_price'] >= 800000) & (df_trade['item_price'] < 1600000))
    df_trade_1 = df_trade[Filt_1]
    df_trade_2 = df_trade[Filt_2]
    df_trade_3 = df_trade[Filt_3]
    x1 = df_trade_1['item_date']
    x2 = df_trade_2['item_date']
    x3 = df_trade_3['item_date']

    def get_counts(seq):
        counts={}
        for x in seq:
            if x in counts:
                counts[x] += 1
            else : 
                counts[x] = 1
        return counts

    count_1 = get_counts(x1)
    count_2 = get_counts(x2)
    count_3 = get_counts(x3)

    x1 = list(count_1.keys())
    x2 = list(count_2.keys())
    x3 = list(count_3.keys())
    y1 = []
    y2 = []
    y3 = []

    for i in list(count_1.keys()):
        y1.append(count_1[i])
    for i in list(count_2.keys()):
        y2.append(count_2[i])  
    for i in list(count_3.keys()):
        y3.append(count_3[i])      

    graphs1 = []
    graphs1.append(go.Bar(x=x1, y=y1, name="10만원~45만원",))
    graphs1.append(go.Bar(x=x2, y=y2, name="45만원~80만원",))
    graphs1.append(go.Bar(x=x3, y=y3, name="80만원~160만원",))
   
    

    layout_graph = {
        'title': '최근 이만큼이나 거래됐어요! :)',
        'xaxis_title': 'Date',
        'yaxis_title': '수량 (개)',
        'height': 480,
        'width': 1270,}

    plot_div = plot({'data': graphs1, 'layout': layout_graph}, 
                    output_type='div')
    
    context = dict()
    context['plot_div'] = plot_div
    context['fig_div'] = fig_div 

    return context
# 메인화면 데이터 시각화 end

def index(request):
    items = Item.objects.all().order_by('-pk') 
    
    context = data_visualization()
    context['items'] = items
                                 
                  
    return render(request, 'main/index.html',context)
    

def signup(request):
    return render(request, 'main/signup.html')

def join(request):

    items = Item.objects.all()
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()

    context = data_visualization()
    context['items'] = items

    return render(request, 'main/index.html',context )

def signin(request):

    return render(request, 'main/signin.html')

def login(request):
    loginEmail = request.POST['loginEmail'] # signin.html <input name=loginEmail> 사용을 위해
    loginPW = request.POST['loginPW']  # signin.html <input name=loginPW> 사용을 위해
    user = User.objects.get(user_email = loginEmail)
    if user.user_password == loginPW:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('main_index')
    else:
        return redirect('main_signin')   

def logout(request):
    del request.session['user_name']
    del request.session['user_email']
    return redirect('main_signin')



def upload(request):
 
        return render(request, 'main/upload.html')
    

def posting(request):
    
    items = Item.objects.all().order_by('-pk') 
    # 1208 수정 : 바로 글목록 볼 수 있게(양식다시제출 팝업 안 뜨게)
    if request.FILES.get('item_img'):
        users = User.objects.get(user_name=request.session['user_name']) #fk추가

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

    context = data_visualization()
    context['items'] = items

    return render(request, 'main/index.html',context) 



def blog(request):
    blogs = Item.objects.all()
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옴 
    return render(request, 'main/blog.html', {'blogs':blogs})
    

def new_post(request, pk):
    
    items = Item.objects.get(pk=pk)
    
    # trade_status = items.trade_status
    login_user = request.session['user_name']
    post_user = str(items.user_name)
     
    comments = CommentForm() #forms.py
   
    context = dict()
    context['items'] = items
    context['comments'] = comments
    context['login_user'] = login_user
    context['post_user'] =  post_user
    context['trade_status'] = items.trade_status
                                  #1/14 맞으면 삭제
    return render(request, 'main/new_post.html', context)
    
UPLOAD_DIR = r'C:\albino\mult_albo_project\media\images'

from PIL import Image

#가격예측버튼 누르면 실행되는 함수
def predict_price(request):
    #predict_img = request.POST['predict_img']

    if 'file1' in request.FILES:
        file = request.FILES['file1']
        file_name = file.name
        fp = open("%s%s" % (UPLOAD_DIR, file_name), 'wb')

    for chunk in file.chunks():
        fp.write(chunk)
        fp.close()

    model_weight_path = r'C:\albino\mult_albo_project\epoch100.h5'
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

    return render(request, 'main/upload.html', context) 


    
def remove_post(request, pk):
    post = Item.objects.get(pk=pk)
    items = Item.objects.all()
  
    post.delete()

    context = data_visualization()
    context['items'] = items 

        
    return render(request, 'main/index.html', context)
    


def boardEdit(request, pk):
  
    items = Item.objects.get(pk=pk)
   
     
    if request.method == "POST":
       
        items.item_name = request.POST.get('item_name')
        items.item_content = request.POST.get('item_content')
        items.item_price = request.POST.get('item_price')
        items.trade_status =request.POST.get('trade_status')
        item_date= request.POST.get('item_date',False)

        
        items.save()

        items = Item.objects.get(pk=pk)
        print(items)
        if items.trade_status == "거래완료" :
            
            #image의 파일 형태가 PIL 형태
            image = items.item_img
            

            # PIL 파일 또는 경로는 save할수 없기 때문에 InMemoryUploadedFile 함수를 이용하여 request해온
            # 이미지 파일 형식과 동일하게 맞춰줘야한다.(불러올 이미지, 새로 저장할 이미지 이름, 저장할 이미지 경로)
            heat_file = InMemoryUploadedFile(image, None, 'heat.jpeg', 'trade_images/jpeg',
                                     None, None)
            
            item_price = items.item_price
            status = Trade(item_date=item_date, item_img=heat_file ,item_price=item_price)
            status.save()
        

    items = Item.objects.all()
    context = data_visualization()
    context['items'] = items

    return render(request, 'main/index.html', context)
 
   

def create_comment(request, items_id):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.cleaned_data['comment']
        parent=None
        

    user = User.objects.get(user_name=request.session['user_name'])
    items = Item.objects.get(pk=items_id)
    

    new_comment = Comment(comment=comment, user_name=user, item_id=items, parent=parent)
    new_comment.save()

    return redirect('new_post', items_id)

def create_reply(request, items_id):
    reply_form = ReplyForm(request.POST) 
    if reply_form.is_valid():
        parent = reply_form.cleaned_data['parent']
        reply = reply_form.cleaned_data['comment']
        

    user = User.objects.get(user_name=request.session['user_name'])
    items = Item.objects.get(pk=items_id)

    new_comment = Comment(comment=reply, user_name=user, item_id=items, parent=parent)
    new_comment.save()

    return redirect('new_post', items_id)


def trade(request, item_id):
    filled_form = Trade(request.POST) #POST 요청이 들어오면,
    if filled_form.is_valid(): #유효성 검사 성공시 진행
        
        temp_form = filled_form.save(commit=False)
        
        temp_form.item_id = Item.objects.get(id=item_id)
        temp_form.user_name = User.objects.get(user_name=request.session['user_name'])
        temp_form.item_status = "거래상태"
        temp_form.save()
    return redirect('posting', {'trade':trade})







def css(request):
    return render(request, 'main/css.html')