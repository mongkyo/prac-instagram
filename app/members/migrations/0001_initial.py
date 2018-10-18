# Generated by Django 2.1.2 on 2018-10-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('img_profile', models.ImageField(upload_to='user')),
                ('name', models.CharField(max_length=30)),
                ('site', models.URLField(max_length=150)),
                ('introduce', models.TextField(blank=True)),
            ],
        ),
    ]
