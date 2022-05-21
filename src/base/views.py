from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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


class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'
    template_name = 'base/tareas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(user=self.request.user, completed=False)
        context['count'] = context['tareas'].filter(completed=False).count()
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