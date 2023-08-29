from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import CursoForm, ProfesorForm, RegistroUsuarioForm, ProductosForm, VendedoresForm, CategoriasForm, UserEditForm, AvatarForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Para no ingresar a la plataforma sin loguearse
from django.contrib.auth.mixins import LoginRequiredMixin # vistas basadas en clases
from django.contrib.auth.decorators import login_required # para vistas basadas en funciones

def crear_curso(request):
    nombre_curso = "Programacion Basica"
    comision_curso = 98765
    print("Creando curso")
    curso = Curso(nombre=nombre_curso, comision=comision_curso)
    # curso.save()
    respuesta = f"Curso creado: {nombre_curso} - {comision_curso}"
    return HttpResponse(respuesta)

@login_required
def cargarAvatar(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    if len(avatar) != 0:
        return avatar[0].imagen.url
    
    return "/media/avatars/default.png"

@login_required
def listar_cursos(request):
    cursos = Curso.objects.all()
    respuesta = "<h2>Cursos</h2>"
    for curso in cursos:
        respuesta += f"Curso: {curso.nombre} - Comisión: {curso.comision}<br>"
    return HttpResponse(respuesta)

def inicio(request):
    return render(request,"AppCoder/inicio.html", {"avatar": cargarAvatar(request)})

@login_required
def profesores(request):
    
    # formulario = ProfesorForm()
    mensaje = ""
    if request.method == "POST":

        form = ProfesorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            nombre    = str(data["nombre"]).rstrip()
            apellido  = str(data["apellido"]).rstrip()
            email     = str(data["email"]).rstrip()
            profesion = str(data["profesion"]).rstrip()

            new_profe = Profesor(nombre=str(nombre).capitalize(), apellido=str(apellido).capitalize(), email=str(email).lower(), profesion = str(profesion).capitalize())
            new_profe.save()
            mensaje = "Profesor creado!"
        else:
            mensaje = "Formulario inválido!"
    
    formulario = ProfesorForm()
    profes = Profesor.objects.all()
    return render(request,
                  "AppCoder/profesores.html", 
                  {"profes":profes, "formulario":formulario, "mensaje":mensaje, "avatar": cargarAvatar(request)}
            )

@login_required
def eliminarProfesor(request, id):
    profesor = Profesor.objects.get(id=id)
    profesor.delete()

    formulario = ProfesorForm()
    profes = Profesor.objects.all()
    return render(request,
                  "AppCoder/profesores.html", 
                  {"profes":profes, "formulario":formulario, "mensaje":"Profesor Eliminado!", "avatar": cargarAvatar(request)}
            )

@login_required
def editarProfesor(request, id):
    profesor = Profesor.objects.get(id=id)
    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            profesor.nombre    = str(data["nombre"]).rstrip()
            profesor.apellido  = str(data["apellido"]).rstrip()
            profesor.email     = str(data["email"]).rstrip()
            profesor.profesion = str(data["profesion"]).rstrip()

            profesor.save()
            mensaje = "Profesor editado correctamente!"

            profes = Profesor.objects.all()
            formulario = ProfesorForm()

            return render(request,
                  "AppCoder/profesores.html", 
                  {"profes":profes, "formulario":formulario, "mensaje":mensaje, "avatar": cargarAvatar(request)}
            )
    else:
        formulario = ProfesorForm(initial= {
            "nombre":profesor.nombre,
            "apellido":profesor.apellido,
            "email":profesor.email,
            "profesion":profesor.profesion
        })
        return render(request,
                      "AppCoder/editarProfesor.html",
                      { "formulario":formulario, "profesor":profesor, "avatar": cargarAvatar(request) }
                )

def estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request,
                  "AppCoder/estudiantes.html", 
                  {"estudiantes":estudiantes, "avatar": cargarAvatar(request)}
            )


@login_required
def cursos(request):
    if request.method == "POST":
        # nombre   = request.POST["nombre"]
        # comision = request.POST["comision"]
        # curso = Curso(nombre=str(nombre).capitalize(), comision=comision)
        # curso.save()
        mensaje = "Formulario inválido!"
        form = CursoForm(request.POST)
        if form.is_valid():
            info = form.cleaned_data
            nombre   = info["nombre"]
            comision = info["comision"]
            curso = Curso(nombre=str(nombre).capitalize(), comision=comision)
            curso.save()
            mensaje = "Curso creado satisfactoriamente!"
            
        return render(request, "AppCoder/cursos.html", {"mensaje":mensaje, "avatar": cargarAvatar(request)})
    
    formulario_curso = CursoForm()
    return render(request, "AppCoder/cursos.html",{"formulario":formulario_curso, "avatar": cargarAvatar(request)})

