from django.shortcuts import render
from django.http import request
from .models import Student
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


# Create your views here.
def all_students(request):
    context = dict()
    context['who'] = 'All Students'
    try:
        context['table_data'] = Student.objects.all()
        data=[]
        if len(context['table_data']) > 0:
            fields = [f.name for f in context['table_data'][0]._meta.local_fields]
            context['columns_header'] = [" ".join(field.split('_')).upper() for field in fields]
        else:
            context['columns_header'] = []

        data=[]
        for obj in context['table_data']:
            data.append([obj.id, obj.first_name, obj.last_name, obj.address, obj.join_date])
        context['rows'] = data

    except Exception as e:
        print('Exception occurs while fetching student data',e)

    return render(request, 'student/actor_details.html', context=context)


def user_login(request):
    user_name = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=user_name, password=password)
    if user is not None:
        login(request, user)
        # redirect to success page
        return HttpResponseRedirect('/students/allStudents')
    else:
        # return to failure
        return render(request, 'registration/login.html',{'message': 'Invalid user credentials'})