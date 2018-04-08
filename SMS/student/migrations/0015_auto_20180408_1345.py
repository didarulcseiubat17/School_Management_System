# Generated by Django 2.0.3 on 2018-04-08 08:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_parents_studentattendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='join_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='studentEnroll',
            field=models.ForeignKey(db_column='roll_num', on_delete=django.db.models.deletion.CASCADE, to='student.StudentEnroll'),
        ),
    ]