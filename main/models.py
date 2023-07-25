from django.db import models
from django.forms import ModelForm # 모델 폼 설정

# Create your models here.

class User(models.Model):
    # user_id = 
    user_name = models.CharField()
    user_password =
    user_email =
    user_data = 
    user_gender =
    user_age =

class Iten(models.Model):
    item_id = 
    user_id = 
    user_name =
    item_name =
    item_price =
    item_img =
    item_content =
    item_date =
    trade_status =

class Comment(models.Model):
    comment_id =
    user_id =
    user_name =
    item_id =
    comment =
    comment_date =
    parent_comment_id =

class Trade(models.Model):
    trade_id =
    item_img =
    item_price =
    trade_date =
    user_gender =
    user_age =