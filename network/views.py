from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import *
from .forms import *


def index(request):

    # I always want the ability to add a new post on the index/all posts page if a user is logged in

    # get all posts and send to index page
    posts = Post.objects.all().order_by('-date')
    post_form = NewPostForm()


    paginator = Paginator(posts, 20) # shows 10 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        'post_form' : post_form,
        'page_obj' : page_obj,
        'edit_post_form' : EditPostForm()
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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def new_post(request):
    
    if request.method == "POST":

        post_form = NewPostForm(request.POST)

        if post_form.is_valid():

            content = post_form.cleaned_data['content']
            user = request.user
            new_post = Post.objects.create(user=user,content=content)
            new_post.save()

            return HttpResponseRedirect(reverse("index"))
        else: return JsonResponse ({'error':"Cannot submit blank post. Please try again."}, status=400)

    else: return JsonResponse ({'error':"Cannot submit get request. Please try again."}, status=400)


# Display users profile page
def profile_page(request, username):
    # Get the user who's page we're on
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'This user does not exist'}, status=400)
    # Get the following list of the requesting user
    
    request_user_following, created = UserFollowing.objects.get_or_create(user=user)
    
    if created == False:
        user_following = request_user_following.following
        user_followers = request_user_following.followers
    else:
        user_following = None
        user_followers = None

    # Get all posts by the profile user
    users_posts = Post.objects.filter(user=user).order_by('-date')
    paginator = Paginator(users_posts, 10) # shows 10 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "user": user,
        "user_followers":user_followers,
        "user_following":user_following,
        "post_form":NewPostForm(),
        "users_posts":users_posts,
        'page_obj': page_obj,
    })


# Display page of posts from users that the requesting user is following
@login_required
def following_page(request):
    # Get the users that the requesting user is following.
    users_follows, created = UserFollowing.objects.get_or_create(user=request.user)
    user_following = users_follows.following.all()
    # Get all their post
    user_following_posts = []
    for follower in user_following:
        follower_posts = Post.objects.filter(user=follower).order_by('-date')
        for post in follower_posts:
            user_following_posts.append(post)
    
    paginator = Paginator(user_following_posts, 10) # shows 10 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Return posts to following page
    return render(request, "network/following.html", {

        "user_following":user_following,
        "all":UserFollowing.objects.all(),
        "post_form":NewPostForm(),
        'page_obj': page_obj,
    })


@csrf_exempt
@login_required
def update_likes(request):

    #post requests only?
    if request.method != 'POST':

        # Get the list of likes for a certain post
        post_id = request.GET.get('id')
        post = Post.objects.get(id=post_id)
        liked_list = post.liked_users

        return JsonResponse({'success': {'liked_list': liked_list}}, status=200)

    data = json.loads(request.body)

    post_id = data.get('id')
    post = Post.objects.get(id=int(post_id))
    liked_list = post.liked_users

    #find out if the username that clicked on the button is in the liked_list or not

    requesting_username = data.get('username')
    
    try:
        requesting_user = User.objects.get(username=requesting_username.casefold())
    except User.DoesNotExist:
        return JsonResponse({'error':'User does not exist.'}, status=400)
    
    if requesting_user in liked_list.all():
        liked_list.remove(requesting_user)
        post.save()
        return JsonResponse({'success':'Like removed'}, status=200)
    else:
        #Get user model instance and add to post likes
        post.liked_users.add(requesting_user)
        post.save()
        return JsonResponse({'success':'Like added'}, status=200)
        

# View for following and unfollowing users
@csrf_exempt 
@login_required
def follow(request):

    if request.method != 'POST':
        return JsonResponse({'error':'Please send a POST request'}, status=400)

    data = json.loads(request.body)
    requesting_username = data.get('requesting_username')
    requested_username = data.get('requested_username')

    try:
        requested_user = User.objects.get(username=requested_username.casefold())
    except User.DoesNotExist:
        return JsonResponse({'error':'User does not exist.1' , 'username':requested_username.casefold()}, status=400)
    try:
        requesting_user = User.objects.get(username=requesting_username.casefold())
    except User.DoesNotExist:
        return JsonResponse({'error':'User does not exist.2', 'username':requesting_username.casefold()}, status=400)

    # Get following list of the requesting user
    requesting_user_following_list, new_requesting_user_following_list = UserFollowing.objects.get_or_create(user=requesting_user)
    requested_user_following_list, new_requested_user_following_list = UserFollowing.objects.get_or_create(user=requested_user)

    if new_requesting_user_following_list != None or new_requested_user_following_list != None:

        if requested_user in requesting_user_following_list.following.all():
            #remove the requested user
            requesting_user_following_list.following.remove(requested_user)
            requesting_user_following_list.save()
            requested_user_following_list.followers.remove(requesting_user)
            requested_user_following_list.save()
            return JsonResponse({'success':'User unfollowed'}, status=200)
        else:
            #add the requested user
            requesting_user_following_list.following.add(requested_user)
            requesting_user_following_list.save()
            requested_user_following_list.followers.add(requesting_user)
            requested_user_following_list.save()
            return JsonResponse({'success':'User followed'}, status=200)

    else:
            #add the requested user
            requesting_user_following_list.following.add(requested_user)
            requesting_user_following_list.save()
            requested_user_following_list.followers.add(requesting_user)
            requested_user_following_list.save()
            return JsonResponse({'success':'User followed'}, status=200)


@csrf_exempt
@login_required
def edit_post(request):

    if request.method != "PUT":

        return JsonResponse ({'error':"Cannot submit request."}, status=400)
    else:
        data = json.loads(request.body)
        new_content = data.get('new_content')
        post_id = data.get('post_id')


        post = Post.objects.get(id=post_id)
        post.content = new_content
        post.save()

        # return HttpResponseRedirect(reverse("index"))
        return JsonResponse({'succes':"Post updated."}, status=200)
        # else: return JsonResponse ({'error':"Cannot submit blank post. Please try again."}, status=400)
