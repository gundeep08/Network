import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Likes, Follow, Following, Messages
   
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

#Add new Post from the logged in user.
def addPost(request):
    if request.method == "POST":
        content = request.POST["postcontent"]
        scope= request.POST["scope"]
        createPost=Post(content= content, owner=request.user, scope=scope) 
        createPost.save() 
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/addpost.html")
    

# Pull all the Posts from Post Model in reverse chronological format and also pull all the likes for that post from Likes Model.
def index(request):
    isSignedIn=False
    if request.user.is_authenticated:
        isSignedIn=True   
    posts=Post.objects.order_by("-creation_time").all()
    likeMap=likeCounts(posts)
    celebrityUsers=celebrities(posts)
    finalPostList=[]
    #Filter posts based on the scope
    finalPostList= filterPosts(posts,isSignedIn, request.user)  
    # Implement Pagination
    page_obj = pagination(finalPostList, request)
    return render(request, "network/index.html", {
        "posts": page_obj,
        "likes":likeMap,
        "isSignedIn": isSignedIn,
        "celebrityList":celebrityUsers
    })
    
#Filter posts based on the scope
def filterPosts(posts, isSignedIn, user):
    finalPostList=[] 
    for post in posts:
        if post.scope == "all":
            finalPostList.append(post)
        elif isSignedIn and post.owner == user:
            finalPostList.append(post)
        elif isSignedIn and post.scope == "followings" and Follow.objects.filter(follower=post.owner, following=user).count()>0: 
            finalPostList.append(post)
        elif isSignedIn and post.scope == "followers" and Follow.objects.filter(follower=user, following=post.owner).count()>0: 
            finalPostList.append(post)
    return finalPostList
 
 # Implement Pagination   
