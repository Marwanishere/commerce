#the following has been generated with the help of the cs50 chatbot
from django import forms
from .models import AuctionListing
from .models import Bid
from .models import Comment

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['user','title', 'description','is_open','category','image','initial_bid']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
