from django.contrib import admin
from .models import Autor, Categoria, Libro, Copia, Estudiante, Prestamo


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class CopiaInline(admin.TabularInline):
    model = Copia
    extra = 1


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "anio_publicacion", "isbn", "categoria", "idioma")
    search_fields = ("titulo", "isbn", "autores__nombre")
    list_filter = ("categoria", "idioma")
    inlines = [CopiaInline]


@admin.register(Copia)
class CopiaAdmin(admin.ModelAdmin):
    list_display = ("codigo_inventario", "libro", "condicion")
    search_fields = ("codigo_inventario", "libro__titulo")
    list_filter = ("condicion",)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "correo")
    search_fields = ("codigo", "nombre")


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ("copia", "estudiante", "fecha_salida", "fecha_limite", "fecha_devolucion")
    search_fields = ("estudiante__codigo", "estudiante__nombre", "copia__codigo_inventario")
    list_filter = ("fecha_devolucion", "fecha_limite")
    autocomplete_fields = ("copia", "estudiante")