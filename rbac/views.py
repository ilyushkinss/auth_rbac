from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mock_resources.views import check_permission
from rbac.models import Permission, Role, RolePermission, UserRole
from users.models import User


class RoleListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        check_permission(request.user, "rbac", "manage")

        roles = Role.objects.values("id", "name")
        return Response(list(roles))

    def post(self, request):
        check_permission(request.user, "rbac", "manage")
        role = Role.objects.create(name=request.data["name"])
        return Response({"id": role.id, "name": role.name})


class RoleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, role_id):
        check_permission(request.user, "rbac", "manage")

        role = Role.objects.get(id=role_id)
        return Response({"id": role.id, "name": role.name})

    def patch(self, request, role_id):
        check_permission(request.user, "rbac", "manage")
        role = Role.objects.get(id=role_id)
        if "name" in request.data:
            role.name = request.data["name"]
            role.save()
        return Response({"id": role.id, "name": role.name})

    def delete(self, request, role_id):
        check_permission(request.user, "rbac", "manage")
        Role.objects.filter(id=role_id).delete()
        return Response(status=204)


class AssignRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        check_permission(request.user, "rbac", "manage")

        target_user = User.objects.get(id=user_id)
        role = Role.objects.get(id=request.data["role_id"])

        UserRole.objects.get_or_create(user=target_user, role=role)
        return Response({"status": "role assigned"})


class PermissionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        check_permission(request.user, "rbac", "manage")
        perms = Permission.objects.values("id", "resource", "action")
        return Response(list(perms))

    def post(self, request):
        check_permission(request.user, "rbac", "manage")
        perm = Permission.objects.create(
            resource=request.data["resource"],
            action=request.data["action"],
        )
        return Response({"id": perm.id, "resource": perm.resource, "action": perm.action})


class RolePermissionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, role_id):
        check_permission(request.user, "rbac", "manage")

        perms = Permission.objects.filter(
            rolepermission__role_id=role_id
        ).values("id", "resource", "action")
        return Response(list(perms))


class RolePermissionAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, role_id):
        check_permission(request.user, "rbac", "manage")

        role = Role.objects.get(id=role_id)
        perm = Permission.objects.get(id=request.data["permission_id"])
        RolePermission.objects.get_or_create(role=role, permission=perm)
        return Response({"status": "permission added to role"})


class RolePermissionRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, role_id, permission_id):
        check_permission(request.user, "rbac", "manage")

        RolePermission.objects.filter(role_id=role_id, permission_id=permission_id).delete()
        return Response(status=204)
