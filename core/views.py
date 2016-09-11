from core.models import Message
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse


@login_required
def get_messages(request):
    """Returns last n messages for specific user"""
    user = request.user  # TODO make sure the user is token authnticated
    page = request.GET.get('page', 1)
    paginator = Paginator(Message.objects.filter(receiver=user.userprofile), 40)

    response = {
        'status': 'ok',
        'messages': [m.to_dict() for m in paginator.page(page).object_list],
        'totalPages': paginator.num_pages,
        'totalMessages': paginator.count,
    }

    return JsonResponse(response)


@login_required
def get_bros(request):
    """Returns bros that the current user have"""
    user = request.user  # TODO make sure the user is token authnticated
    bros = user.userprofile.bros.all()

    response = {
        'status': 'ok',
        'bros': [bro.to_dict() for bro in bros],
    }

    return JsonResponse(response)


@login_required
def get_dashboard(request):
    """Returns all the data for the dashboard"""
    user = request.user
    response = {
        'totalMessages': Message.objects.filter(receiver=user).count(),
        'totalMessagesToday': Message.get_messages_from_last_day().filter(receiver=user).count(),
        'totalMessagesLastWeek': Message.get_messages_from_last_week().filter(receiver=user).count(),
        'totalBros': user.userprofile.bros.count(),
    }

    return JsonResponse(response)


def login(request):
    """
    Login a user with a user auth token
    """
    username = request.POST['username']
    password = request.POST['password']
    response = {'status', 'ok'}

    # Check the username and password, could be a facebook token also
    user = authenticate(username=username, password=password)

    if user:
        if not user.userprofile.auth_token:
            user.userprofile.set_new_auth_token()
            user.save()

        response['token'] = user.userprofile.auth_token
    else:
        response['status'] = 'error'
        response['message'] = 'Invalid login credentials'
        return response


def check_version(request):
    """
    Check the current user app version against the server version.
    We can use this to force update for users.
    """
    pass