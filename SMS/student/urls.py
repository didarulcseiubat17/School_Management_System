from django.urls import path
from .import views

app_name = 'student'
urlpatterns = [
    path('allStudents', views.all_students, name='studentHome')
]