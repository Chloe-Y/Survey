from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>', views.survey, name = 'survey'),
    path('add/<int:pk>', views.addUser, name = 'addUser'),
    path('user/<int:pk>', views.user, name = 'user'),
    path('user/random/<int:pk>', views.randUser, name = 'randUser'),
    path('<slug:slug>/analysis', views.analysis, name = 'analysis'),
]
