from django.shortcuts import render
from django.core import serializers
from django.core.mail import send_mail
from django.core import mail
from django.contrib.auth.decorators import login_required
from .forms import GiftRecipientForm
from .models import GiftRecipient
from .helpers import email_string

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
                        email_message = email_string(recipient=cleaned_form)
                        with mail.get_connection() as connection:
                            mail.EmailMessage(
                                'Your Secret Santa Information has been Saved!', email_message.entry_message(), 'hoenigmannmolina.secretsanta@gmail.com', [cleaned_form['email']],
                                connection=connection,
                            ).send()
                form = GiftRecipientForm()
                return render(request, 'api/gift_recipient_entered.html', {'form' : form})
            else:
                form = GiftRecipientForm()
                return render(request, 'api/gift_recipient_entry.html', {'form' : form})
        else:
            form = GiftRecipientForm()
            return render(request, 'api/gift_recipient_entry.html', {'form' : form})

@login_required
def RunSecretSantaOperation(request):
    runButton = request.POST.get('Run Secret Santa Operation')
    if runButton is not None:
        if runButton:
            temp = {}
            temp['first_name'] = 'Alec'
            temp['last_name'] = 'Hoenigmann'
            temp['street_address'] = '2415 Blairlogie Court'
            temp['city'] = 'Henderson'
            temp['state'] = 'NV'
            temp['zip_code'] = '89044'
            email_message = email_string(recipient=temp, gift_recipient=temp)
            # with mail.get_connection() as connection:
            #     mail.EmailMessage(
            #         "Here's Your Secret Santa Gift Recipient!", email_message.operation_message(), 'hoenigmannmolina.secretsanta@gmail.com', ['JAHoenigmann@student.fullsail.edu'],
            #         connection=connection,
            #     ).send()

    return render(request, 'api/run_secret_santa_operation.html')
