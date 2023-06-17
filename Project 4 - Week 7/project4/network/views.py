import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Post, Follow


def index(request):
    user = request.user

    # Handle page selection so that we only have 10 entries per page
    posts = Post.objects.all()
    posts = posts.order_by('-timestamp').all()
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    list = p.get_page(page)

    return render(request, "network/index.html", {
        'user':user,
        'list':list
    })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        image = "/static/network/noimage.png"

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user.image = image
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        
        # Create following entries for each user that registers
        follow = Follow(user=user)
        follow.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# Creating a function for user to write a post
@login_required
@csrf_exempt
def posts(request):

    # Composing a new email must be via POST
    if request.method == "POST":

        # Get contents of post
        data = json.loads(request.body)

        post = Post()
        post.author = request.user
        post.body = data.get("body")
        post.save()

        return JsonResponse({"message": "Post created successfully."})
    
    else:
        return JsonResponse({"message": "Request must be via POST"})


# Function for seeing posts from whom the author follows
def page(request):

    posts = Post.objects.all()

    # Return in reverse order
    posts = posts.order_by('-timestamp').all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def user_posts(request, author):

    user = request.user

    # Filter posts by author
    posts = Post.objects.filter(author__username=author)

    # Return in reverse order
    posts = posts.order_by('-timestamp').all()
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    list = p.get_page(page)

    return render(request, "network/profile.html", {
        'user':user,
        'list':list
    })


# Create a function for going to a profile
def profile(request, author):

    # Get follow info for author
    follows = Follow.objects.filter(user__username=author)

    if not follows:
        return JsonResponse({"message": "No follows exist for this author"})

    return JsonResponse([follow.serialize() for follow in follows], safe=False)


@login_required
# Create a function to handle follow
def follow(request, author):

    # Get current user
    user = request.user
    user = user.id

    follow = Follow.objects.get(user__username=author)
    following = Follow.objects.get(user__username=request.user)

    # Make sure user cannot follow himself
    if follow.user == request.user:
        return JsonResponse({"message": "Impossible to follow self_1"}) 
     
    else:    
        # Handle Follow for author
        follow.followers.add(user)
        follow.save()

        # Handle following for user
        following.following.add(follow.user)
        following.save()
        return JsonResponse({"message": "Everything went accordingly"})


@login_required
# Create a function to handle unfollow
def unfollow(request, author):

    # Get current user
    user = request.user
    user = user.id

    follow = Follow.objects.get(user__username=author)
    following = Follow.objects.get(user__username=request.user)

    # Make sure user cannot follow himself
    if follow.user == request.user:
        return JsonResponse({"message": "Impossible to unfollow self"}) 
    
    else:    
        # Handle Follow for author
        follow.followers.remove(user)
        follow.save()

        # Handle following for user
        following.following.remove(follow.user)
        following.save()
        return JsonResponse({"message": "Everything went accordingly"})
    

@login_required
@csrf_exempt
# Create a function to handle post edits and like updates
def edit(request, option, id):
        
    user = request.user 

    # Get post checking if user is author
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # Only give access to edition if request is via PUT
    if request.method == 'PUT':
        # Update database
        # Gather data
        data = json.loads(request.body)
        if option == 'edit':
            body = data.get('body')
            data = json.loads(request.body)
            post.body = body
            post.save()
            return JsonResponse({"message": "Everything went accordingly"})
        
    else:
        if option == 'like':
            post.likes.add(user)
            post.save()
            return JsonResponse({"message": "Everything went accordingly"})
        elif option == 'unlike':
            post.likes.remove(user)
            post.save()
            return JsonResponse({"message": "Everything went accordingly"})
        
        # If anyone tries to access, display the post
        else:
            return JsonResponse(post.serialize(), safe=False)


# Function for seeing posts from whom the author follows
def following(request):

    # Get user
    user = request.user

    # Get user follow model
    following = Follow.objects.get(user__username=user)
    
    # Iterate the followers list
    list = []
    for follow in following.following.all():
        list.append(follow)

    # Get every post made by a person in the following list
    posts = Post.objects.filter(author__username__in=list)
    posts = posts.order_by('-timestamp').all()

    # Handle paginator
    p = Paginator(posts, 10)
    page = request.GET.get('page')
    list = p.get_page(page)

    return render(request, "network/follow.html", {
        'user':user,
        'list':list
    })
        