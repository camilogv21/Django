from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Aprendiz, Actividades, Monitoria, Usuario
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

# mensajes tipo cookie temporales
from django.contrib import messages

#gestion de errores de base de datos

from django.core.paginator import Paginator
from pathlib import Path
from os import remove, path
BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.

def inicio(request):
    #return HttpResponse(request, 'territorium/index.html')

    return render(request,'territorium/index.html')


def loginForm(request):
    return render(request,'territorium/login/login.html')

def login(request):
    try:
        user = request.POST["usuario"]
        pas = request.POST["clave"]

        q = Usuario.objects.get(usuario = user, clave = pas)

        request.session["logueo"] = [q.id, q.nombre, q.apellido, q.rol, q.get_rol_display()]

        return redirect('territorium:inicio')
    except:
        messages.warning(request,"no se han enviado datos")
        return redirect('territorium:login')

def loginC(request):
    try:
        del request.session["logueo"]
        messages.success(request, "session cerrada")
    except Exception as e:
        messages.warning(request, "ocurrio un error: ", e)
    return redirect('territorium:inicio')

def aprendices(request):

    login = request.session.get('logueo', False)
    if login and (login[3] == "R" or login[3] == "I"):
        q = Aprendiz.objects.all()

        p = Paginator(q, 2)
        p_number = request.GET.get('page')

        q = p.get_page(p_number)

        contexto = {'page_obj': q}

        return render(request,'territorium/aprendices/listar_aprendiz.html',contexto)
    else:
        if login and login[3] != "R" and login[3] != "I":
            messages.warning(request, "usted no esta autorizados para este modulo")
            return redirect('territorium:inicio')
        else:    
            messages.warning(request, "No has iniciado session")
            return redirect('territorium:loginForm')


def aprendicesBuscar(request):
    if request.method == "POST":

        

        q = Aprendiz.objects.filter(
            Q(nombre__icontains = request.POST["buscar"])|
            Q(apellido__icontains = request.POST["buscar"])|
            Q(cedula__icontains = request.POST["buscar"])
            )

        p = Paginator(q, 20)
        p_number = request.GET.get('page')

        q = p.get_page(p_number)

        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}

        return render(request,'territorium/aprendices/listar_aprendiz_ajax.html',contexto)
    else:
        messages.warning(request,"no se han enviado datos")
        return redirect('territorium:aprendices')

def aprendicesFormulario(request):
    return render(request, 'territorium/aprendices/crear_aprendiz.html') 

def aprendicesGuardar(request):
    try:
        if request.method == "POST":
            q = Aprendiz(
                cedula = request.POST["cedula"],
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                fecha_nacimiento = request.POST["fecha_nacimiento"],
            )
            q.save()
            messages.success(request,"¡Aprendiz guardado correctamente!")
            # messages.debug(request, 'error tal')
            # messages.info(request, 'thanks')
            # messages.warning(request, 'ojo con la fecha de nacimiento')
            # messages.error(request, 'error')
            #return HttpResponse("Aprendiz guardado correctemente! <br/> <a href='../aprendices/'>Listar Aprendices</a> ")
            #return HttpResponseRedirect(reverse('territorium:aprendices'))
            return redirect('territorium:aprendices')
        else:
            messages.warning(request,"no se han enviado datos")
            return redirect('territorium:aprendices')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('territorium:aprendices')
        # return HttpResponse("Error: " + str(e))

def aprendicesEliminar(request,id):
    try:
        a = Aprendiz.objects.get(pk = id)
        a.delete()
        return HttpResponseRedirect(reverse('territorium:aprendices'))
    except Aprendiz.DoesNotExist:
        return HttpResponse('ERROR: Aprendiz no existe')
    except Exception as e:
        return HttpResponse(f'error: {e}')

def editarAprendiz(request, id):
    A = Aprendiz.objects.get(pk = id)
    context = { "datos": A }
    return render(request, 'territorium/aprendices/editar_aprendiz.html', context) 