def pagination(finalPostList,request):
    paginator = Paginator(finalPostList, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

#Populate The Dictionary object for likes for each post
def likeCounts(posts):
    likeMap={}
    for post in posts:
        likeMap[post.id]=Likes.objects.filter(post=post, like=True).all().count()
    return likeMap

#Populate The List of Celebrity Users 
def celebrities(posts):
    celebrityUsers=[]
    for post in posts:
        if Follow.objects.filter(following=post.owner).count()>10 and post.owner not in celebrityUsers:
            celebrityUsers.append(post.owner)
    return celebrityUsers
    
#Pull all the Posts with its details specific for the requested user and allow the current user to follow/unfollow it.
def profile(request, user_id):
    isSignedIn=False
    if request.user.is_authenticated:
        isSignedIn=True 
    finalPostList=[]
    user= get_object_or_404(User, pk=user_id)
    posts=Post.objects.filter(owner=user).order_by("-creation_time").all()
    finalPostList= filterPosts(posts,isSignedIn, request.user) 
    page_obj = pagination(finalPostList, request)
    if request.user.is_authenticated:
        isItFollower=Follow.objects.filter(follower=request.user, following=user).exists()
    else:
        isItFollower=False
    return render(request, "network/profile.html", {
        "followers": Follow.objects.filter(following=user).all().count(),
        "follows": Follow.objects.filter(follower=user).all().count(),
        "alreadyFollows": isItFollower,
        "posts": page_obj,
        "postOwnerId":user_id
    })
    
# Details for Followers page, for listing and descrbing follower users of each user.    
def followersDetails(request, postOwnerId):
    followerDetails=[]
    followings= Following.objects.filter(followingId=postOwnerId).all()
    for following in followings:
        eachFollower={}
        user=get_object_or_404(User, pk=following.followerId)
        eachFollower["username"]=user.username
        eachFollower["postCount"]=Post.objects.filter(owner=user).count()
        eachFollower["followers"]=Follow.objects.filter(following=user).all().count()
        eachFollower["following"]=Follow.objects.filter(follower=user).all().count()  
        followerDetails.append(eachFollower)
    return render(request, "network/followerDetails.html", {
        "followersList": followerDetails,
        "postOwnerId":postOwnerId
    })
   
# Details for Follows page, for listing and descrbing users that current user follows.     
def followingDetails(request, postOwnerId):
    followingDetails=[]
    followers= Following.objects.filter(followerId=postOwnerId).all()
    for follower in followers:
        eachFollowing={}
        user=get_object_or_404(User, pk=follower.followingId)
        eachFollowing["username"]=user.username
        eachFollowing["postCount"]=Post.objects.filter(owner=user).count()
        eachFollowing["followers"]=Follow.objects.filter(following=user).all().count()
        eachFollowing["following"]=Follow.objects.filter(follower=user).all().count()  
        followingDetails.append(eachFollowing)
    return render(request, "network/followingDetails.html", {
        "followingDetails": followingDetails,
        "postOwnerId":postOwnerId
    })
    
#Pull all the Posts from all the users that the current user follows.
def following(request):
    posts={}
    isSignedIn=False
    if request.user.is_authenticated:
        isSignedIn=True 
    followings= Following.objects.filter(followerId=request.user.id).all()
    for following in followings:
        user=get_object_or_404(User, pk=following.followingId)
        if posts:
           tempPost= Post.objects.filter(owner=user).order_by("-creation_time").all()
           posts.union(tempPost)
           posts = posts | tempPost
        else:
            posts=Post.objects.filter(owner=user).order_by("-creation_time").all()
    likeMap=likeCounts(posts)
    celebrityUsers=celebrities(posts)
    page_obj = pagination(posts, request)
    return render(request, "network/index.html", {
        "posts": page_obj,
        "likes":likeMap,
        "isSignedIn": isSignedIn,
        "celebrityList":celebrityUsers
    })
        
     

#Allow user to edit his post by prepopulating the post content in textarea and allowing him/her to edit and save it.
def edit(request, post_id):
    if request.method == "POST":
        updatedContent = request.POST["postcontent"]
        updatedScope = request.POST["scope"]
        post=get_object_or_404(Post, pk=post_id)
        post.content=updatedContent
        post.scope=updatedScope
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        post=get_object_or_404(Post, pk=post_id)
        return render(request, "network/edit.html", {
            "post": post,
            "id": post_id
        })
        
#Allow user to repost other user's post by using the same post content and allowing user to change the visibility of post but cannot change the content of post.
def repost(request, post_id):
    if request.method == "POST":
        scope = request.POST["scope"]
        post=get_object_or_404(Post, pk=post_id)
        createPost=Post(content= post.content, owner=request.user, scope=scope) 
        createPost.save() 
        return HttpResponseRedirect(reverse("index"))
    else:
        post=get_object_or_404(Post, pk=post_id)
        return render(request, "network/repost.html", {
            "post": post,
            "id": post_id
        })

#Allow current user to follow another user.
@csrf_exempt
def follows(request, postOwnerId):
    follower= get_object_or_404(User, pk=request.user.id)
    postOwner= get_object_or_404(User, pk=postOwnerId)
    follow= Follow()
    follow.save()
    follow.follower.add(follower)
    follow.following.add(postOwner)
    following=Following(followerId=request.user.id, followingId=postOwnerId)
    following.save()
    return HttpResponse("Successfully Following")

#Allow current user to unfollow another user that he/she is currently following.
def unfollow(request, postOwnerId):
    follower= get_object_or_404(User, pk=request.user.id)
    postOwner= get_object_or_404(User, pk=postOwnerId)
    follow= Follow.objects.filter(follower=request.user, following=postOwner).all()
    follow.delete()
    following= Following.objects.filter(followerId=request.user.id, followingId=postOwnerId).all()
    following.delete()
    return HttpResponse("Successfully UnFollowed")

#Allow any user, even the post owner to like a post and can click the same button again to unlike it. One user can like a particular post only once, clicking it again will toggle it and be treated as unlike.
@csrf_exempt
def manageLike(request, postId):
    postLikes= get_object_or_404(Post, pk=postId)
    likes= Likes.objects.filter(user=request.user, post=postLikes).all()
    if likes:
        likes.delete()
        return HttpResponse("delete")
    else:
        addLike=Likes(like=True, user=request.user, post=postLikes) 
        addLike.save() 
        return HttpResponse("add")
    
#Load the requested Messages box inbox/sent. 
def messages(request, messageType):
    if messageType == "inbox":
        messages = Messages.objects.filter(recipient=request.user)
    elif messageType == "sent":
        messages = Messages.objects.filter(sender=request.user)
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)
    # Return messages in reverse chronologial order
    messages = messages.order_by("-creation_time").all()
    return JsonResponse([message.serialize() for message in messages], safe=False)
    