@login_required
def entregables(request):

    return render(request,"AppCoder/cursos.html", { "avatar":cargarAvatar(request) })

@login_required
def busquedaComision(request):

    return render(request,"AppCoder/busquedaComision.html")

@login_required
def buscar(request):
    comision = request.GET["comision"]
    mensaje = "Sin resultados!"
    if comision != "":
        listar_cursos = Curso.objects.filter(comision__icontains=comision)
        if listar_cursos:
            mensaje = ""
    return render(
            request,
            "AppCoder/resultadosBusqueda.html",
            {"cursos":listar_cursos, "mensaje":mensaje, "avatar": cargarAvatar(request)}
        )


class EstudiantesList(LoginRequiredMixin, ListView):
    model = Estudiante
    template_name = "AppCoder/estudiantes.html"

class EstudianteCreacion(LoginRequiredMixin, CreateView):
    model = Estudiante
    success_url = reverse_lazy("estudiante_list")
    fields = ['nombre', 'apellido', 'email']

class EstudianteDetalle(LoginRequiredMixin, DetailView):
    model = Estudiante
    template_name = "AppCoder/estudiante_detail.html"

class EstudianteDelete(LoginRequiredMixin, DeleteView):
    model = Estudiante
    success_url = reverse_lazy("estudiante_list")

class EstudianteUpdate(LoginRequiredMixin, UpdateView):
    model = Estudiante
    success_url = reverse_lazy("estudiante_list")
    fields = ['nombre', 'apellido', 'email']

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            data = form.cleaned_data

            username = data["username"]
            clave    = data["password"]

            usuario = authenticate(username=username, password=clave)

            if usuario is not None:
                login(request, usuario)
                return render(request,
                              "AppCoder/inicio.html",
                              {"mensaje": f"Usuario {username} logueado correctamente!"})
        return render(request,
                      "AppCoder/login.html",
                      {"formulario":form, "mensaje": "Datos inválidos!"})
    
    # No es necesario hacer un else
    form = AuthenticationForm()
    return render(request,
                    "AppCoder/login.html",
                    {"formulario":form})

