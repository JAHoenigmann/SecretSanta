# Generated by Django 2.1.5 on 2019-01-21 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftrecipient',
            name='state',
            field=models.CharField(default=None, max_length=2),
        ),
        migrations.AlterField(
            model_name='giftrecipient',
            name='city',
            field=models.CharField(max_length=100),
        ),
    ]
