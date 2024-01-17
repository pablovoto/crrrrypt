from django.urls import include, path
from rest_framework import routers
from .views import *
# from .empresa_APIView import *

# router = routers.DefaultRouter()
# router.register(r'empresa', EmpresaViewSet),
# router.register(r'estadisticas', StatsViewSet),
# # router.register(r'partidos', views.GameViewSet)
# router.register(r'clientes', ClientViewSet)
# # router.register(r'cliente-detail', views.ClienteDetailView)


#_________________________CAPAZ DEBA AGREGAR EL ID DEL SUPERUSER EN LA URL PARA QUE NO SE PUEDA MODIFICAR A OTRO USUARIO_________________________


app_name = "app"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("post/user/", CreateUserInfoAPI.as_view()), #crear un usuario
    path("get/user/", GetUserInfoAPI.as_view()),    #control de usuarios LVL ADMIN
    path("put/<int:user_id>/user/", CreateUserInfoAPI.as_view()), #modificar un usuario
    
    path("post/company/", CreateCompanyInfoAPI.as_view()), #crear una empresa
    path("get/company/", GetCompanyInfoAPI.as_view()), #obtener una empresa
    path("put/company/ ", CreateCompanyInfoAPI.as_view()), #modificar una empresa
    
    path("post/type_stat/", CreateTypeStatAPI.as_view()), #crear un cliente
    path("get/type_stat/", GetTypeStatAPI.as_view()), #obtener un cliente
    path("put/type_stat/<int:id>", CreateTypeStatAPI.as_view()), #modificar un cliente
    #urls de las empresas
    #control de clientes LVL EMPRESA
    path("post/<int:company>/client/", CreateClientInfoAPI.as_view()), #crear un cliente
    path("get/client/", GetClientInfoAPI.as_view()), #obtener un cliente
    path('put/client/', CreateUserInfoAPI.as_view(), name='client-info'), #modificar un cliente
    #control de estadísticas LVL EMPRESA
    path("post/type/", CreateTypeStatAPI.as_view()), #crear tipos de estadisticas
    path("get/type/", GetTypeStatAPI.as_view()), #obtener tipos de estadisticas
    path("put/type/<int:id>", CreateTypeStatAPI.as_view()), #modificar tipos de estadisticas
    #urls de los clientes
    path("post/client/game/", CreateGameInfoAPI.as_view()),  #crear juegos
    path("get/client/game/", GetGameInfoAPI.as_view(), name= 'matches'), #obtener juegos
    path("put/client/game/<int:id>/", CreateGameInfoAPI.as_view()), #modificar juegos
    # #urls de los juegos
    path("post/client/<int:game>/stats/",  CreateStatsAPI.as_view()),  #crear estadisticas
    path("get/client/<int:game>/stats/", GetStatsAPI.as_view()),   #obtener estadisticas
    path("put/client/<int:game>/stats/<int:stat>", CreateStatsAPI.as_view()), #modificar estadisticas
    # #urls de las estadisticas

]



 