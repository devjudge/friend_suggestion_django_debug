from django.urls import path
from .views import (register_user,
                    add_friend,
                    recieved_request,
                    current_friends,
                    friends_suggestions)

urlpatterns =[
    path("create", register_user, name="new_user"),
    path("add/<str:userA>/<str:userB>", add_friend, name="add_friend"),
    path("friendRequests/<str:user>", recieved_request, name="recieved_request"),
    path("friends/<str:user>", current_friends, name="current_friends"),
    path("suggestions/<str:user>", friends_suggestions, name="friends_suggestions"),
]