import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Alumno

@login_required
def export_csv_view(request):
    alumnos = Alumno.objects.filter(usuario=request.user) 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumnos.csv"'
    writer = csv.writer(response)
    writer.writerow(['nombre','dni','email'])
    for a in alumnos:
        writer.writerow([a.nombre, a.dni, a.email])
    return response
