from rest_framework.permissions import BasePermission


class AnonlistAndUpdateOwnerOnlyAndAuthRetrieve(BasePermission):

    """
    Custom permission:
        - allow anonymous GET
        - allow authenticated POST
        - allow PUT for record owner
        - allow all actions for staff
    """
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action in ['create','retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):

        if view.action in 'retrieve':
            return True
        elif view.action in ['update', 'partial_update','destroy']:
            return obj.owner == request.user or request.user.is_admin
        else:
            return False

