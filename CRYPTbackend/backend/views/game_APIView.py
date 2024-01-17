from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from backend.models import Client, Game
from backend.permissions import IsClientUser
from django.utils import timezone


class GetGameInfoAPI(APIView):
    #Esta clase es para obtener la información de un cliente
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser] 
    
    class OutputSerializer(serializers.ModelSerializer):
        username = serializers.SerializerMethodField()
        
        class Meta:
            model = Game
            fields = ['id', 'username', 'start_time', 'end_time', 'game_type', 'game_ending_type', 'won']
        def get_username(self, obj):
            return obj.user_client.user_client.username
  

    def get(self, request, format=None):
        
        try:
            client = Client.objects.get(user_client=request.user)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        game= Game.objects.filter(user_client=client)
        
        # Get query parameters
        game_type = request.query_params.get('game_type')
        game_ending_type = request.query_params.get('game_ending_type')
        won = request.query_params.get('won')

        # Filter clients based on query parameters
        if game_type is not None:
            game = game.filter(game_type__icontains=game_type)
        if game_ending_type is not None:
            game = game.filter(game_ending_type__icontains=game_ending_type)
        if won is not None:
            game = game.filter(won=won)
        
        serializer = self.OutputSerializer(game, many=True)
        return Response({"data": serializer.data})
    
    
class CreateGameInfoAPI(APIView):
    #Esta clase es para crear o modificar un cliente
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsClientUser]     
    
    class InputSerializer(serializers.ModelSerializer): 
        username = serializers.SerializerMethodField()         #Estos campos pueden variar con respecto a los del output
    
        class Meta:
            model = Game
            fields = ['username', 'start_time', 'end_time', 'game_type', 'game_ending_type', 'won']
            
        def get_username(self, obj):
            return obj.user_client.user_client.username
  

    
    def post(self, request, format=None):
        #Esta función es para crear un cliente
        
        try:
            client = Client.objects.get(user_client=request.user)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.InputSerializer(data=request.data)
        #Se crea un serializer con los datos del cliente
    
        if serializer.is_valid():
            serializer.save(user_client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                                    
        

    def put(self, request, game_id, format=None):                     
        #Esta función es para modificar un cliente
       
        try:
            game = Game.objects.get(request.user, game_id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        #Si el cliente no existe se devuelve un error

        serializer = self.InputSerializer(game, data=request.data)
        #Se crea un serializer con los datos del cliente
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)