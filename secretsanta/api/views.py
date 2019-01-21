from django.shortcuts import render
from .forms import GiftRecipientForm

# Create your views here.
def GiftRecipientEntry(request):
    if request.method == 'GET':
        return render(request, 'api/gift_recipient_entry.html')
    if request.method == 'POST':
        return render(request, 'api/gift_recipient_entry.html')
