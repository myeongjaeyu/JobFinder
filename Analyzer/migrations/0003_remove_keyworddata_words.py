# Generated by Django 2.2.5 on 2019-09-06 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Analyzer', '0002_auto_20190906_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyworddata',
            name='words',
        ),
    ]
