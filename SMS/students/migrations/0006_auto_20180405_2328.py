# Generated by Django 2.0.3 on 2018-04-05 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20180405_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='id',
        ),
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='id',
        ),
        migrations.AlterField(
            model_name='class',
            name='class_code',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='Roll_Num',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='class_name',
            field=models.ForeignKey(db_column='class_name', on_delete=django.db.models.deletion.PROTECT, to='students.Class'),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='subject_code',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]