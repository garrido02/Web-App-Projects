
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/search", views.profile, name="profile"),
    path("support/<int:id>", views.support, name="support"),
    path("pack-<str:short>", views.pacote, name="pacote"),



    # API
    path("profile/nick/<str:user>", views.change_nick, name="nick"),
    path("profile/search/pass/<str:user>", views.change_pass, name="nick"),
    path("ticket", views.ticket, name="ticket"),
    path("ticket/<int:id>", views.close, name="close")
]
