from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
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
    join_date = models.DateField(auto_now_add=True)

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
    section = models.OneToOneField(Section, db_column='class_code', on_delete=models.CASCADE)
    staff = models.OneToOneField(Staff, db_column='user_name', on_delete=models.PROTECT)



    def __str__(self):
        return str(self.section)+' | '+str(self.staff)


class Student(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    address = models.CharField(max_length=200, default='')
    join_date = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]

    def __str__(self):
        return self.first_name+' '+self.last_name


class StudentEnroll(models.Model):
    roll_num = models.CharField(max_length=20, primary_key=True, db_index=True,
                                help_text='Assign Roll Number formate : YY+class_code+max_seq')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, help_text='Assign Class_code')
    enroll_date = models.DateField(auto_now=True, db_index=True)

    class Meta:
        unique_together = ("student", "section")

    def __str__(self):
        return self.roll_num+' : '+str(self.student.first_name)


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
    studentEnroll = models.ForeignKey(StudentEnroll, db_column='roll_num', on_delete=models.CASCADE, db_index=True)
    subjects = models.ForeignKey(Subjects, db_column='subject_code', on_delete=models.CASCADE, db_index=True)

    def validate_subject_class(self):
        print('\n\n\n\n\n'+self.studentEnroll.roll_num)
        if SubjectEnroll.objects.filter(studentEnroll=self.studentEnroll,
                                        subjects=self.subjects).exists():
            raise ValidationError('This Course Is Already Enrolled')

        student_enroll = StudentEnroll.objects.get(roll_num=self.studentEnroll.roll_num)
        if not Subjects.objects.filter(subject_code=self.subjects.subject_code)\
                .filter(classes=student_enroll.section.classes).exists():
            raise ValidationError('Invalid Assignment Please check course belong to  student current class(standard)')

    def save(self, *args, **kwargs):
        self.validate_subject_class()
        super(SubjectEnroll, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.subjects.subject_code)


class Parents(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=(('m', 'Male'), ('f', 'Female')), blank=True, null=True)
    relation = models.CharField(max_length=50)

    def __str__(self):
        return self.student.first_name+' :: Parent :'+self.name+', '+self.relation


class StudentAttendance(models.Model):
    studentEnroll = models.ForeignKey(StudentEnroll, db_column='roll_num', on_delete=models.CASCADE)
    attend_date = models.DateField('Date', default=date.today(), auto_now=False, auto_now_add=False, db_index=True)
    staff = models.ForeignKey(Staff, db_column='user_name', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.studentEnroll)+' : '+str(self.staff)
