# Generated by Django 2.2.5 on 2019-09-06 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analyzer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyworddata',
            name='id',
        ),
        migrations.AlterField(
            model_name='keyworddata',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='keyworddata',
            name='keyword',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]