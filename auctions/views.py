from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Max

from .models import User
from .models import AuctionListing
from .models import Bid
from .models import Comment
from .models import Watch
from .forms import AuctionListingForm
from .forms import BidForm
from .forms import CommentForm

def index(request):
    Listings = AuctionListing.objects.filter(is_open=True)
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

def new_listing_view(request):
    if request.method == 'POST':
        #below line made using cs50 chatbot assistance
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            #the next line replaces all the fields in the auction listing model in models.py
            new_listing = AuctionListing(user=form.cleaned_data['user'], title=form.cleaned_data['title'],
            description=form.cleaned_data['description'],is_open=form.cleaned_data['is_open'],
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
        # the below if else statement ensures im not attempting to access the bid amount
        #of None or a Decimal object, this in conjustion with the change i made lower in the
        #code means that there is no longer an error occuring due to variable types
        if bid:
            current_bids[listing.id] = bid.bid_amount
        else:
            current_bids[listing.id] = listing.initial_bid
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid_amount']
            highest_bidding_price = current_bids[auction_listing.id]
            if bid_amount <= highest_bidding_price:
                form.add_error('bid_amount',"Your bid is not sufficient and must be higher than the current bid amount")
            else:
                new_bid = Bid(user=request.user, auction_listing=auction_listing, bid_amount=form.cleaned_data['bid_amount'])
                new_bid.save()
                return render(request, 'auctions/listing.html', {'form': form, 'listing': auction_listing, 'current_bids': current_bids})
    else:
        form = BidForm()
    return render(request, 'auctions/listing.html', {'form': form, 'listing': auction_listing})
    
def listing_view(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    bid = listing.auction_listing.first()
    if bid != None:
        amount = bid.bid_amount
    else:
        amount = 0
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                listing = AuctionListing.objects.get(id=listing_id)
                new_comment = Comment(user=request.user, comment=form.cleaned_data['comment'], auction_listing=listing)
                new_comment.save()
                return render(request, 'auctions/listing.html', {'listing': listing})
            else:
                return HttpResponse("Go back to index page then click on listing to submit another comment")
        else:
            form = CommentForm()
            form.add_error('comment',"You must be signed in to submit a comment")
            return render(request, 'auctions/listing.html', {'form': form})
    else:
        form = CommentForm()
        if request.user.is_authenticated: 
            return render(request, 'auctions/listing.html', {'form': form,'listing': listing})
        else:
            return render(request, "auctions/not_in.html")

def closing_bid_view(request, listing_id):
    try:
        listing = AuctionListing.objects.get(id = listing_id)
    except AuctionListing.DoesNotExist:
        return form.add_error('listing',"No such listing found")
    bid = Bid.objects.filter(auction_listing=listing)
    if request.user.is_authenticated and request.user == listing.user:
        if listing.is_open:
            if request.method == 'POST':
                if bid.exists():
                    listing.is_open = False
                    top_bid = listing.top_bid()
                    listing.winner = top_bid.user
                else:
                    listing.is_open = False
                listing.save()
                return render(request, 'auctions/auction_closed.html', {'listing.winner': listing.winner})
        else:
            return HttpResponse("Bid already closed")
    else:
        return render(request, "auctions/not_in.html")

def not_in(request):
    return render(request, "auctions/not_in.html")

def previous_listings_view(request):
    inactive_listings = AuctionListing.objects.filter(is_open=False)
    return render(request, "auctions/previous_listings.html", {'inactive_listings': inactive_listings})

def watch(request):
    watchitems = Watch.objects.filter(user=request.user)
    lis = [listing.auction_listing for listing in watchitems]
    return render(request, "auctions/watch.html", {'watchlist': lis})

def a2w(request, listing_id):
    #a2w stands for add (listing) to watchlist
    user = request.user
    #the above line is used to associate the object with the user
    listing = AuctionListing.objects.get(id=listing_id)
    if not Watch.objects.filter(user=user, auction_listing=listing).exists():
        #the above line checks if the listing is already in the users watch list and was made using cs50 chatbot
        neww = Watch(user=user, auction_listing= listing )
        neww.save()
        #neww stands for new watch listing
    return HttpResponse("Added to Watchlist")

def category_view(request, category):
    items_in_list = AuctionListing.objects.filter(category=category)
    return render(request, 'auctions/category.html', {'items_in_list': items_in_list})

def categories(request):
    #below line generated with the assistance of cs50 chatbot
    categories = AuctionListing.objects.values('category').distinct()
    return render(request, "auctions/categories.html", {'categories': categories})

#the request.user part on line in closing_bid_view checks if the user is the same one who made the listing.

#using print() will ussually output the result to your command prompt