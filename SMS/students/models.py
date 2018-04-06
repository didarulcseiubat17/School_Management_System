from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
# Create your models here.


class StaffType(models.Model):
    staff_type = models.CharField(max_length=50,primary_key=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.staff_type


class Staff(models.Model):
    user_name = models.CharField(max_length=100,primary_key=True)
    StaffType = models.ForeignKey(StaffType, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20, unique=True) #unique can be set
    details = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.first_name+', '+self.last_name+' : '+str(self.StaffType)


class Class(models.Model):
    class_name = models.CharField(max_length=20, primary_key=True)
    class_details = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.class_name+': '+str(self.class_details)


class Section(models.Model):
    class_code = models.CharField(max_length=20, primary_key=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.CharField(max_length=5)
    #class_Teacher = models.CharField(max_length=20, null=True, blank=True)  # This Will be update when Teachers Tables are created
    #class_Teacher =models.ForeignKey(Staff, on_delete=set(''),null=True)
    def __str__(self):
        return 'Class code : '+self.class_code

class ClassTeacher(models.Model):
    class_code = models.ForeignKey(Section, on_delete=models.CASCADE)
    class_Teacher = models.ForeignKey(Staff, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.class_code)+' | '+str(self.class_Teacher)


class Student(models.Model):
    Roll_Num = models.CharField(max_length=20,primary_key=True)
    Name = models.CharField(max_length=150)
    Address = models.CharField(max_length=200,default='')
    class_code = models.ForeignKey(Section,  on_delete=models.CASCADE)
    #parent_code = models.CharField(max_length=20)

    def __str__(self):
        return self.Roll_Num+', '+self.Name


class Subjects(models.Model):
    subject_code = models.CharField(max_length=20, primary_key=True)
    class_name = models.ForeignKey(Class, db_column='class_name', on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100)
    details = models.CharField(max_length=500)
    '''
    def validate_subject_code(self):
        if self.subject_code==self.subject_name[:3]+self.class_name.class_name

    def save(self, *args, **kwargs):
        self.validate_subject_class()
        super(Subjects, self).save(*args, **kwargs)
    '''
    def __str__(self):
        return self.subject_code+', '+self.subject_name


class SubjectEnroll(models.Model):
    Roll_Num = models.ForeignKey(Student, on_delete=models.CASCADE,db_index=True)
    subject_code = models.ForeignKey(Subjects, on_delete=models.CASCADE,db_index=True)

    def validate_subject_class(self):
        if SubjectEnroll.objects.filter(Roll_Num=self.Roll_Num.Roll_Num, subject_code=self.subject_code.subject_code).exists():
            raise ValidationError('This Course Is Already Enrolled')

        student = Student.objects.get(Roll_Num=self.Roll_Num.Roll_Num)
        sec = Section.objects.get(class_code=student.class_code.class_code)
        if not Subjects.objects.filter(subject_code=self.subject_code.subject_code).filter(class_name=sec.class_name)\
                .exists():
            raise ValidationError('Invalid Assignment Please check course belong to  student class')


    def save(self, *args, **kwargs):
        self.validate_subject_class()
        super(SubjectEnroll, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.Roll_Num)+', '+str(self.subject_code)


class Parents(models.Model):
    Roll_Num = models.ForeignKey(Student,on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    contact =  models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=(('m','Male'), ('f', 'Female')), blank=True, null=True)
    relation = models.CharField(max_length=50)

    def __str__(self):
        return self.name+', '+self.relation+', '+self.gender


class StudentAttendance(models.Model):
    Roll_Num = models.ForeignKey(Student, on_delete=models.CASCADE)
    Attend_date = models.DateField(default=datetime.today(), blank=True,db_index=True)
    user_entry = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.Roll_Num)+' : '+self.Attend_date
