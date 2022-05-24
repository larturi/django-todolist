from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    Login,
    Register,
    ListaTareas, 
    DetalleTarea, 
    CrearTarea, 
    EditarTarea, 
    EliminarTarea
)

urlpatterns = [
    path('', ListaTareas.as_view(), name='tareas'),
    path('login/', Login.as_view(), name='login'),
    path('salir/', LogoutView.as_view(next_page='login'), name='salir'),
    path('registro/', Register.as_view(), name='registro'),
    path('tarea/<int:pk>/', DetalleTarea.as_view(), name='tarea'),
    path('crear-tarea/', CrearTarea.as_view(), name='crear-tarea'),
    path('editar-tarea/<int:pk>/', EditarTarea.as_view(), name='editar-tarea'),
    path('eliminar-tarea/<int:pk>/', EliminarTarea.as_view(), name='eliminar-tarea'),
]
