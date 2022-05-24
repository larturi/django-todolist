from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Tarea

class Login(LoginView):
    template_name = 'base/login.html'
    field = '__all__'
    redirect_authenticated_user: True
    
    def get_success_url(self):
        return reverse_lazy('tareas')

class Register(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user: True
    success_url = reverse_lazy('tareas')
    
    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super().form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super().get(self.request, *args, **kwargs)

class ListaTareas(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'
    template_name = 'base/tareas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(user=self.request.user)
        context['tareas'] = context['tareas'].order_by('completed')
        context['count'] = context['tareas'].filter(completed=False).count()        
        
        valor_busqueda = self.request.GET.get('buscador') or ''
        
        if valor_busqueda:
            context['tareas'] = context['tareas'].filter(title__icontains=valor_busqueda)
            
        context['valor_busqueda'] = valor_busqueda
            
        return context
    
class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'


class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['title', 'description']
    template_name = 'base/tarea_form.html'
    success_url = reverse_lazy('tareas')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ['title', 'description', 'completed']
    template_name = 'base/tarea_form.html'
    success_url = reverse_lazy('tareas')
    
    
class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea_delete.html'
    success_url = reverse_lazy('tareas')