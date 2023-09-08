from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    auction_listings = models.CharField(max_length = 64)
    bids = models.CharField(max_length = 64)
    comments = models.CharField(max_length = 64)
