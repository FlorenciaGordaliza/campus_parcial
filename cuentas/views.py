from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            send_mail(
                subject='Bienvenido al Campus',
                message=f'Hola {user.username}, ¡bienvenido!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )
            login(request, user)
            messages.success(request, 'Registro exitoso. Te enviamos un correo de bienvenida.')
            return redirect('alumnos:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'cuentas/register.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'cuentas/login.html'

class UserLogoutView(LogoutView):
    next_page = 'cuentas:login'
