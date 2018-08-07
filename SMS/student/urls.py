from django.urls import path, include
from .import views

app_name = 'student'
urlpatterns = [
    path('allStudents', views.all_students, name='studentHome'),
    path('', include('django.contrib.auth.urls' )),
    path('loginValidate', views.user_login, name='login')
]