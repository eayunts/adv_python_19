# Generated by Django 2.2.5 on 2019-12-25 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20191224_2120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='Slug',
        ),
    ]
