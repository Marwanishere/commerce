from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import AuctionListing
from .models import Bid
from .models import Comment
from .forms import AuctionListingForm


def index(request):
    Listings = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html",{'Listings': Listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def check(request):
    complete = 1
    if complete == 1:
        return render(request, "auctions/index.html")
    

def new_listing_view(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            #the next line replaces all the fields in the auction listing model in models.py
            new_listing = AuctionListing(user=form.cleaned_data['user'], title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],active=form.cleaned_data['active'],
            category = form.cleaned_data['category'], image = form.cleaned_data['image'])
            new_listing.save()
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/new_listing.html', {'form': form})
    #return render(request, "auctions/new_listing.html")