# Generated by Django 3.2.9 on 2022-06-21 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
