# Generated by Django 3.1 on 2021-01-08 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0004_auto_20210107_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='first_name',
            new_name='user_name',
        ),
    ]
