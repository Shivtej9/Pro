# Generated by Django 4.2.5 on 2023-10-24 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rename_attendance_data_attendance_attendance_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='attendance_date',
            new_name='attendance_data',
        ),
    ]