# Generated by Django 4.2 on 2024-12-28 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default-user.jpg', null=True, upload_to='images'),
        ),
    ]
