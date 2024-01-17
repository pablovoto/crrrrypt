from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response({"detail": "Logout successful"})
