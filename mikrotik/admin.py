from django import forms
from django.contrib import admin
from .models import Router, Plan, TareaSincronizacion
from .fields import EncryptedCharField


class PlanInline(admin.TabularInline):
    model = Plan
    extra = 0


@admin.register(Router)
class RouterAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'modelo', 'ip', 'puerto', 'sector')
    list_filter = ('sector',)
    search_fields = ('nombre', 'ip', 'modelo')
    inlines = [PlanInline]
    formfield_overrides = {
        EncryptedCharField: {'widget': forms.PasswordInput(render_value=True)},
    }


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'router', 'velocidad_bajada', 'velocidad_subida', 'priority_down', 'priority_up')
    list_filter = ('router',)
    search_fields = ('nombre', 'router__nombre')

@admin.register(TareaSincronizacion)
class TareaSincronizacionAdmin(admin.ModelAdmin):
    """
    Estas tareas las crea el sistema (al guardar/borrar un Contrato) y las
    procesa el servicio MikroTik — no se crean ni editan a mano desde aquí,
    solo sirve para ver el estado y el motivo si algo falló.
    """
    list_display = ('contrato', 'operacion', 'estado', 'intentos', 'creada_en', 'procesada_en')
    list_filter = ('estado', 'operacion')
    search_fields = ('contrato__cliente__nombre_completo', 'contrato__identificador_mikrotik')
    readonly_fields = [f.name for f in TareaSincronizacion._meta.fields]

    def has_add_permission(self, request):
        return False