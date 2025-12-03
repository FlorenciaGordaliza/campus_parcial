from django.urls import path
from .views import dashboard, crear_alumno
from .pdf import enviar_pdf_por_correo, descargar_pdf_alumno, descargar_pdf_todos
from .csv import export_csv_view 

app_name = 'alumnos'
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('crear/', crear_alumno, name='crear'),
    path('descargar-pdf/<int:alumno_id>/', descargar_pdf_alumno, name='descargar_pdf'),
    path('descargar-todos-pdf/', descargar_pdf_todos, name='descargar_todos_pdf'),
    path('enviar-pdf/<int:alumno_id>/', enviar_pdf_por_correo, name='enviar_pdf'),
    path('export-csv/', export_csv_view, name='export_csv'),
]