from django.contrib.auth.models import User


class AuthTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.META.get('HTTP_TOKEN')
        if token:
            try:
                user = User.objects.get(userprofile__auth_token=token)
                request.user = user
            except User.DoesNotExist:
                pass
        response = self.get_response(request)

        return response