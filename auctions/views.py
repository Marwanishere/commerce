from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from .models import User
from .models import AuctionListing
from .models import Bid
from .models import Comment
from .forms import AuctionListingForm
from .forms import BidForm


def index(request):
    Listings = AuctionListing.objects.filter(active=True)
    current_bids = {}
    for listing in Listings:
        bid = Bid.objects.filter(auction_listing=listing).order_by('-bid_amount').first()
        if bid == None:
            bid = listing.initial_bid
        current_bids[listing.id] = bid
    return render(request, "auctions/index.html",{'Listings': Listings, 'current_bids': current_bids})


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
        #below line made using cs50 chatbot assistance
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            #the next line replaces all the fields in the auction listing model in models.py
            new_listing = AuctionListing(user=form.cleaned_data['user'], title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],active=form.cleaned_data['active'],
            category = form.cleaned_data['category'], image = form.cleaned_data['image'],
            initial_bid = form.cleaned_data['initial_bid'])
            new_listing.save()
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/new_listing.html', {'form': form})
    #return render(request, "auctions/new_listing.html")

#following function was made with the help of cs50 chatbot
def current_price(request, listing_id):
    auction_listing = AuctionListing.objects.get(id=listing_id)
    auction_listings = AuctionListing.objects.all()
    current_bids = {}
    for listing in auction_listings:
        bid = Bid.objects.filter(auction_listing=listing).order_by('-bid_amount').first()
        if bid == None:
            bid = listing.initial_bid
        current_bids[listing.id] = bid if bid else listing.initial_bid
        current_bids
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid = Bid(user=request.user, auction_listing=auction_listing, bid_amount=form.cleaned_data['bid_amount'])
            new_bid.save()
            
            return render(request, 'auctions/listing.html', {'form': form, 'listing': auction_listing, 'current_bids': current_bids})
    else:
        form = BidForm()
    return render(request, 'auctions/listing.html', {'form': form, 'listing': auction_listing, 'current_bids': current_bids})
    
def listing_view(request, listing_id):
    #following line was made with cs50 chatbot assistance
    listing = AuctionListing.objects.get(id=listing_id)
    return render(request, 'auctions/listing.html', {'listing': listing})