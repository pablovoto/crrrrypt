from rest_framework.permissions import BasePermission

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        # Solo permitir el acceso si el usuario es del tipo Company
        print("User:", request.user)  # Print the user
        print("Has client:", hasattr(request.user, 'client'))  # Print whether the user has a user_company attribute
        #imprime por pantalla el valor del atributo id
        print("ID:", request.user.id)
        if request.user.is_authenticated and hasattr(request.user, 'client'):
            print("Es un cliente")
            return True
        else:
            return False