from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
from random import *
from main.models import *
from django.db import connection

from django.db.models import Count
import os


def update(request):

    return render(request, 'modeling.html')

#---------데이터 보강 실행-----------#
import update.modeling as modeling
import pandas as pd

def update_model(request):

    trade = Trade.objects.all() 
    trade_count = len(trade)
    td = Trade.objects.get(pk=1)

    modeling.main()

    #테이블에 데이터가 64개 이상일 경우에만 실행
    if trade_count >= 64:
        # 기존 모델 파일 삭제
        os.remove(r'C:\albino\mult_albo_project\epoch100.h5')

        

        #데이터 보강 실행
        modeling.main()

        

    return render(request, 'modeling.html')
    # return HttpResponse('데이터 재보강중')