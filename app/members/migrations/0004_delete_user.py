# Generated by Django 2.1.2 on 2018-10-22 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20181023_0057'),
        ('members', '0003_auto_20181018_2044'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
