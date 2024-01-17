from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from backend.models import CustomUser, Client, Company
from django.shortcuts import get_object_or_404





class GetClientInfoAPI(APIView):  
    #Esta clase es para obtener la información de un cliente
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]               

    
    class OutputSerializer(serializers.ModelSerializer):
        username = serializers.SerializerMethodField()
        
        class Meta:
            model = Client
            fields = ['id', 'username','teacher','company','type']
        def get_username(self, obj):
            return obj.user_client.username
    
    def get(self, request, format=None):
        try:
            company = Company.objects.get(user_company=request.user)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        clients = Client.objects.filter(company=company)

        # Get query parameters
        teacher = request.query_params.get('teacher')
        client_type = request.query_params.get('type')

        # Filter clients based on query parameters
        if teacher is not None:
            clients = clients.filter(teacher__icontains=teacher)
        if client_type is not None:
            clients = clients.filter(type__icontains=client_type)

        serializer = self.OutputSerializer(clients, many=True)
        return Response({"data": serializer.data})



class CreateClientInfoAPI(APIView): 
    #Esta clase es para crear o modificar un cliente
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    class InputSerializer(serializers.ModelSerializer):        
        #Estos campos pueden variar con respecto a los del output
        username = serializers.SerializerMethodField()
        
        class Meta:
            model = Client
            fields = ['username','teacher','company','type']
        def get_username(self, obj):
            return obj.user_client.username
   
    def post(self, request,company, format=None):                                    
        #Esta función es para crear un cliente
        
        try:
            company = Company.objects.get(user_company_id=company)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.InputSerializer(data=request.data)
        #Se crea un serializer con los datos del cliente
        
        if serializer.is_valid():
            serializer.save(user_client= user, company=company)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,  format=None):                     
        #Esta función es para modificar un cliente
        
        try:
            company = Company.objects.get(user_company_id=company)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            client = Client.objects.get(request.user)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        #Si el cliente no existe se devuelve un error

        serializer = self.InputSerializer(client, data=request.data)
        #Se crea un serializer con los datos del cliente
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 

