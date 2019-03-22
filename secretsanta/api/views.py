from django.shortcuts import render
from django.core import serializers
from .forms import GiftRecipientForm

# Create your views here.
def GiftRecipientEntry(request):
    if request.method == 'GET':
        form = GiftRecipientForm()
        return render(request, 'api/gift_recipient_entry.html', {'form' : form})

    if request.method == 'POST':
        form = GiftRecipientForm(request.POST)

        if form.is_valid():
            
            return render(request, 'api/gift_recipient_entered.html')
        return render(request, 'api/gift_recipient_entered.html')
