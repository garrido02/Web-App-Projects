
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/all/<str:author>", views.user_posts, name="user_posts"),
    path("following", views.following, name="following"),


    # API routes
    path("posts", views.posts, name="posts"),
    path("posts/all", views.page, name="page"),
    path("posts/<str:option>/<int:id>", views.edit, name="edit"),
    path("profile/<str:author>", views.profile, name="profile"),
    path("profile/<str:author>/Follow", views.follow, name="follow"),
    path("profile/<str:author>/Unfollow", views.unfollow, name="unfollow"),
]
