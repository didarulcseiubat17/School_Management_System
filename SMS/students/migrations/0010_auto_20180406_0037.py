# Generated by Django 2.0.3 on 2018-04-05 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_class_class_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='class_name',
            field=models.ForeignKey(db_column='class_name', on_delete=django.db.models.deletion.CASCADE, to='students.Class'),
        ),
    ]
