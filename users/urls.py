from django.urls import path

from .views import (
    DeleteAccountView,
    LoginView,
    LogoutView,
    ProfileView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view()),
    path("delete-account/", DeleteAccountView.as_view()),
]
