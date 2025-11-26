from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
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