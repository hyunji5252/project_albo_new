from .models import *
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment',]

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','parent']

class EditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields= ['item_name','item_price','item_content','item_img']

