from rest_framework.permissions import IsAuthenticated


class IsClientManagerRelationshipAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.has_perm("directory.administrate_clientmanagerrelationship")