def ActualizarAprendiz(request):
    try:
        if request.method == "POST":
            a = Aprendiz.objects.get(pk = request.POST["id"])         
            a.cedula = request.POST["cedula"]
            a.nombre = request.POST["nombre"]
            a.apellido = request.POST["apellido"]
            a.fecha_nacimiento = request.POST["fecha_nacimiento"]
            a.save()
            messages.success(request,"¡Aprendiz Actualizado correctamente!")
            # messages.debug(request, 'error tal')
            # messages.info(request, 'thanks')
            # messages.warning(request, 'ojo con la fecha de nacimiento')
            # messages.error(request, 'error')
            #return HttpResponse("Aprendiz guardado correctemente! <br/> <a href='../aprendices/'>Listar Aprendices</a> ")
            #return HttpResponseRedirect(reverse('territorium:aprendices'))
            return redirect('territorium:aprendices')
        else:
            messages.warning(request,"no se han enviado datos")
            return redirect('territorium:aprendices')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('territorium:aprendices')
        # return HttpResponse("Error: " + str(e))


# ======================================================================================================================================

def usuario(request):

    login = request.session.get('logueo', False)
    if login and (login[3] == "R" or login[3] == "I"):
        q = Usuario.objects.all()

        p = Paginator(q, 2)
        p_number = request.GET.get('page')

        q = p.get_page(p_number)

        contexto = {'page_obj': q}

        return render(request,'territorium/usuario/listar_usuario.html',contexto)
    else:
        if login and login[3] != "R" and login[3] != "I":
            messages.warning(request, "usted no esta autorizados para este modulo")
            return redirect('territorium:inicio')
        else:    
            messages.warning(request, "No has iniciado session")
            return redirect('territorium:loginForm')


def usuarioBuscar(request):
    if request.method == "POST":

        q = Usuario.objects.filter(
            Q(nombre__icontains = request.POST["buscar"])|
            Q(rol__icontains = request.POST["buscar"])|
            Q(usuario__icontains = request.POST["buscar"])
            )

        p = Paginator(q, 20)
        p_number = request.GET.get('page')

        q = p.get_page(p_number)

        contexto = {'page_obj': q, 'Datos': request.POST["buscar"]}

        return render(request,'territorium/usuario/listar_usuario_ajax.html',contexto)
    else:
        messages.warning(request,"no se han enviado datos")
        return redirect('territorium:usuario')

def usuarioFormulario(request):
    return render(request, 'territorium/usuario/crear_usuario.html') 

def usuarioGuardar(request):
    try:
        if request.method == "POST":
            if request.FILES:
                # crear instacian de file sistem storage
                fss = FileSystemStorage()
                # capturar foto de formulario
                r = request.FILES["foto"]
                # cargar archivo alservidor
                file = fss.save("territorium/fotos/"+ r.name, r)
            else:
                file = "territorium/fotos/default.png"
            
            q = Usuario(
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                correo = request.POST["correo"],
                usuario = request.POST["usuario"],
                clave = request.POST["clave"],
                rol = request.POST["rol"],
                foto = file
            )
            q.save()
            messages.success(request,"Usuario guardado correctamente!")
            return redirect('territorium:usuario')
        else:
            messages.warning(request,"no se han enviado datos")
            return redirect('territorium:usuario')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('territorium:usuario')
        # return HttpResponse("Error: " + str(e))

def usuarioEliminar(request,id):
    try:
        a = Usuario.objects.get(pk = id)
        # Primero eliminar la foto y despues el usuario
        ruta_foto = str(BASE_DIR) + str(a.foto.url)
        #averiguamos si la ruta es validad
        if path.exists(ruta_foto):
            #Borramos la ruta de la foto
            if a.foto.url != "/uploads/territorium/fotos/default.png":
                remove(ruta_foto)
            # messages.success(request,"Foto eliminada correctamente")
        else:
            messages.error(request,"No se pudo eliminar la foto")
            raise Exception("Error!!! la foto no existe o no se encuentra")
        a.delete()
        messages.success(request,"Usuario eliminado correctamente")
        return redirect('territorium:usuario')
    except Usuario.DoesNotExist:
        messages.error(request,"Error!! el ueuario no existe")
    except Exception as e:
        messages.error(request,f'Error!! no se pudo eliminar el registro: {e}')

