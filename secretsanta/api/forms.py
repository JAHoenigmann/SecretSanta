from django.forms import ModelForm, TextInput
from .models import GiftRecipient

class GiftRecipientForm(ModelForm):
    class Meta:
        model = GiftRecipient
        fields = ['first_name', 'last_name', 'email', 'street_address', 'city',
                  'state', 'zip_code']
        widgets = {
            'state': TextInput(attrs={'style':'max-width: 2.5em'}),
            'zip_code': TextInput(attrs={'style':'max-width: 3.5em'}),
        }
