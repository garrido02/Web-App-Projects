from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=20, default='username')


class Listing(models.Model):
    choices = (
        (None, 'Select a Category'),
        ('Fashion', 'Fashion'), 
        ('Toys', 'Toys'), 
        ('Electronics', 'Eletronics'),
        ('Home', 'Home'),
        ('Video Games', 'Video Games'),
        ('Entertainment', 'Entertainment'),
        ('Technology', 'Technology'),
        ('Sports', 'Sports'),
        ('Clothing', 'Clothing'),
        ('Literature', 'Literature') 
    )
    category = models.CharField(choices=choices, max_length=40, blank=True, null=True)
    name = models.CharField(max_length=64, null=False, blank=False)
    price = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=999999)
    bid = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=999999)
    image = models.URLField(null=True, blank=True, max_length=9999)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    status = models.CharField(choices=(("Open", "Open"), ("Closed", "Closed")), blank=True, null=True, max_length=6)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", null=True, blank=True)
    def __str__(self):
        return f"Auction: {self.name}, Creator: {self.creator}, Status: {self.status}, Winner: {self.winner}"
    

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='item')
    bid = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=999999)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    def __str__(self):
        return f"Bid on {self.auction.name}: {self.user.nickname} -> {self.bid}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comments = models.TextField()
    def __str__(self):
        return f"Entry {self.id}: {self.user.nickname} - {self.auction.name}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"Entry {self.id}: {self.user.nickname} - {self.auction}"
