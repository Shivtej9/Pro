# Generated by Django 4.2.5 on 2023-10-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_studentresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='assignment_mark',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='exam_mark',
            field=models.IntegerField(),
        ),
    ]
