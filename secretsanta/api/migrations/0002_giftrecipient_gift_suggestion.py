# Generated by Django 2.1.7 on 2019-04-03 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='giftrecipient',
            name='gift_suggestion',
            field=models.TextField(blank=True),
        ),
    ]