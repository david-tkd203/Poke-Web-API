from django.db import models
from django.contrib.auth.models import User

class PokemonRegistro(models.Model):
    ESTADOS = [
        ('visto', 'Visto'),
        ('atrapado', 'Atrapado'),
    ]

    GENEROS = [
        ('desconocido', 'Desconocido'),
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_pokemon = models.CharField(max_length=100)
    estado = models.CharField(max_length=10, choices=ESTADOS)
    fecha = models.DateTimeField(auto_now_add=True)

    # Campos adicionales al atrapar
    nivel = models.PositiveIntegerField(null=True, blank=True)
    naturaleza = models.CharField(max_length=50, null=True, blank=True)
    shiny = models.BooleanField(default=False)
    genero = models.CharField(max_length=15, choices=GENEROS, default='desconocido')
    comentarios = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'nombre_pokemon', 'estado')

    def __str__(self):
        return f"{self.usuario.username} - {self.nombre_pokemon.title()} ({self.estado})"
