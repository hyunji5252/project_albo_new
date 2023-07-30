from django.shortcuts import render, redirect
from random import *
from .models import *
from django.db import connection
from django.urls import reverse
from django.db.models import Q # Q는 Django내 Model을 관리할 때 사용되는 ORM으로 SQL의 WHERE절과 같은 조건문을 추가할 때 사용한다.
from .forms import *
from datetime import datetime
from django.http import HttpResponse
#from google.protobuf import descriptor as _descriptor

# from PIL import Image
# import tensorflow as tf
# import os,glob
# import numpy as np
# from tensorflow import keras
# from tensorflow.keras.models import load_model, Model
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
# import pandas as pd
# from plotly.offline import plot
# import plotly.graph_objects as go
# from django.core.files.uploadedfile import InMemoryUploadedFile


def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

def join(request):
    
    # 메인화면 접속 시 필요한 데이터
    #items = Item.objects.all()
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    pw_check = request.POST['signupPWcheck']
    gender = request.POST['signupGender']
    age = request.POST['signupAge']

    if pw==pw_check:
        user = Users(user_name = name, user_email = email, user_password = pw, user_gender = gender, user_age = age)
        user.save()
    
    # context = data_visualization()
    # context['items'] = items

        return render(request, 'home.html')

    else:
        return render(request, 'signup.html')