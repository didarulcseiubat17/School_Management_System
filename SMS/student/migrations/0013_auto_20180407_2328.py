# Generated by Django 2.0.3 on 2018-04-07 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_auto_20180407_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectEnroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentEnroll', models.ForeignKey(db_column='roll_num', on_delete=django.db.models.deletion.CASCADE, to='student.StudentEnroll')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('subject_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=500)),
                ('classes', models.ForeignKey(db_column='class_name', on_delete=django.db.models.deletion.CASCADE, to='student.Class')),
            ],
        ),
        migrations.AddField(
            model_name='subjectenroll',
            name='subjects',
            field=models.ForeignKey(db_column='subject_code', on_delete=django.db.models.deletion.CASCADE, to='student.Subjects'),
        ),
    ]
