from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from backend.models import Stat, Client, TypeStat
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from backend.permissions import IsClientUser


class GetStatsAPI(APIView):
    #Esta clase es para obtener la información de un tipo de estadística   
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]                              
    
    class OutputSerializer(serializers.ModelSerializer):
        username = serializers.SerializerMethodField()
        stat_type = serializers.SerializerMethodField()

        class Meta:
            model = Stat
            fields = ['id','stat_type','game','username']
        def get_username(self, obj):
            return obj.client.user_client.username
        def get_stat_type(self, obj):
            return obj.stat_type.name
        

    def get(self, request, game, format=None):
        
        
        try:
            client = Client.objects.get(user_client=request.user)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        stats = Stat.objects.filter(client=client)
        
         # Get query parameters
        stat_type = request.query_params.get('stat_type')
        game = request.query_params.get('type')
        month= request.query_params.get('month')
        year= request.query_params.get('year')
        
        # Filter clients based on query parameters
        if stat_type is not None:
            stats = stats.filter(stat_type__icontains=stat_type)
        if game is not None:
            stats = stats.filter(game__icontains=game)  
        if month is not None:
            stats = stats.filter(month__icontains=month)
        if year is not None:
            stats = stats.filter(year__icontains=year)

        # Serialize the filtered objects
        serializer = self.OutputSerializer(stats, many=True)

        # Return a response with the serialized data
        return Response(serializer.data)



class CreateStatsAPI(APIView):   
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]                            
    #Esta clase es para crear o modificar un tipo de estadística

    class InputSerializer(serializers.ModelSerializer):         
        #Estos campos pueden variar con respecto a los del output
        username = serializers.SerializerMethodField()
        stat_type = serializers.SerializerMethodField()

        class Meta:
            model = Stat
            fields = ['stat_type', 'game','username']
        def get_username(self, obj):
            return obj.client.user_client.username
        def get_stat_type(self, obj):
            return obj.stat_type.name
   


    def post(self, request, game, format=None):                                   
        #Esta función es para crear un tipo de estadística
        
        try:
            client = Client.objects.get(user_client=request.user)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            type_stat = TypeStat.objects.get(name=request.data['stat_type'])
        except TypeStat.DoesNotExist:    
            return Response({'error': 'TypeStat not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.InputSerializer(data=request.data)
        #Se crea un serializer con los datos del tipo de estadística
        if serializer.is_valid():
            serializer.save(client=client,stat_type=type_stat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, game, stat , format=None):                     
        #Esta función es para modificar un tipo de estadística
        client=Client.objects.get(user_client=request.user)
        try:
            stat = Stat.objects.get(client=client, id=stat, game=game)
        except Stat.DoesNotExist:
            return Response({'error': 'Stat not found'}, status=status.HTTP_404_NOT_FOUND)
        
        #Si el tipo de estadística no existe se devuelve un error
        new_stat_type = request.data.get('stat_type')
        if new_stat_type is not None:
            try:
                new_stat_type = TypeStat.objects.get(name=request.data['stat_type'])
                stat.stat_type = new_stat_type
                stat.save()
            except TypeStat.DoesNotExist:    
                return Response({'error': 'TypeStat not found'}, status=status.HTTP_404_NOT_FOUND)
   
        serializer = self.InputSerializer(stat, data=request.data)
        #Se crea un serializer con los datos del tipo de estadística
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)