from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.contrib import messages
from .models import Alumno

class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'dni', 'email']

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/dashboard.html', {'alumnos': alumnos})

@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, 'Alumno creado.')
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/crear.html', {'form': form})