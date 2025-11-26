from django.urls import path
from .views import dashboard, crear_alumno
from .pdf import enviar_pdf_por_correo

app_name = 'alumnos'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('crear/', crear_alumno, name='crear'),
    path('enviar-pdf/<int:alumno_id>/', enviar_pdf_por_correo, name='enviar_pdf'),
]