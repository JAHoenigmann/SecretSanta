# Generated by Django 2.1.7 on 2019-03-27 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190323_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftrecipient',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='giftrecipient',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='giftrecipient',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='giftrecipient',
            name='street_address',
            field=models.CharField(max_length=255),
        ),
    ]
