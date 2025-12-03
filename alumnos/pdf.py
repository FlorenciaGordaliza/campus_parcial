from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from .models import Alumno

def generar_pdf_alumno(alumno):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 80, "Ficha de Alumno")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 120, f"Nombre: {alumno.nombre}")
    c.drawString(50, height - 140, f"DNI: {alumno.dni}")
    c.drawString(50, height - 160, f"Email: {alumno.email}")
    c.drawString(50, height - 180, f"Creado: {alumno.fecha_registro.strftime('%Y-%m-%d %H:%M')}")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def generar_pdf_todos_alumnos(alumnos, usuario):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Título
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 60, "Listado de Alumnos")
    
    # Info del usuario
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, f"Usuario: {usuario.username}")
    c.drawString(50, height - 95, f"Total de alumnos: {alumnos.count()}")
    
    # Encabezados de tabla
    y_position = height - 130
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_position, "Nombre")
    c.drawString(220, y_position, "DNI")
    c.drawString(320, y_position, "Email")
    
    # Línea separadora
    c.line(50, y_position - 5, width - 50, y_position - 5)
    
    # Contenido
    c.setFont("Helvetica", 10)
    y_position -= 25
    
    for alumno in alumnos:
        # Si llegamos al final de la página, crear nueva
        if y_position < 80:
            c.showPage()
            y_position = height - 80
            c.setFont("Helvetica", 10)
        
        c.drawString(50, y_position, alumno.nombre[:30])
        c.drawString(220, y_position, alumno.dni)
        c.drawString(320, y_position, alumno.email[:35])
        y_position -= 20
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

@login_required
def descargar_pdf_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, usuario=request.user)
    pdf_buffer = generar_pdf_alumno(alumno)
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="alumno_{alumno.nombre.replace(" ", "_")}.pdf"'
    return response

@login_required
def descargar_pdf_todos(request):
    alumnos = Alumno.objects.filter(usuario=request.user).order_by('nombre')
    pdf_buffer = generar_pdf_todos_alumnos(alumnos, request.user)
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="listado_alumnos.pdf"'
    return response

@login_required
def enviar_pdf_por_correo(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, usuario=request.user)
    pdf_buffer = generar_pdf_alumno(alumno)
    email = EmailMessage(
        subject=f'PDF Alumno - {alumno.nombre}',
        body='Adjunto PDF con los datos del alumno.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[request.user.email],  # cambiar al correo del docente si corresponde
    )
    email.attach(f'alumno_{alumno.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
    email.send(fail_silently=False)
    messages.success(request, 'PDF enviado por correo.')
    return redirect('alumnos:dashboard')