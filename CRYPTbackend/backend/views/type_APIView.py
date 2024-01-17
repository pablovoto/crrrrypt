from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets
from backend.models import TypeStat, Company
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication   
from backend.permissions import IsCompanyUser

class GetTypeStatAPI(APIView):   
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, IsCompanyUser]
    #Esta clase es para obtener la información de un tipo de estadística
    class OutputSerializer(serializers.ModelSerializer):
        company = serializers.SerializerMethodField()
        class Meta:
            model = TypeStat
            fields = ['id','company','name']
        def get_company(self, obj):
            return obj.company.user_company.username
    
    def get(self, request, format=None):
       
        try:
            company = Company.objects.get(user_company=request.user)
        except Company.DoesNotExist:                        
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
       
        type = TypeStat.objects.all()
        serializer = self.OutputSerializer(type, many=True)
        return Response({"data": serializer.data})



class CreateTypeStatAPI(APIView):                             
    #Esta clase es para crear o modificar un tipo de estadística
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, IsCompanyUser]
    class InputSerializer(serializers.ModelSerializer):         
        #Estos campos pueden variar con respecto a los del output
        class Meta:
            model = TypeStat
            fields = ['name']
    
    def post(self, request):                                    
        #Esta función es para crear un tipo de estadística
        
        try:
            company = Company.objects.get(user_company=request.user)
        except Company.DoesNotExist:                        
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.InputSerializer(data=request.data)
        #Se crea un serializer con los datos del tipo de estadística
        if serializer.is_valid():
            serializer.save(company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):                     
        #Esta función es para modificar un tipo de estadística
        
        try:
            company = Company.objects.get(user_company=request.user)
        except Company.DoesNotExist:                        
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            type = TypeStat.objects.get(id=id, company=company)
        except TypeStat.DoesNotExist:
            return Response({'error': 'Type Stat not found'}, status=status.HTTP_404_NOT_FOUND)
        #Si el tipo de estadística no existe se devuelve un error

        serializer = self.InputSerializer(type, data=request.data)
        #Se crea un serializer con los datos del tipo de estadística
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
