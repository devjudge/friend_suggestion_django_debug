# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .serializer import serializer_register
from .models import friend_suggestor
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def register_user(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        data_serialize = serializer_register(data=data)

        if data_serialize.is_valid():
            data_serialize.save()
            user = friend_suggestor.objects.get(username=data_serialize.data['username'])
            user.friends = '[]'
            user.friend_request = '[]'
            user.request_pending = '[]'
            user.save()

            return JsonResponse(data_serialize.data, status=status.HTTP_201_CREATED)

        return JsonResponse({"status": "failure",
                             "reason": data_serialize.errors}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def add_friend(request, userA, userB):

    if userA == userB:
        return JsonResponse({"status": "failure",
                             "reason": "Both username are same"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from_friend = friend_suggestor.objects.get(username=userA)
        to_friend = friend_suggestor.objects.get(username=userB)

    except friend_suggestor.DoesNotExist:
        return JsonResponse({"status": "failure",
                             "reason": "One of the specified user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        to_current_friends = eval(to_friend.friends)
        to_send_request = eval(to_friend.request_pending)
        to_received_request = eval(to_friend.friend_request)
        from_current_friends = eval(from_friend.friends)
        from_send_request = eval(from_friend.request_pending)
        from_received_request = eval(from_friend.friend_request)

        if to_friend.username in from_received_request:

            to_current_friends.append(from_friend.username)
            from_current_friends.append(to_friend.username)
            from_received_request.remove(to_friend.username)
            to_send_request.remove(from_friend.username)
            to_friend.friends = str(to_current_friends)
            from_friend.friends = str(from_current_friends)
            from_friend.friend_request = str(from_received_request)
            to_friend.request_pending = str(to_send_request)
            from_friend.save()
            to_friend.save()
            return JsonResponse({"status": "success"}, status=status.HTTP_202_ACCEPTED)
        elif to_friend.username in from_send_request:
            return JsonResponse({"status": "failure",
                                 "reason": "Request already send"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            from_send_request.append(to_friend.username)
            to_received_request.append(from_friend.username)
            from_friend.request_pending = str(from_send_request)
            to_friend.friend_request = str(to_received_request)
            from_friend.save()
            to_friend.save()

            return JsonResponse({"status": "success"}, status=status.HTTP_202_ACCEPTED)


@csrf_exempt
def recieved_request(request, user):

    try:
        user = friend_suggestor.objects.get(username=user)
    except friend_suggestor.DoesNotExist:
        return JsonResponse({"status": "failure",
                             "reason": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        user_pending = eval(user.friend_request)

        if not user_pending:
            return JsonResponse({"status": "failure",
                                 "reason": "No pending Friends Requests"}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({"friend_requests": user_pending}, status=status.HTTP_200_OK)


@csrf_exempt
def current_friends(request, user):

    try:
        user = friend_suggestor.objects.get(username=user)

    except friend_suggestor.DoesNotExist:
        return JsonResponse({"status": "failure",
                             "reason": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        cur_user = eval(user.friends)

        if not cur_user:
            return JsonResponse({"status": "failure",
                                 "reason": "No Friends"}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({"friends": cur_user}, status=status.HTTP_200_OK)


@csrf_exempt
def friends_suggestions(request, user):

    try:
        user = friend_suggestor.objects.get(username=user)
    except friend_suggestor.DoesNotExist:
        return JsonResponse({"status": "failure",
                             "reason": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        suggestions = set(())
        for friend in eval(user.friends):
            try:
                suggest = friend_suggestor.objects.get(username=friend)
                suggestions = suggestions.union(set(eval(suggest.friends)))
            except friend_suggestor.DoesNotExist:
                return JsonResponse({"status": "failure",
                                     "reason": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            if friend in suggestions:
                suggestions.discard(friend)

        suggestions.discard(user.username)
        for suggest in list(suggestions):
            if suggest in user.friends:
                suggestions.discard(suggest)
        print("Suggestions are : {suggestions}")
        return JsonResponse({"suggestions": list(suggestions)}, status=status.HTTP_200_OK)
