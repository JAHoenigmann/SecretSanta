from django.shortcuts import render
from django.core import serializers
from django.core import mail
from django.contrib.auth.decorators import login_required
from .forms import GiftRecipientForm
from .models import GiftRecipient
from .helpers import email_string
from .serializers import GiftRecipientSerializer
from datetime import datetime
import copy
import random as rand

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
                        new_recipient = GiftRecipient.objects.get(first_name=cleaned_form['first_name'].lower().strip(), last_name=cleaned_form['last_name'].lower().strip())
                        new_recipient.email = cleaned_form['email'].strip()
                        new_recipient.street_address = cleaned_form['street_address'].lower().strip()
                        new_recipient.city = cleaned_form['city'].lower().strip()
                        new_recipient.state = cleaned_form['state'].upper().strip()
                        new_recipient.zip_code = cleaned_form['zip_code'].strip()
                        new_recipient.gift_suggestion = cleaned_form['gift_suggestion'].strip()
                        new_recipient.save()

                        form = GiftRecipientForm()
                        return render(request, 'api/gift_recipient_duplicate.html', {'form' : form})
                    except GiftRecipient.DoesNotExist:
                        new_recipient = GiftRecipient(
                            first_name=cleaned_form['first_name'].lower().strip(),
                            last_name=cleaned_form['last_name'].lower().strip(),
                            email=cleaned_form['email'].strip(),
                            street_address=cleaned_form['street_address'].lower().strip(),
                            city=cleaned_form['city'].lower().strip(),
                            state=cleaned_form['state'].upper().strip(),
                            zip_code=cleaned_form['zip_code'].strip(),
                            gift_suggestion=cleaned_form['gift_suggestion'].strip()
                        )
                        new_recipient.save()
                        email_message = email_string(giver=cleaned_form)
                        # with mail.get_connection() as connection:
                        #     mail.EmailMessage(
                        #         'Your Secret Santa Information has been Saved!', email_message.entry_message(), 'hoenigmannmolina.secretsanta@gmail.com', [cleaned_form['email']],
                        #         connection=connection,
                        #     ).send()
                form = GiftRecipientForm()
                return render(request, 'api/gift_recipient_entered.html', {'form' : form})
            else:
                form = GiftRecipientForm()
                return render(request, 'api/gift_recipient_error.html', {'form' : form})
        else:
            form = GiftRecipientForm()
            return render(request, 'api/gift_recipient_entry.html', {'form' : form})

@login_required
def RunSecretSantaOperation(request):
    runButton = request.POST.get('Run Secret Santa Operation')
    if runButton is not None:
        if runButton:
            rand.seed(datetime.now())
            recipients_data = GiftRecipientSerializer(GiftRecipient.objects.all(), many=True).data
            fail_counter = 0
            FAIL_LIMIT = 1000
            dict = {}
            givers = copy.deepcopy(recipients_data)

            while fail_counter < (FAIL_LIMIT + 1):
                recipients = copy.deepcopy(recipients_data)
                failsafe_triggered = False

                for giver in givers:
                    counter = 0
                    while counter < 51:
                        recipient = recipients[rand.randint(0, (len(recipients)) - 1)]
                        if recipient is not giver:
                            if counter >= 50:
                                if fail_counter >= FAIL_LIMIT:
                                    recipients.remove(recipient)
                                    # with mail.get_connection() as connection:
                                    #     email_message = email_string(giver=giver, gift_recipient=recipient)
                                    #     mail.EmailMessage(
                                    #         "Here's Your Secret Santa Gift Recipient!", email_message.operation_message(), 'hoenigmannmolina.secretsanta@gmail.com', [giver['email']],
                                    #         connection=connection,
                                    #     ).send()
                                    break
                                failsafe_triggered = True
                                break

                            recipient_addr = recipient['street_address'] + ', ' + recipient['city'] + ', ' + recipient['state'] + ' ' + recipient['zip_code']
                            giver_addr = giver['street_address'] + ', ' + giver['city'] + ', ' + giver['state'] + ' ' + giver['zip_code']

                            if recipient_addr != giver_addr:
                                recipients.remove(recipient)
                                # with mail.get_connection() as connection:
                                #     email_message = email_string(giver=giver, gift_recipient=recipient)
                                #     mail.EmailMessage(
                                #         "Here's Your Secret Santa Gift Recipient!", email_message.operation_message(), 'hoenigmannmolina.secretsanta@gmail.com', [giver['email']],
                                #         connection=connection,
                                #     ).send()
                                break
                        counter += 1

                    if failsafe_triggered is True:
                        fail_counter += 1
                        break

                if failsafe_triggered == False:
                    break

            # with mail.get_connection() as connection:
            #     mail.EmailMessage(
            #         'All Secret Santa Emails have been Sent', f'There were {fail_counter} failed attempts with a fail limit of: {FAIL_LIMIT}.', 'hoenigmannmolina.secretsanta@gmail.com', ['JAHoenigmann@student.fullsail.edu'],
            #         connection=connection,
            #     ).send()

    return render(request, 'api/run_secret_santa_operation.html')
