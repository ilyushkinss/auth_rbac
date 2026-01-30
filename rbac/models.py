from django.db import models

from users.models import User


class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Permission(models.Model):
    resource = models.CharField(max_length=50)
    action = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.resource}:{self.action}"


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
