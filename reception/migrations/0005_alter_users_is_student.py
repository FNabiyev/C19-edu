# Generated by Django 3.2.5 on 2021-10-15 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reception', '0004_users_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
    ]