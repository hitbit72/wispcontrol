# Portal WISP — Fase Núcleo

Esta es la primera fase del proyecto: modelo de datos base, login con roles
(administrador / técnico) y estructura del proyecto. Todavía **no** incluye
monitorización, integración con MikroTik ni dashboard — eso llega en las
siguientes fases.

## Qué incluye esta fase
- App `accounts`: usuario personalizado con rol (administrador / técnico) y login.
- App `clientes`: modelo de `Cliente` y `Contrato`.
- App `red`: modelo de `Sector`, `Dispositivo` (compatible con MikroTik y
  Ubiquiti desde ya), `Interfaz` y `Enlace`.
- Panel de administración de Django ya configurado para gestionar todo lo anterior.

## Requisitos previos
- Python 3.10 o superior
- PostgreSQL instalado y corriendo localmente

## Puesta en marcha

1. Crear y activar el entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Crear la base de datos en PostgreSQL:
   ```bash
   psql -U postgres -c "CREATE DATABASE wisp_portal;"
   psql -U postgres -c "CREATE USER wisp_admin WITH PASSWORD 'cambia-esta-contrasena';"
   psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE wisp_portal TO wisp_admin;"
   ```

4. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con la contraseña que usaste en el paso 3
   ```

5. Aplicar migraciones y crear el primer usuario administrador:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
   Cuando te pregunte, después de crear el usuario puedes entrar al admin
   (`/admin/`) y ponerle rol "Administrador" desde ahí — el comando
   `createsuperuser` no pide el rol directamente.

6. Levantar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

7. Abrir en el navegador:
   - `http://127.0.0.1:8000/` → login del portal
   - `http://127.0.0.1:8000/admin/` → panel de administración (gestión de
     clientes, contratos, dispositivos, sectores, etc.)

## Siguiente fase
Cuando confirmes que esto funciona en tu máquina, seguimos con la gestión de
clientes + integración MikroTik (PPPoE y Queues vía API de RouterOS).
