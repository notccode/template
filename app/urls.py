from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('mensajes/', views.mensajes, name="mensajes"),
    path('crud/', views.crud, name="crud"),
    path('busqueda/', views.busqueda, name="busqueda"),
    path('detalle/', views.detalle, name="detalle"),
    path('estudiante/', views.estudiante, name="id_path_estudiante"),
    path('curso/', views.curso, name="id_path_curso"),

    path('mest/', views.mantenedor_estudiantes, name="mantenedor_estudiantes"),
    path('mcur/', views.mantenedor_cursos, name="mantenedor_cursos"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/login/"), name='logout'),

]
