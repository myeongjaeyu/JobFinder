# Generated by Django 2.2.5 on 2019-10-15 06:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordData',
            fields=[
                ('date', models.DateField(auto_now=True)),
                ('count', models.IntegerField()),
                ('keyword', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('basic_words', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), null=True, size=None)),
                ('additional_words', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), null=True, size=None)),
            ],
            options={
                'unique_together': {('date', 'keyword')},
            },
        ),
    ]
