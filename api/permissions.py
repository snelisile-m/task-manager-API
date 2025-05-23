from rest_framework import permissions

class IsAdminOrAssignedUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        return obj.assigned_to == request.user
