from django.urls import include, path

urlpatterns = [
    path("api/users/", include("users.urls")),
    path("api/", include("mock_resources.urls")),
    path("api/admin/", include("rbac.urls")),
]
