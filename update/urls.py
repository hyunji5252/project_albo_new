from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.update, name='update'),
    path("update_model", views.update_model, name='update_model'),
    
]