from sys import maxsize
from django.contrib.auth.models import AbstractUser
from django.db import models


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

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "bid" )
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "comment")
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

#when adding new models remember to run python manage.py makemigrations and python manage.py migrate
#so that django gnerates the correct sql commands to make the table your model represents