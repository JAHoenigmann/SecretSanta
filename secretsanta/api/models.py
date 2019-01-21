from django.db import models

# Create your models here.
class GiftRecipient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    street_address = models.TextField()
    city = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
