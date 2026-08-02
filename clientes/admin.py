from django.contrib import admin
from .models import Cliente, Contrato


class ContratoInline(admin.TabularInline):
    model = Contrato
    extra = 0


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'apodo', 'telefono', 'poblacion', 'activo', 'fecha_alta')
    list_filter = ('activo', 'poblacion')
    search_fields = ('nombre_completo', 'apodo', 'numero_documento', 'telefono', 'email')
    inlines = [ContratoInline]


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'nombre_plan', 'conexion', 'estado', 'velocidad_bajada_mbps', 'velocidad_subida_mbps', 'precio_mensual')
    list_filter = ('estado', 'conexion', 'nombre_plan')
    search_fields = ('cliente__nombre_completo', 'pppoe_usuario', 'ip_asignada')
