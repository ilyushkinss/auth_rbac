import jwt

from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rbac.models import Permission
from users.models import User


def get_user_from_request(request):
    """Используется в rbac/views при необходимости; 401 при отсутствии/неверном токене."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationFailed("Authorization header missing")
    try:
        token = auth_header.split()[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return User.objects.get(id=payload["user_id"], is_active=True)
    except (User.DoesNotExist, jwt.InvalidTokenError, IndexError):
        raise AuthenticationFailed("Invalid token")


def check_permission(user, resource, action):
    """403 если у пользователя нет разрешения (resource, action) по правилам RBAC."""
    allowed = Permission.objects.filter(
        rolepermission__role__userrole__user=user,
        resource=resource,
        action=action,
    ).exists()
    if not allowed:
        raise PermissionDenied("Forbidden")


class ArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        check_permission(request.user, "articles", "read")
        return Response({"articles": ["Article 1", "Article 2"]})


class ReportView(APIView):
    """Мок-ресурс: список отчётов (требуется reports:read; только у admin в демо)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        check_permission(request.user, "reports", "read")
        return Response({"reports": ["Report A", "Report B", "Report C"]})
