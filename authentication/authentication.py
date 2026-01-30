import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """
    Собственная аутентификация по JWT в заголовке Authorization: Bearer <token>.
    Позволяет идентифицировать пользователя при последующих запросах после login.
    """

    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith(self.keyword + " "):
            return None

        token = auth_header[len(self.keyword) + 1 :].strip()
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                raise AuthenticationFailed("Invalid token")
            user = User.objects.get(id=user_id, is_active=True)
            return (user, token)
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found or inactive")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
