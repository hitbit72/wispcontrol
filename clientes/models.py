from django.db import models


class Cliente(models.Model):
    """Cliente final del WISP (persona o empresa) que contrata servicios."""

    class TipoDocumento(models.TextChoices):
        DNI = 'dni', 'DNI'
        RUC = 'ruc', 'RUC / RFC / NIT'
        PASAPORTE = 'pasaporte', 'Pasaporte'
        OTRO = 'otro', 'Otro'

    nombre_completo = models.CharField(max_length=200, verbose_name='Nombre completo / Razón social')
    tipo_documento = models.CharField(max_length=20, choices=TipoDocumento.choices, default=TipoDocumento.DNI)
    numero_documento = models.CharField(max_length=30, blank=True, verbose_name='Número de documento')
    telefono = models.CharField(max_length=20, blank=True)
    telefono_alternativo = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    fecha_alta = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre_completo']

    def __str__(self):
        return self.nombre_completo


class Contrato(models.Model):
    """Servicio contratado por un cliente. Un cliente puede tener varios contratos."""

    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        SUSPENDIDO = 'suspendido', 'Suspendido'
        CANCELADO = 'cancelado', 'Cancelado'
        PENDIENTE = 'pendiente', 'Pendiente de instalación'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contratos')
    nombre_plan = models.CharField(max_length=100, verbose_name='Plan / Servicio')
    velocidad_bajada_mbps = models.PositiveIntegerField(verbose_name='Velocidad de bajada (Mbps)')
    velocidad_subida_mbps = models.PositiveIntegerField(verbose_name='Velocidad de subida (Mbps)')
    precio_mensual = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_cancelacion = models.DateField(null=True, blank=True)

    # Campos pensados para la integración futura con el servicio MikroTik.
    pppoe_usuario = models.CharField(max_length=100, blank=True, verbose_name='Usuario PPPoE')
    ip_asignada = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP asignada')

    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f'{self.cliente.nombre_completo} · {self.nombre_plan}'
