from django.forms import ModelForm
from .models import GiftRecipient

class GiftRecipientForm(ModelForm):
    class Meta:
        model = GiftRecipient
        fields = ['first_name', 'last_name', 'email', 'street_address', 'city',
                  'state', 'zip_code']
