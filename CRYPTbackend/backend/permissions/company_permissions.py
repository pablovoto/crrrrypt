from rest_framework.permissions import BasePermission

class IsCompanyUser(BasePermission):
    def has_permission(self, request, view):
        # Solo permitir el acceso si el usuario es del tipo Company
        print("User:", request.user)  # Print the user
        print("Has user_company:", hasattr(request.user, 'company'))  # Print whether the user has a user_company attribute
        #imprime por pantalla el valor del atributo company
        print("Company:", request.user.company)
        if request.user.is_authenticated and hasattr(request.user, 'company'):
            print("Es una empresa")
            return True
        else:
            return False