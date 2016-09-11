from django.contrib.auth.models import User


class TokenAuthBackend:
    def authenticate(self, token=None):
        if not token:
            return None

        try:
            return User.objects.get(userprofile__auth_token=token)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None