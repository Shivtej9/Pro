# Generated by Django 4.2.5 on 2023-10-24 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_student_feedback_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_feedback',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
