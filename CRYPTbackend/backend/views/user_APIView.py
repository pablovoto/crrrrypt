from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from backend.models import CustomUser
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
#Clases Serializer


class GetUserInfoAPI(APIView):  
    #Esta clase es para obtener la información de un usuario
    permission_classes = [AllowAny]
    
    class OutputSerializer(serializers.ModelSerializer):
    
        class Meta:
            model=CustomUser
            fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']


    def get(self, request, format=None):
        user = CustomUser.objects.all()
        
        #get query parameters
        username = request.query_params.get('username')
        is_active = request.query_params.get('is_active')
        
        #filter clients based on query parameters
        if username is not None:
            user = user.filter(username__icontains=username)
        if is_active is not None:
            user = user.filter(is_active=is_active)
        
        serializer = self.OutputSerializer(user, many=True)
        return Response({"data": serializer.data})
    
class CreateUserInfoAPI(APIView):   
    #Esta clase es para crear o modificar un usuario
    permission_classes = [AllowAny]
    class InputSerializer(serializers.ModelSerializer):          #Estos campos pueden variar con respecto a los del output
        class Meta:
            model=CustomUser
            fields = ['username', 'email', 'first_name', 'last_name', 'is_active','password']


    def post(self, request, format=None):  
        #Esta función es para crear un usuario
        serializer = self.InputSerializer(data=request.data)
        password = request.data.get('password')
        request.data['password'] = make_password(password)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, user_id, format=None):
        #Esta función es para modificar un usuario
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.InputSerializer(user, data=request.data)
        password = request.data.get('password')
        request.data['password'] = make_password(password)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
