from core.models import Message
from django.core.paginator import Paginator
from django.http import JsonResponse


def get_messages(request):
    """Returns last n messages for specific user"""
    user = request.user  # TODO make sure the user is token authnticated
    page = request.GET.get('page', 1)
    paginator = Paginator(Message.objects.filter(receiver=user), 40)

    response = {
        'status': 'ok',
        'messages': [m.to_dict() for m in paginator.page(page).object_list],
        'totalPages': paginator.num_pages,
        'totalMessages': paginator.count,
    }

    return JsonResponse(response)


def get_bros(request):
    """Returns bros that the current user have"""
    user = request.user  # TODO make sure the user is token authnticated
    bros = user.userprofile.bros.all()

    response = {
        'status': 'ok',
        'bros': [bro.to_dict() for bro in bros],
    }

    return JsonResponse(response)


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
