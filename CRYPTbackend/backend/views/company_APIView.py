from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from backend.models import Company
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated  
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser


class GetCompanyInfoAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]                                
    #Esta clase es para obtener la información de una empresa
    
    class OutputSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Company
            fields = ['user_company','company_name','lease_date']
    
    def get(self, request, format=None):
        company = Company.objects.all()
        
        #get query parameters
        company_name = request.query_params.get('company_name')
        
        #filter clients based on query parameters
        if company_name is not None:
            company = company.filter(company_name__icontains=company_name)
        
        serializer = self.OutputSerializer(company, many=True)
        return Response({"data": serializer.data})



class CreateCompanyInfoAPI(APIView):
    #Esta clase es para crear o modificar una empresa
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    class InputSerializer(serializers.ModelSerializer):         
    
        class Meta:
            model = Company
            fields =['company_name','lease_date']
   
    def post(self, request):                                    
        #Esta función es para crear una empresa
        
        serializer = self.InputSerializer(data=request.data)
        #Se crea un serializer con los datos de la empresa
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,  format=None):                     
        #Esta función es para modificar una empresa
        
        try:
            company = Company.objects.get(request.user)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        #Si la empresa no existe se devuelve un error
        
        serializer = self.InputSerializer(company, data=request.data)
        #Se crea un serializer con los datos de la empresa
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)