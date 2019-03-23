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
                        new_recipient = GiftRecipient.objects.get(first_name=cleaned_form['first_name'], last_name=cleaned_form['last_name'])
                        form = GiftRecipientForm()
                        return render(request, 'api/gift_recipient_duplicate.html', {'form' : form})
                    except GiftRecipient.DoesNotExist:
                        form.save()
                        email_message = email_string(giver=cleaned_form)
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
            rand.seed(datetime.now())
            recipients_data = GiftRecipientSerializer(GiftRecipient.objects.all(), many=True).data
            fail_counter = 0
            FAIL_LIMIT = 1000
            dict = {}

            while fail_counter < (FAIL_LIMIT + 1):
                givers = copy.deepcopy(recipients_data)
                recipients = copy.deepcopy(recipients_data)
                failsafe_triggered = False

                for giver in givers:
                    counter = 0
                    while counter < 51:
                        recipient = recipients[rand.randint(0, (len(recipients)) - 1)]
                        if recipient is not giver:
                            if counter >= 50:
                                if fail_counter >= FAIL_LIMIT:
                                    dict[giver['first_name'] + ' ' + giver['last_name']] = recipient['first_name'] + ' ' + recipient['last_name']
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

                            recipient_addr = recipient['street_address'].strip() + ', ' + recipient['city'].strip() + ', ' + recipient['state'].strip() + ' ' + recipient['zip_code'].strip()
                            giver_addr = giver['street_address'].strip() + ', ' + giver['city'].strip() + ', ' + giver['state'].strip() + ' ' + giver['zip_code'].strip()
                            if recipient_addr.lower() != giver_addr.lower():
                                recipients.remove(recipient)
                                dict[giver['first_name'] + ' ' + giver['last_name']] = recipient['first_name'] + ' ' + recipient['last_name']
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
                        print('*******\nFAILSAFE TRIGGERED | Fail Count = ' + str(fail_counter) + '\n*******')
                        break

                if failsafe_triggered == False:
                    print('clean run!')
                    break

            print('test finished')
            for key in dict.keys():
                print(key + ': ' + dict[key])

            # temp = {}
            # temp['first_name'] = 'Alec'
            # temp['last_name'] = 'Hoenigmann'
            # temp['street_address'] = '2415 Blairlogie Court'
            # temp['city'] = 'Henderson'
            # temp['state'] = 'NV'
            # temp['zip_code'] = '89044'
            # email_message = email_string(recipient=temp, gift_recipient=temp)
            # with mail.get_connection() as connection:
            #     mail.EmailMessage(
            #         "Here's Your Secret Santa Gift Recipient!", email_message.operation_message(), 'hoenigmannmolina.secretsanta@gmail.com', ['JAHoenigmann@student.fullsail.edu'],
            #         connection=connection,
            #     ).send()

    return render(request, 'api/run_secret_santa_operation.html')
