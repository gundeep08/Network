
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addPost", views.addPost, name="addPost"),
    path("search", views.search, name="search"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("follow/<int:postOwnerId>", views.follows, name="follows"),
    path("unfollow/<int:postOwnerId>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("messages/<str:messageType>", views.messages, name="messages"),
    path("messagecontent/<int:message_id>", views.messagecontent, name="messagecontent"),
    path("message", views.message, name="message"),
    path("sendmessage", views.sendmessages, name="sendmessages"),
    path("manageLike/<int:postId>", views.manageLike, name="manageLike"),
    path("followersDetails/<int:postOwnerId>", views.followersDetails, name="followersDetails"),
    path("followingDetails/<int:postOwnerId>", views.followingDetails, name="followingDetails"),
    path("repost/<int:post_id>", views.repost, name="repost")
]
