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
    StaffType = models.ForeignKey(StaffType, db_column='staff_type', on_delete=models.PROTECT)
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
    classes = models.ForeignKey(Class, db_column='class_name', on_delete=models.CASCADE)
    section = models.CharField(max_length=5, default='A')

    def __str__(self):
        return 'Class code : '+self.class_code


class ClassTeacher(models.Model):
    section = models.ForeignKey(Section, db_column='class_code', null=False, default='Teacher',primary_key=True,
                                on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, db_column='user_name', unique=True, on_delete=models.PROTECT)

   # def validate_classTeacher(self):
        # Confirm that only one class teacher for each class

    def __str__(self):
        return str(self.section)+' | '+str(self.staff)


class Student(models.Model):
    Roll_Num = models.CharField(max_length=20,primary_key=True)
    Name = models.CharField(max_length=150)
    Address = models.CharField(max_length=200,default='')
    section = models.ForeignKey(Section, db_column='class_code', on_delete=models.CASCADE)


    def __str__(self):
        return self.Roll_Num+', '+self.Name


class Subjects(models.Model):
    subject_code = models.CharField(max_length=20, primary_key=True)
    classes = models.ForeignKey(Class, db_column='class_name', on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=100)
    details = models.CharField(max_length=500)

    def validate_subject_code(self):
        #Validate Subject Code formate Standard
        class_name_code = self.classes.class_name
        if len(class_name_code) == 1:
            class_name_code = '0'+class_name_code
        if self.subject_code != self.subject_name[:3].upper()+class_name_code:
            raise ValidationError('Invalid Subject Code Formate EX : SUBNAME(first 3 Char)+Class_name(ex: 10) ')

    def save(self, *args, **kwargs):
        self.validate_subject_code()
        super(Subjects, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject_code+', '+self.subject_name


class SubjectEnroll(models.Model):
    students = models.ForeignKey(Student, db_column='Roll_Num', on_delete=models.CASCADE,db_index=True)
    subjects = models.ForeignKey(Subjects, db_column='subject_code', on_delete=models.CASCADE,db_index=True)

    def validate_subject_class(self):
        if SubjectEnroll.objects.filter(Roll_Num=self.students.Roll_Num, subject_code=self.subjects.subject_code).exists():
            raise ValidationError('This Course Is Already Enrolled')

        student = Student.objects.get(Roll_Num=self.students.Roll_Num)
        sec = Section.objects.get(class_code=student.class_code.class_code)
        if not Subjects.objects.filter(subject_code=self.subjects.subject_code).filter(class_name=sec.class_name)\
                .exists():
            raise ValidationError('Invalid Assignment Please check course belong to  student class')


    def save(self, *args, **kwargs):
        self.validate_subject_class()
        super(SubjectEnroll, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.students)+', '+str(self.subjects)


class Parents(models.Model):
    student = models.ForeignKey(Student, db_column='Roll_Num', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=(('m','Male'), ('f', 'Female')), blank=True, null=True)
    relation = models.CharField(max_length=50)

    def __str__(self):
        return self.name+', '+self.relation+', '+self.gender


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, db_column='Roll_Num', on_delete=models.CASCADE)
    Attend_date = models.DateField(default=datetime.today(), blank=True,db_index=True)
    staff = models.ForeignKey(Staff, db_column='user_name', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.student)+' : '+self.Attend_date
