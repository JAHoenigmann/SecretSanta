from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.decorators import login_required
from .forms import GiftRecipientForm
from .models import GiftRecipient

# Create your views here.
def GiftRecipientEntry(request):
    if request.method == 'GET':
        form = GiftRecipientForm()
        return render(request, 'api/gift_recipient_entry.html', {'form' : form})

    if request.method == 'POST':
        # ['first_name', 'last_name', 'email', 'street_address', 'city', 'state', 'zip_code']
        form = GiftRecipientForm(request.POST)
        if form is not None:
            if form.is_valid():
                cleaned_form = form.cleaned_data
                if cleaned_form is not None:
                    try:
                        new_recipient = GiftRecipient.objects.get(first_name=cleaned_form['first_name'], last_name=cleaned_form['last_name'])
                        form = GiftRecipientForm()
                        return render(request, 'api/gift_recipient_duplicate.html', {'form' : form})
                    except GiftRecipient.DoesNotExist:
                        form.save()
                form = GiftRecipientForm()
                return render(request, 'api/gift_recipient_entered.html', {'form' : form})
            else:
                form = GiftRecipientForm()
                return render(request, 'api/gift_recipient_entry.html', {'form' : form})
        else:
            form = GiftRecipientForm()
            return render(request, 'api/gift_recipient_entry.html', {'form' : form})

# def check_admin(user):
#     return user.is_superuser

@login_required
def RunSecretSantaOperation(request):
    form = GiftRecipientForm()
    return render(request, 'api/srun_secret_santa_operation.html')
