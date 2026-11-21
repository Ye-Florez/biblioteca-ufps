from django.db import models
from django.db.models import Q


class Autor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    anio_publicacion = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    autores = models.ManyToManyField(Autor)
    idioma = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.titulo} ({self.anio_publicacion})"


class Copia(models.Model):
    class Condicion(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        USADO = "usado", "Usado"
        DANADO = "danado", "Dañado"

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    codigo_inventario = models.CharField(max_length=20, unique=True)
    condicion = models.CharField(
        max_length=10, choices=Condicion.choices, default=Condicion.NUEVO
    )

    def __str__(self):
        return f"{self.codigo_inventario} - {self.libro.titulo}"


class Estudiante(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Prestamo(models.Model):
    copia = models.ForeignKey(Copia, on_delete=models.PROTECT, verbose_name="Copia")
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT)
    fecha_salida = models.DateField()
    fecha_limite = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "préstamo"
        verbose_name_plural = "préstamos"
        constraints = [
            models.UniqueConstraint(
                fields=["copia"],
                condition=Q(fecha_devolucion__isnull=True),
                name="una_copia_un_prestamo_activo",
                violation_error_message="Esta copia ya está prestada y no ha sido devuelta.",                                                                                                                                                                                                                                              
            )
        ]

    def __str__(self):
        return f"{self.copia.codigo_inventario} -> {self.estudiante.nombre}"