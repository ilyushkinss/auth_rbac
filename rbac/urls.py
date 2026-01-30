from django.urls import path

from .views import (
    AssignRoleView,
    PermissionListCreateView,
    RoleDetailView,
    RoleListCreateView,
    RolePermissionAddView,
    RolePermissionListView,
    RolePermissionRemoveView,
)

urlpatterns = [
    path("roles/", RoleListCreateView.as_view()),
    path("roles/<int:role_id>/", RoleDetailView.as_view()),
    path("roles/<int:role_id>/permissions/", RolePermissionListView.as_view()),
    path("roles/<int:role_id>/permissions/add/", RolePermissionAddView.as_view()),
    path("roles/<int:role_id>/permissions/<int:permission_id>/", RolePermissionRemoveView.as_view()),
    path("permissions/", PermissionListCreateView.as_view()),
    path("users/<int:user_id>/roles/", AssignRoleView.as_view()),
]