#Load the Message home page  
def message(request):
    return render(request, "network/message.html")

# Search Functionality to search post from a particular user or/and based on date frame.
def search(request):
    isSignedIn=False
    if request.user.is_authenticated:
        isSignedIn=True  
    user=None
    finalPostList=[] 
    filteredPosts=[]
    celebrityUsers=[]
    if request.method != "POST":
        return render(request, "network/search.html")
    else:
        username=request.POST["username"]
        fromDate=request.POST["fromDate"]
        toDate=request.POST["toDate"]
        if username and username!="":
            user= get_object_or_404(User, username=username)
        if user and user!="":
            posts=Post.objects.filter(owner=user).order_by("-creation_time").all()
        else:
            posts=Post.objects.order_by("-creation_time").all()
        for post in posts: 
            if fromDate and fromDate !="":
                if compareDates(post.creation_time.strftime("%Y/%m/%d").split("/"), fromDate.split("-"))=="Greater":
                    filteredPosts.append(post)
            if toDate and toDate !="":
                if compareDates(post.creation_time.strftime("%Y/%m/%d").split("/"), toDate.split("-"))=="Smaller": 
                    if post not in filteredPosts:
                        filteredPosts.append(post)
                else:
                    filteredPosts.remove(post)
            else:
                filteredPosts.append(post)
    likeMap=likeCounts(filteredPosts)
    celebrityUsers=celebrities(filteredPosts)
    #Filter posts based on the scope
    finalPostList= filterPosts(filteredPosts,isSignedIn, request.user)  
    # Implement Pagination
    page_obj = pagination(finalPostList, request)                     
    
    return render(request, "network/index.html", {
        "posts": page_obj,
        "likes":likeMap,
        "isSignedIn": isSignedIn,
        "celebrityList":celebrityUsers
    })
            
#Send Messages Successfully
@csrf_exempt
def sendmessages(request):
    # Composing a new message must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    # Check if recipient user exists
    data = json.loads(request.body)
    try:
        user = User.objects.get(username=data.get("recipient"))
    except User.DoesNotExist:
        return JsonResponse({
            "error": f"User with username {email} does not exist."
        }, status=400)     
    # Get recipient username
    recipient= data.get("recipient", "")
    # Get contents of message
    body = data.get("body", "")
    message = Messages(
        recipient=recipient,
        sender=request.user,
        content=body,
        read=False,
        )
    message.save()
    return JsonResponse({"message": "Email sent successfully."}, status=201)

@csrf_exempt
def messagecontent(request, message_id):
    # Query for requested message
    try:
        message = Messages.objects.get(pk=message_id)
        message.read=True
        message.save()
    except Messages.DoesNotExist:
        return JsonResponse({"error": "Message not found."}, status=404)
    # Return message contents
    if request.method == "GET":
        return JsonResponse(message.serialize())
    
# Compare dates for Search Functionality 
def compareDates(postCreationDate, requestedDate):
    if postCreationDate[0]==requestedDate[0]:
        if postCreationDate[1]==requestedDate[1]:
            if postCreationDate[2]==requestedDate[2]:
                return "Equal"
            else:
                return compare(postCreationDate[2],requestedDate[2])
        else:
            return compare(postCreationDate[1],requestedDate[1])   
    else:
        return compare(postCreationDate[0],requestedDate[0])
        
# Compare dates sub sections of days/months/year for Search Functionality   
def compare(source, target):
    if source>target:
        return "Greater"
    elif source<target: 
        return "Smaller" 
    else:
        return "Equal" 
        
        



