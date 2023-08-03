from django.urls import path
from . import views
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  
    path("signup", views.signup, name='signup'),
    path('signup/join', views.join, name= 'join'),  
    path('signin', views.signin, name='signin'),
    path('signin/login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('upload', views.upload, name = 'upload'),
    path('upload/predict_price', views.predict_price, name='predict_price'),
    path('posting', views.posting, name='posting'),
    path('posting/<int:pk>/', views.new_post, name='new_post'),
    path('posting/<int:pk>/upload/', views.remove_post, name= 'remove_post'),
    path('posting/<int:pk>/edit/', views.boardEdit, name= 'boardEdit'),
    path('trade', views.trade, name='trade'),
    path('create_comment/<int:items_id>', views.create_comment, name='create_comment'),
    path('create_reply/<int:items_id>', views.create_reply, name='create_reply'),
    
]