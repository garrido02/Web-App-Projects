from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Listing, Bid, Comment, Watchlist
from django.db.models import Max


# Form creation for creating an auction
class NewForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('name', 'price', 'category', 'description', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Item Name'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price $'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your auction'}),
            'image': forms.TextInput(attrs={'placeholder': 'Image URL'})
        }


# Form for bidding
class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ('bid',)
        widgets = {
            'bid': forms.NumberInput(attrs={'placeholder': 'Bid $'})
        }


# Form for Commenting
class ComForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comments',)
        widgets = {
            'comments' : forms.Textarea(attrs={'placeholder': 'Add your comment to the current auction'})
        }


# Main page
def index(request):
    # Ensure no message stays visable
    try:
        del request.session["message"]

    except KeyError:
        pass

    listings = Listing.objects.filter(status="Open")
    return render(request, "auctions/index.html", {
        'listings':listings
    })


# Login page
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


# Log out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        nickname = request.POST["nickname"]
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
            change = User.objects.get(username=username)
            change.nickname = nickname
            change.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Create Auction
@login_required
def create_listing(request):
    # Ensure no message stays visable
    try:
        del request.session["message"]

    except KeyError:
        pass

    # Shows creation page
    if request.method == "GET":
        return render(request, 'auctions/create.html', {
            'form': NewForm()
        })
    else:
        form = NewForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            image = form.cleaned_data["image"]

            if not image:
                image = "/static/auctions/noimage.jpg"

            # Capitalize each entry name and get user
            name = name.capitalize()
            user = request.user

            # Save info from form to the database
            instance = form.save(commit=False)
            instance.name = name
            instance.creator = user
            instance.status = "Open"
            instance.bid = price
            instance.image = image
            instance.save()
        
        else:
            return render(request, "auctions/create.html", {
                'message': 'Please fill the form correctly.',
                'form': NewForm()
            })


        return HttpResponseRedirect(reverse("index"))
    

# Auction/item Page
def listing(request, id):
    # Get user
    user = request.user

    # Get listings with id, capitalize name
    auction = Listing.objects.get(id=id)
    name = auction.name
    name = name.capitalize()

    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
            'auction': auction
        })
    
    else:
        try:
            # Try to get watch list
            watchlist = Watchlist.objects.get(user=user, auction=auction)

            # Check if there are bids and comments
            bid = Bid.objects.filter(auction=auction).order_by('bid')
            highest = bid.last
            comment = Comment.objects.filter(auction=auction)


            # Render template with all info for the specific auction
            return render(request, "auctions/listing.html", {
                'auction':auction,
                'user': user, 
                'watchlist': watchlist,
                'form': BidForm(),
                'bid': bid,
                'count': bid.count,
                'highest': highest,
                'comment' : comment,
                'comment_form': ComForm()
            })
        
        except ObjectDoesNotExist:
            # If no watchlist we skip inserting it into the template
            # We check if there are bids
            bid = Bid.objects.filter(auction=auction)
            highest = bid.last
            comment = Comment.objects.filter(auction=auction)

            # Render template with all info for the specific auction
            return render(request, "auctions/listing.html", {
                'auction':auction,
                'user': user, 
                'form': BidForm(),
                'bid': bid,
                'count': bid.count,
                'highest': highest,
                'comment': comment,
                'comment_form': ComForm()
            })


# Add to watchlist
@login_required        
def watch(request):
    if request.method == "POST":
        # Ensure no message stays visable
        try:
            del request.session["message"]

        except KeyError:
            pass

        # Get user and auction id
        user = request.user
        id = request.POST["auction_id"]

        # Get entry that corresponds to id
        auction = Listing.objects.get(pk=id)

        # Open a new WatchList line and assign user and auction
        watchlist = Watchlist()
        watchlist.user = user
        watchlist.auction = auction
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    

# Removing from watchlist
@login_required        
def de_watch(request):
    if request.method == "POST":

        # Ensure no message stays visable
        try:
            del request.session["message"]

        except KeyError:
            pass

        # Get user and auction id
        user = request.user
        id = request.POST["auction_id"]

        # Get auction that corresponds to id
        auction = Listing.objects.get(pk=id)

        # Delete watchlist entry
        Watchlist.objects.get(user=user, auction=auction).delete()

        return HttpResponseRedirect(reverse("listing", args=(id,)))


# Watchlist page
@login_required
def watchlist(request):
    # Ensure no message stays visable
    try:
        del request.session["message"]

    except KeyError:
        pass

    # Get user
    user = request.user

    #  Try to get user watchlist
    watchlist = Watchlist.objects.filter(user=user)
    if watchlist:
        # Render template with all info for the specific auction
        return render(request, "auctions/watchlist.html", {
            'watchlist': watchlist,
        })

    else:
        # If no watchlist we display message
        return render(request, "auctions/watchlist.html", {
            'message': 'Your watchlist has no items.'
        })
    

