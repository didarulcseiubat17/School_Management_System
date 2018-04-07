from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(StaffType)
admin.site.register(Staff)
admin.site.register(Class)
admin.site.register(Section)
admin.site.register(ClassTeacher)
admin.site.register(Student)
admin.site.register(StudentEnroll)
admin.site.register(SubjectEnroll)
admin.site.register(Subjects)
admin.site.register(Parents)
admin.site.register(StudentAttendance)


