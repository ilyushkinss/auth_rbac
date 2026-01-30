import jwt

from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import User


def generate_token(user):
    return jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        password_confirm = request.data.get("password_confirm")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        patronymic = request.data.get("patronymic", "")

        if not email or not password:
            raise ValidationError("email и password обязательны")
        if password != password_confirm:
            raise ValidationError("Пароль и повтор пароля не совпадают")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")

        User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )
        return Response({"status": "registered"})


class LoginView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data.get("email")).first()

        if not user or not user.check_password(request.data.get("password", "")):
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise AuthenticationFailed("Учетная запись деактивирована")

        return Response({"token": generate_token(user)})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"detail": "Вы успешно вышли из системы"},
            status=200,
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "patronymic": user.patronymic,
        })

    def patch(self, request):
        user = request.user
        for field in ("first_name", "last_name", "patronymic", "email"):
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()
        return Response({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "patronymic": user.patronymic,
        })


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"detail": "Аккаунт деактивирован. Вход больше невозможен."},
            status=200,
        )
