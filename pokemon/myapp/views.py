# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from .models import Usuario, Licencia, Registro
from django.contrib import messages
import pandas as pd
from datetime import datetime

def seleccionar_licencia(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_usuario')
        licencia_seleccionada_id = request.POST.get('licencia_seleccionada')  
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_finalizacion = request.POST.get('fecha_finalizacion')
        fecha_presentacion = datetime.now().strftime('%Y-%m-%d')

        nombre = nombre_completo.split(maxsplit=1)[0] if nombre_completo else ""

        # Buscar usuarios cuyos nombres comiencen con la parte ingresada por el usuario
        usuarios = Usuario.objects.filter(nombre__istartswith=nombre)

        # Tomar el primer usuario encontrado
        usuario = usuarios.first()

        try:
            licencia_seleccionada = Licencia.objects.get(id=licencia_seleccionada_id)
        except Licencia.DoesNotExist:
            messages.error(request, 'La licencia seleccionada no está disponible.')
            return redirect('seleccionar_licencia')

        # Obtener el número de usuario del usuario seleccionado
        numero_usuario = usuario.numero  # Suponiendo que el número de usuario está almacenado en el campo 'numero' del modelo Usuario

        # Crear un nuevo registro en la base de datos
        Registro.objects.create(
            nombre_usuario=usuario,
            numero_usuario=numero_usuario,  # Pasar el número de usuario al crear el registro
            numero_licencia=licencia_seleccionada,
            fecha_inicio=fecha_inicio,
            fecha_finalizacion=fecha_finalizacion,
            fecha_presentacion=fecha_presentacion  # Guardar la fecha y hora actuales en el nuevo registro
        )

        # Establecer los datos necesarios en la sesión
        request.session['nombre_usuario'] = usuario.nombre
        request.session['licencia_nombre'] = licencia_seleccionada.nombre
        request.session['licencia_numero'] = licencia_seleccionada.numero
        request.session['fecha_inicio'] = fecha_inicio
        request.session['fecha_finalizacion'] = fecha_finalizacion
        request.session['fecha_presentacion'] = fecha_presentacion

        # Redirigir al usuario a la página de resultados
        return redirect('resultado')
    else:
        licencias = Licencia.objects.all()
        usuarios = Usuario.objects.all()
        nombres_usuarios = [usuario.nombre for usuario in usuarios]
        return render(request, 'seleccionar_licencia.html', {'licencias': licencias, 'nombres_usuarios': nombres_usuarios})
    
    
def resultado(request):
    # Obtener los datos necesarios para el resultado desde donde sea que estén disponibles
    nombre_usuario = request.session.get('nombre_usuario')
    licencia_nombre = request.session.get('licencia_nombre')
    licencia_numero = request.session.get('licencia_numero')  
    fecha_inicio = request.session.get('fecha_inicio')
    fecha_finalizacion = request.session.get('fecha_finalizacion')
    fecha_presentacion = request.session.get('fecha_presentacion')

    # Obtener los registros de la base de datos
    registros = Registro.objects.all()

    # Crear un diccionario con todos los datos que queremos pasar a la plantilla
    datos_resultado = {
        'nombre_usuario': nombre_usuario,
        'licencia_nombre': licencia_nombre,
        'licencia_numero': licencia_numero,  
        'fecha_inicio': fecha_inicio,
        'fecha_finalizacion': fecha_finalizacion,
        'fecha_presentacion': fecha_presentacion,
        'registros': registros  # Pasar los registros a la plantilla
    }

    # Renderizar la plantilla 'resultado.html' con el contexto creado
    return render(request, 'resultado.html', datos_resultado)


def ver_registros(request):
    registros = Registro.objects.all()
    registros_data = []
    for registro in registros:
        # Obtener la fecha y hora actual en el formato deseado
        fecha_presentacion = registro.fecha_presentacion.strftime('%Y-%m-%d')  # Cambia el formato según tus necesidades
        
        registro_data = {
            'id_registro': registro.id,  
            'nombre_usuario': registro.nombre_usuario.nombre,
            'numero_legajo': registro.nombre_usuario.numero,  
            'numero_licencia': registro.numero_licencia.numero,
            'fecha_inicio': registro.fecha_inicio,
            'fecha_finalizacion': registro.fecha_finalizacion,
            'fecha_presentacion': fecha_presentacion
        }
        registros_data.append(registro_data)
    context = {
        'registros': registros_data
    }
    return render(request, 'ver_registros.html', context)


def descargar_excel(request):
    if request.method == 'POST':
        registros = Registro.objects.all()
        registros_data = []
        for registro in registros:
            registro_data = {
                'id_registro': registro.id,  
                'nombre_usuario': registro.nombre_usuario.nombre,
                'numero_legajo': registro.nombre_usuario.numero,  
                'numero_licencia': registro.numero_licencia.numero,
                'fecha_inicio': registro.fecha_inicio,
                'fecha_finalizacion': registro.fecha_finalizacion,
                'fecha_presentacion': registro.fecha_presentacion
            }
            registros_data.append(registro_data)

        df = pd.DataFrame(registros_data)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="registros.xlsx"'
        df.to_excel(response, index=False)
        return response
    else:
        # Manejar solicitudes GET para evitar errores
        return HttpResponse("Esta página solo maneja solicitudes POST.")
    


