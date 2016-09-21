import urllib

from core.models import Message, UserProfile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse


@login_required
def get_messages(request):
    """Returns last n messages for specific user"""
    user = request.user
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
def create_messages(request):
    """Returns last n messages for specific user"""
    user = request.user
    response = {'status': 'ok'}

    if not user.userprofile.verify_has_bro(request.POST['broId']):
        response['status'] = 'error'
        response['message'] = 'You don\'t have this bro'
        return JsonResponse(response)

    # Create the new messaged
    receiver = UserProfile.objects.get(pk=request.POST['receiverId'])
    message = Message.objects.create(
        sender=user.userprofile,
        receiver=receiver,
        bro_id=request.POST['broId'],
    )

    response['message_id'] = message.id

    # Check if the user got new BroType!
    new_bro_type = user.userprofile.has_new_bro_type()
    if new_bro_type:
        user.userprofile.bros.add(new_bro_type)
        user.save()
        response['newBroType'] = new_bro_type.to_dict()
    return JsonResponse(response)


@login_required
def get_bros(request):
    """Returns bros that the current user have"""
    user = request.user
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
    response = {'status', 'ok'}
    user = request.user
    try:
        fb_data = user.userprofile.get_fb_user_data()
    except ValidationError:
        # TODO email admin?
        response['status'] = 'error'
        return response
    except urllib.error.HTTPError:
        response['status'] = 'error'
        return response

    # Set new token and update facebook details
    token = user.userprofile.set_new_auth_token()
    user.first_name = fb_data['first_name']
    user.last_name = fb_data['last_name']
    user.userprofile.fb_user_id = fb_data['user_id']
    user.save()
    user.userprofile.save()

    response['token'] = token
    return response


def check_version(request):
    """
    Check the current user app version against the server version.
    We can use this to force update for users.
    """
    pass