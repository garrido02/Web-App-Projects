import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Message, Pack, Team


def index(request):
    user = request.user
    team = Team.objects.all()
    pack = Pack.objects.all()
    return render(request, "finalproject/index.html", {
        'user':user,
        'team':team,
        'pack':pack
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
            return render(request, "finalproject/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "finalproject/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        nickname = request.POST["nickname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "finalproject/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user.nickname = nickname
            user.save()
        except IntegrityError:
            return render(request, "finalproject/register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "finalproject/register.html")


# Function to handle ticket requests 
@csrf_exempt
def ticket(request):

    if request.method == "POST":
        # Get Data
        author = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        body = request.POST.get("message")
        
        # Create Message
        message = Message()
        message.author = author
        message.email = email
        message.subject = subject
        message.body = body
        message.save()

        return redirect(index)

    
    if request.method == "GET":
        messages = Message.objects.all()
        messages = messages.order_by('-timestamp').all()
        return JsonResponse([message.serialize() for message in messages], safe=False)
    
    else:
        return JsonResponse({"error": "Request must be POST or GET"})


# Function to handle profile visit
@login_required
def profile(request):

    # Get user
    user = User.objects.get(username=request.user)

    if user.username != "admin":
        # Get Messages
        message = Message.objects.filter(author=request.user)
        message = message.order_by('-timestamp').all()

        return render(request, "finalproject/profile.html", {
            'user': user,
            'message': message
        })
    
    else:
        message = Message.objects.filter(solved=False)
        message = message.order_by('-timestamp').all()

        return render(request, "finalproject/profile.html", {
            'user': user,
            'message': message
        })


@login_required
@csrf_exempt
def change_nick(request, user):

    if request.method == "PUT":
        # Get user and data
        u = User.objects.get(username=user)
        data = json.loads(request.body)
        u.nickname = data["nickname"]
        u.save()
        return JsonResponse({"message": "Nickname changed."})

    else:
        return JsonResponse({"error": "Only accessible via PUT"}, status=404)


@login_required
def support(request, id):
    if request.method == "GET":
        message = Message.objects.get(id=id)
        return render(request, "finalproject/ticket.html", {
            'message': message,
            'user': request.user
        })


@csrf_exempt
@login_required
def close(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        message = Message.objects.get(id=id)
        message.solved = True
        message.save()

        return JsonResponse({"Ticket Closed"})

    else:
        return JsonResponse({"error": "Only accessible via PUT"}, status=404)


def pacote(request, short):
    pack = Pack.objects.get(short=short)
    return render(request, "finalproject/pacotes.html", {
    'pack': pack,
    'user': request.user
})

@login_required
@csrf_exempt
def change_pass(request, user):

    if request.method == "PUT":
        # Get user and data
        u = User.objects.get(username=user)
        data = json.loads(request.body)
        u.set_password(data["password"])
        update_session_auth_hash(request, request.user)
        u.save()
        user = authenticate(request, username=user, password=data["password"])
        return render(request, 'finalproject/index.html')