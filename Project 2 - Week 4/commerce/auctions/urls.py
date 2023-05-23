from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name='create'),
    path("listing/<int:id>", views.listing, name="listing"),
    path("add_watchlist", views.watch, name="add_watchlist"),
    path("de_watchlist", views.de_watch, name="de_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close", views.close, name="close"),
    path("bid", views.bid, name="bid"),
    path("won", views.won, name="won"),
    path("comment", views.comment, name="comment"),
    path("category", views.category, name="category")
]