# Delete auction
@login_required
def close(request):
    if request.method == 'POST':
        # Get auction's id
        id = request.POST["auction_id"]

        # Get user 
        user = request.user

        # Get the auction entry change status to closed
        auction = Listing.objects.get(id=id)

        # Get highest bidder AKA winner
        bid = Bid.objects.filter(auction=auction).order_by('-bid')

        if bid:
            # Path only chosen if there was a bid
            winner = bid[0].user
            auction.status = "Closed"
            auction.winner = winner
            auction.save()

        else:
            # Path chosen if no bids are placed and creator closes the auction
            auction.status = "Closed"
            auction.winner = auction.creator
            auction.save()

        # Remove auction from user wishlist if is on
        # Try to get user watchlist
        try:
            Watchlist.objects.get(auction=auction, user=user).delete()
            return HttpResponseRedirect(reverse("index"))
            
        except ObjectDoesNotExist:
            # If no watchlist we just return the normal page
            return HttpResponseRedirect(reverse("index"))


@login_required
# Bidding
def bid(request):
    if request.method == "POST":
        # Ensure no message stays visable
        try:
            del request.session["message"]

        except KeyError:
            pass
        

        # Get Form data
        form = BidForm(request.POST)
        if form.is_valid():
            new_bid = form.cleaned_data['bid']
            
            # Get user Data
            user = request.user

            # Get auction info
            id = request.POST["auction_id"]
            auction = Listing.objects.get(pk=id)

            # Get highest bid
            bid = Bid.objects.filter(auction=auction).order_by('-bid')

            try:
                # This path is only chosen if there is a bid[0] index
                # Check if new bid is higher than current highest
                if new_bid > bid[0].bid:
                    # If so update bid price on auction db
                    auction.bid = new_bid
                    auction.save()

                    # Update bid db
                    instance = form.save(commit=False)
                    instance.user = user
                    instance.auction = auction
                    instance.save()

                    return HttpResponseRedirect(reverse("listing", args=(id,)))

                else:
                    request.session["message"] = "Your bid must be at least 1$ higher than the current highest bid."
                    return HttpResponseRedirect(reverse("listing", args=(id,)))
            
            except IndexError:
                # Index error only occurs when there is no bid yet
                if new_bid >= auction.price:
                    # If so update auction db
                    auction.bid = new_bid
                    auction.save()

                    # Update bid db
                    instance = form.save(commit=False)
                    instance.user = user
                    instance.auction = auction
                    instance.save()

                    return HttpResponseRedirect(reverse("listing", args=(id,)))
 
                else:
                    request.session["message"] = "Your bid must be higher or equal than the starting price."
                    return HttpResponseRedirect(reverse("listing", args=(id,)))
                

# Won auctions page
@login_required
def won(request):
    # Ensure no message stays visable
    try:
        del request.session["message"]

    except KeyError:
        pass

    # Get user and auctions won by the user
    user = request.user
    auction_all = Listing.objects.filter(winner=user)

    # Exclude auction where creator is user (meaning user closed auctions before anyone bid)
    auction = auction_all.exclude(creator=user)

    return render(request, "auctions/won.html", {
        'auction': auction,
        'user': user
    })


@login_required
# Comment
def comment(request):
    if request.method == "POST":
        # Ensure no message stays visable
        try:
            del request.session["message"]

        except KeyError:
            pass
        
        # Get Form data
        form = ComForm(request.POST)
        if form.is_valid():
            
            # Get user Data
            user = request.user

            # Get auction info
            id = request.POST["auction_id"]
            auction = Listing.objects.get(pk=id)

            # Save Comment info
            instance = form.save(commit=False)
            instance.user = user
            instance.auction = auction
            instance.save()

            return HttpResponseRedirect(reverse("listing", args=(id,)))
        

# Categories view
def category(request):
    if request.method == 'GET':
        # Ensure no message stays visable
        try:
            del request.session["message"]
        
        except KeyError:
            pass

        # Get list of available categories:
        choices = ['Fashion', 'Toys', 'Electronics', 'Home', 'Video Games', 'Entertainment', 
                   'Technology', 'Sports', 'Clothing', 'Literature']
        
        return render(request, "auctions/category.html", {
            'choices':choices
        })
    
    # If POST
    else:
        # Get user choice and all the listings belonging to that category 
        choice = request.POST["choice"]
        listings_all = Listing.objects.filter(category=choice)
        listings = listings_all.exclude(status="Closed")

        return render(request, "auctions/cat_filter.html", {
            'listings':listings,
            'choice':choice
        })


