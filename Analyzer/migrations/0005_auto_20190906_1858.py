# Generated by Django 2.2.5 on 2019-09-06 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Analyzer', '0004_auto_20190906_1850'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keyworddata',
            old_name='preferential_treatment_word',
            new_name='preferential_treatment_words',
        ),
    ]