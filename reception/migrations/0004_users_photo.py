# Generated by Django 3.2.5 on 2021-10-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reception', '0003_chiqim_kirim'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users'),
        ),
    ]
