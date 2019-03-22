from django.urls import path
from api import views

urlpatterns = [
    path('', views.GiftRecipientEntry, name='gift_recipient_entry'),
    path('RunSecretSantaOperation/', views.RunSecretSantaOperation, name='run_secret_santa_operation'),
]
