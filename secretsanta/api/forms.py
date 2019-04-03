from django.forms import ModelForm, TextInput
from .models import GiftRecipient
from django.utils.translation import ugettext_lazy as _

class GiftRecipientForm(ModelForm):
    class Meta:
        model = GiftRecipient
        fields = ['first_name', 'last_name', 'email', 'street_address', 'city',
                  'state', 'zip_code', 'gift_suggestion']
        widgets = {
            'state': TextInput(attrs={'style':'max-width: 2.5em'}),
            'zip_code': TextInput(attrs={'style':'max-width: 3.5em'}),
            'gift_suggestion': TextInput(),
        }

        labels = {
            'gift_suggestion': _("Give a suggestion that you'd like to recieve:")
        }