def register(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            nombre = data["username"]

            form.save()
            return render(request,
                          "AppCoder/inicio.html",
                          {"mensaje": f"Usuario {nombre} creado correctamente!"})
        return render(request,
                          "AppCoder/inicio.html",
                          {"mensaje": "Datos inválidos!"})

    
    form = RegistroUsuarioForm()
    return render(request,
                  "AppCoder/register.html",
                  {"formulario":form})

def editarPerfil(request):
    usuario = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            usuario.email = data["email"]
            usuario.password1 = data["password1"]
            usuario.password2 = data["password2"]
            usuario.first_name = data["first_name"]
            usuario.last_name = data["last_name"]
            usuario.save()
            return render(
                request,
                "AppCoder/inicio.html",
                {"mensaje":f"Usuario {usuario.username} actualizado!", "avatar":cargarAvatar(request)}
            )
        return render(
                request,
                "AppCoder/editarPerfil.html",
                {"form":form, "mensaje":f"Datos inválidos!", "nombreusuario":usuario.username, "avatar":cargarAvatar(request)}
            )
        
    form = UserEditForm(instance=usuario)
    return render(request,
                  "AppCoder/editarPerfil.html",
                  {"form":form, "nombreusuario":usuario.username, "avatar":cargarAvatar(request)})

@login_required
def agregarAvatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = Avatar(user = request.user, imagen = form.cleaned_data['imagen'])
            oldAvatar = Avatar.objects.filter(user = request.user)
            if len(oldAvatar) > 0:
                oldAvatar.delete()
            avatar.save()
            return render(request,
                          "AppCoder/inicio.html",
                          {"mensaje":"Avatar agregado correctamente!", "avatar":cargarAvatar(request)})
        return render(request,
                          "AppCoder/inicio.html",
                          {"mensaje":"Error al cargar avatar!", "avatar":cargarAvatar(request)})
    form = AvatarForm()
    return render(request,
                  "AppCoder/agregarAvatar.html",
                  {"form":form, "usuario":request.user,"avatar":cargarAvatar(request)})

# PRE ENTREGA 3

def home(request):

    return render(request,"Entrega/inicio.html")

def productos(request):
    mensaje = ""
    
    if request.method == "POST":
        form = ProductosForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            newProducto = Producto(descripcion = data["descripcion"].title(),
                                   marca       = data["marca"].title(),
                                   precio      = data["precio"],
                                   stock       = data["stock"]
                               )
            newProducto.save()
            mensaje = "Producto creado!"
        else:
            mensaje = "Formulario inválido!"

    allProductos = Producto.objects.all()
    if not allProductos:
        crear_productos()
        allProductos = Producto.objects.all()

    form = ProductosForm()
    return render(request,
                  "Entrega/productos.html",
                  {"form":form, "productos":allProductos, "mensaje":mensaje})


def eliminarProducto(request,id):
    producto = Producto.objects.get(id=id)
    producto.delete()

    allProductos = Producto.objects.all()
    form = ProductosForm()
    return render(request,
                  "Entrega/productos.html",
                  {"form":form, "productos":allProductos, "mensaje":"Producto eliminado!"})

def editarProducto(request, id):
    producto = Producto.objects.get(id=id)

    if request.method == "POST":
        form = ProductosForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            producto.descripcion = str(data["descripcion"]).rstrip().title()
            producto.marca = str(data["marca"]).rstrip().title()
            producto.precio = data["precio"]
            producto.stock = data["stock"]

            producto.save()
            allProductos = Producto.objects.all()
            form = ProductosForm()
            return render(request,
                  "Entrega/productos.html",
                  {"form":form, "productos":allProductos, "mensaje":"Producto actualizado!"})
    else:
        form = ProductosForm(initial= {
            "descripcion" : producto.descripcion,
            "marca"       : producto.marca,
            "precio"      : producto.precio,
            "stock"       : producto.stock 
        })

        return render(request,
                  "Entrega/editar_producto.html",
                  {"form":form, "producto":producto})
    
def buscarProducto(request):
    if request.method == "POST":
        filtro = request.POST["busqueda"]
        allProductos = Producto.objects.filter(descripcion__icontains=filtro)
        mensaje = f"Resultados encontrados: {allProductos.count()}"
        if not allProductos:
            allProductos = Producto.objects.all()
            mensaje = f"No se encontraron resultados asociados a la descripción '{filtro}'!"
        form = ProductosForm()
        return render(request,
                  "Entrega/productos.html",
                  {"form":form, "productos":allProductos, "mensaje":mensaje})
        
def crear_productos():
    arrProductos = [
        {"descripcion":"Air Pods Max",  "marca": "Apple", "precio": 490000, "stock":10},
        {"descripcion":"MacBook Pro",   "marca": "Apple", "precio": 1200000,"stock":8 },
        {"descripcion":"iPhone 14 Pro", "marca": "Apple", "precio": 949000 ,"stock":5 },
        {"descripcion":"Apple Watch S8","marca": "Apple", "precio": 590000 ,"stock":12}
    ]
    
    for producto in arrProductos:
        newProducto = Producto(descripcion = producto["descripcion"],
                               marca       = producto["marca"],
                               precio      = producto["precio"],
                               stock       = producto["stock"]
                               )
        newProducto.save()

def vendedor(request):
    mensaje = ""
    if request.method == "POST":
        form = VendedoresForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            newVendedor = Vendedor(
                nombre    = data["nombre"].title().rstrip(),
                apellido  = data["apellido"].title().rstrip(),
                email     = data["email"].rstrip(),
                direccion = data["direccion"].title().rstrip(),
                seccion   = data["seccion"].title().rstrip()
            )
            newVendedor.save()
            mensaje = "Vendedor creado!"
        else:
            mensaje = "Datos inválidos!"
    vendedores = Vendedor.objects.all()
    form = VendedoresForm()
    
    atributos = ["nombre", "apellido", "email", "direccion", "seccion"]
    clase     = "form-control h-25 w-100"

    for field_name in atributos:
        form.fields[field_name].widget.attrs["class"] = clase

    return render(request,
                  "Entrega/vendedores.html",
                  {"form":form, "vendedores":vendedores, "mensaje":mensaje})

def editarVendedor(request, id):
    vendedor = Vendedor.objects.get(id=id)

    if request.method == "POST":
        form = VendedoresForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            vendedor.nombre     = str(data["nombre"]).title().rstrip()
            vendedor.apellido   = str(data["apellido"]).title().rstrip()
            vendedor.email      = data["email"].rstrip()
            vendedor.direccion  = data["direccion"].title().rstrip()
            vendedor.seccion    = data["seccion"].title().rstrip()

            vendedor.save()
            allVendedores = Vendedor.objects.all()
            form = VendedoresForm()
            atributos = ["nombre", "apellido", "email", "direccion", "seccion"]
            clase     = "form-control h-25 w-100"

            for field_name in atributos:
                form.fields[field_name].widget.attrs["class"] = clase

            return render(request,
                  "Entrega/vendedores.html",
                  {"form":form, "vendedores":allVendedores, "mensaje":"Vendedor actualizado!"})
    else:
        form = VendedoresForm(initial= {
            "nombre"    : vendedor.nombre,
            "apellido"  : vendedor.apellido,
            "email"     : vendedor.email,
            "direccion" : vendedor.direccion,
            "seccion"   : vendedor.seccion
        })
        atributos = ["nombre", "apellido", "email", "direccion", "seccion"]
        clase     = "form-control h-25 w-100"

        for field_name in atributos:
            form.fields[field_name].widget.attrs["class"] = clase

        return render(request,
                  "Entrega/editar_vendedor.html",
                  {"form":form, "vendedor":vendedor})

def eliminarVendedor(request, id):
    vendedor = Vendedor.objects.get(id=id)
    vendedor.delete()

    allVendedores = Vendedor.objects.all()
    form = VendedoresForm()
    return render(request,
                  "Entrega/vendedores.html",
                  {"form":form, "vendedores":allVendedores, "mensaje":"Vendedor eliminado!"})

def buscarVendedor(request):

    if request.method == "POST":
        filtro = request.POST["busqueda"]
        allVendedores = Vendedor.objects.filter(nombre__icontains=filtro)
        mensaje = f"Resultados encontrados: {allVendedores.count()}"
        if not allVendedores:
            allVendedores = Vendedor.objects.all()
            mensaje = f"No se encontraron resultados asociados al nombre: '{filtro}'!"
        form = VendedoresForm()
        return render(request,
                  "Entrega/vendedores.html",
                  {"form":form, "vendedores":allVendedores, "mensaje":mensaje})
    
def categorias(request):
    mensaje = ""
    if request.method == "POST":
        form = CategoriasForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            newCategoria = Categoria(
                nombre      = data["nombre"].title().strip(),
                descripcion = data["descripcion"].capitalize().strip(),
                activo      = data["activo"]
            )
            newCategoria.save()
            mensaje = "Categoría creada!"
        else:
            mensaje = "Campos inválidos!"
    allCategorias = Categoria.objects.all()
    form = CategoriasForm(initial={"activo":True})
    return render(request,
                  "Entrega/categorias.html",
                  {"form":form, "categorias":allCategorias,"mensaje":mensaje})

def editarCategoria(request, id):
    mensaje = ""
    categoria = Categoria.objects.get(id=id)
    if request.method == "POST":
        form = CategoriasForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            categoria.nombre      = str(data["nombre"]).title().strip()
            categoria.descripcion = str(data["descripcion"]).capitalize().strip()
            categoria.activo      = data["activo"]

            categoria.save()

            allCategorias = Categoria.objects.all()
            form = CategoriasForm(initial={"activo":True})
            mensaje = "Categoría actualizada!"
        else:
            mensaje = "Campos inválidos!"
        return render(request,
                  "Entrega/categorias.html",
                  {"form":form, "categorias":allCategorias,"mensaje":mensaje})
    else:
        form = CategoriasForm(initial= {
            "nombre"      : categoria.nombre,
            "descripcion" : categoria.descripcion,
            "activo"      : categoria.activo
        })
        allCategorias = Categoria.objects.all()
        return render(request,
                  "Entrega/editar_categorias.html",
                  {"form":form, "categoria":categoria})

def eliminarCategoria(request, id):
    categoria = Categoria.objects.get(id = id)
    categoria.delete()

    allCategorias = Categoria.objects.all()
    form = CategoriasForm(initial={"activo":True})
    return render(request,
                  "Entrega/categorias.html",
                  {"form":form, "categorias":allCategorias,"mensaje":"Categoría eliminada!"})

