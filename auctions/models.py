from sys import maxsize
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import render


#The cs50 chatbot was used to help generate the User, AuctionListing,
# Bid and Comment classes
class User(AbstractUser):
    pass
    #bio = models.CharField(max_length= 64*4),
    #profile_photo = models.ImageField()

class AuctionListing(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "auction_listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    #below line syntax corrected by cs50 chatbot
    active = models.BooleanField(default=True)
    category = models.CharField(max_length = 64)
    #below 2 lines generated using cs50 ai assistance
    image = models.ImageField(upload_to='')
    initial_bid = models.DecimalField(max_digits=6, decimal_places=2)

    def current_bid(self):
        bid = Bid.objects.filter(auction_listing=self).order_by('-bid_amount').first()
        if bid:
            return bid.bid_amount
        else:
            return self.initial_bid
        
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "bid" )
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name= "auction_listing" )
    bid_amount = models.DecimalField(max_digits=6, decimal_places=2)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "comment")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
#when adding new models remember to run python manage.py makemigrations and python manage.py migrate
#so that django gnerates the correct sql commands to make the table your model represents