def editarUsuario(request, id):
    A = Usuario.objects.get(pk = id)
    context = { "datos": A }
    return render(request, 'territorium/usuario/editar_usuario.html', context) 

def ActualizarUsuario(request):
    try:
        if request.method == "POST":
            a = Usuario.objects.get(pk = request.POST["id"])
            if request.FILES:
                #Eliminar foto Anterior
                ruta_foto = str(BASE_DIR) + str(a.foto.url)
                if path.exists(ruta_foto):
                    if a.foto.url != "/uploads/territorium/fotos/default.png":
                        remove(ruta_foto)
                else:
                    raise Exception("Error!!! la foto no existe o no se encuentra")
                #Guardar foto Nueva
                fss = FileSystemStorage()
                r = request.FILES["foto"]
                file = fss.save("territorium/fotos/"+ r.name, r)
                a.foto = file
            else:
                print ("El  usuario no cambiao la foto")

            a.nombre = request.POST["nombre"]
            a.apellido = request.POST["apellido"]
            a.correo = request.POST["correo"]
            a.usuario = request.POST["usuario"]
            a.clave = request.POST["clave"]
            a.rol = request.POST["rol"]
            
            a.save()
            messages.success(request,"¡Usuario Actualizado correctamente!")
            return redirect('territorium:usuario')
        else:
            messages.warning(request,"no se han enviado datos")
            return redirect('territorium:usuario')
    except Exception as e:
        messages.error(request,"Error" + str(e))
        return redirect('territorium:usuario')
        # return HttpResponse("Error: " + str(e))


# =======================================================================================================================================


def monitorias(request):
    q = Monitoria.objects.all()
    contexto = {'datos': q}
    return render(request,'territorium/monitorias/listar_monitorias.html',contexto)

def monitoriasFormulario(request):
    q = Aprendiz.objects.all()
    contexto = {'datos':q}
    return render(request, 'territorium/monitorias/crear_monitorias.html',contexto) 

def monitoriasGuardar(request):
    
    try:
        a = Aprendiz.objects.get(pk = request.POST["aprendiz"])
        
        q = Monitoria(
            cat = request.POST["cat"],
            aprendiz = a,
            fecha_inicio = request.POST["fecha_inicio"],
            fecha_final = request.POST["fecha_final"],
        )
        q.save()
        #return HttpResponse("Monitoria guardada correctemente! <br/> <a href='../monitorias/'>Listar Monitorias</a> ")
        return HttpResponseRedirect(reverse('territorium:monitorias'))
    except Exception as e:
         return HttpResponse("Error: " + str(e))
    
def monitoriasEliminar(request,id):
    try:
        a = Monitoria.objects.get(pk = id)
        a.delete()
        return HttpResponseRedirect(reverse('territorium:monitorias'))
    except Aprendiz.DoesNotExist:
        return HttpResponse('ERROR: Monitoria no existe')
    except Exception as e:
        return HttpResponse(f'error: {e}')

def actividades(request):
    q = Actividades.objects.all()
    contexto = {'datos': q}
    return render(request,'territorium/actividades/listar_actividades.html',contexto)


def actividadesFormulario(request):
    q = Monitoria.objects.all()
    contexto = {'datos':q}
    return render(request, 'territorium/actividades/crear_actividades.html',contexto) 


def actividadesGuardar(request):
    
    try:
        a = Monitoria.objects.get(pk = request.POST["monitoria"])
        
        q = Actividades(
            monitoria = a,
            actividad = request.POST["actividad"],
            observaciones = request.POST["observaciones"],
            fecha = request.POST["fecha"],
        )
        q.save()
        return HttpResponseRedirect(reverse('territorium:actividades'))
    except Exception as e:
         return HttpResponse("Error: " + str(e))

def actividadesEliminar(request,id):
    try:
        a = Actividades.objects.get(pk = id)
        a.delete()
        return HttpResponseRedirect(reverse('territorium:actividades'))
    except Aprendiz.DoesNotExist:
        return HttpResponse('ERROR: Actividad no existe')
    except Exception as e:
        return HttpResponse(f'error: {e}')

