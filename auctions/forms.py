#the following has been generated with the help of the cs50 chatbot
from django import forms
from .models import AuctionListing

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['user','title', 'description','active','category','image','initial_bid']
