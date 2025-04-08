from rest_framework.permissions import BasePermission

class IsStaffOrReadOnly(BasePermission):
    """
    Custom permission to allow staff users to edit, others can only read.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff
