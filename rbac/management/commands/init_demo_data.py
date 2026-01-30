from django.core.management.base import BaseCommand

from rbac.models import Permission, Role, RolePermission, UserRole
from users.models import User


class Command(BaseCommand):
    help = "Create demo roles, permissions and admin user"

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(name="admin")
        user_role, _ = Role.objects.get_or_create(name="user")

        p_articles_read, _ = Permission.objects.get_or_create(
            resource="articles",
            action="read",
        )
        p_reports_read, _ = Permission.objects.get_or_create(
            resource="reports",
            action="read",
        )
        p_manage, _ = Permission.objects.get_or_create(
            resource="rbac",
            action="manage",
        )

        RolePermission.objects.get_or_create(role=admin_role, permission=p_articles_read)
        RolePermission.objects.get_or_create(role=admin_role, permission=p_reports_read)
        RolePermission.objects.get_or_create(role=admin_role, permission=p_manage)
        RolePermission.objects.get_or_create(role=user_role, permission=p_articles_read)

        admin, created = User.objects.get_or_create(email="admin@test.com")
        if created:
            admin.set_password("admin123")
            admin.save()

        UserRole.objects.get_or_create(user=admin, role=admin_role)

        self.stdout.write(self.style.SUCCESS("Demo data initialized"))
