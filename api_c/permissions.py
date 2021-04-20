from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
        

class IsProfessor(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_professor == True


class IsStudent(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_student == True