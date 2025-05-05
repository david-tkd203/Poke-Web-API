
# Evaluación Técnica - Proyecto Django

Este proyecto es una aplicación web desarrollada en **Django** como parte de una evaluación técnica. Permite el ingreso mediante login, consulta de datos desde una API pública (PokéAPI), procesamiento y visualización de esos datos en una vista protegida.

---

## 🚀 Tecnologías utilizadas

- Python 3.12
- Django 5.2
- Docker & Docker Compose
- PokéAPI (https://pokeapi.co/)
- HTML + Templates de Django
- postgresql (como base de datos por defecto)

---

## 📦 Instalación y requisitos

### Requisitos previos

- Tener instalado:
  - [Docker](https://www.docker.com/)
  - [Docker Compose](https://docs.docker.com/compose/)
  - (Opcional para desarrollo local) Python 3.12+ y `pip`

---

## 🧪 Instalación con Docker (recomendado)

```bash
# Clonar el repositorio o descomprimir los archivos
cd evaluacion_ist/

# Levantar los contenedores
docker-compose up --build
```

Accede a la app en:  
👉 [http://localhost:8000](http://localhost:8000)

---

## 🧰 Instalación manual (modo local sin Docker)

```bash
cd evaluacion_ist/

# Crear entorno virtual
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Migrar la base de datos
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

---

## 🔐 Autenticación

La aplicación requiere login para acceder a las funcionalidades. Se utiliza el sistema de autenticación propio de Django.

### URL de acceso
- Login: [http://localhost:8000/login/](http://localhost:8000/login/)
- Logout: [http://localhost:8000/logout/](http://localhost:8000/logout/)
- Dashboard: [http://localhost:8000/](http://localhost:8000/)

### Usuario de prueba (crear con el comando `createsuperuser`)
Solicitara datos como usuario, correo y contraseña
Si quieres puedes añadirlo desde http://localhost:8000/admin/

---

## 🌐 API utilizada

Se utiliza la **[PokéAPI](https://pokeapi.co/)** para obtener información de Pokémon. Se realiza:

- Fetch inicial de 10 pokémon desde `/pokemon?limit=10`
- Consulta individual de cada pokémon para obtener detalles
- Procesamiento: ordenados por experiencia base (`base_experience`)
- Visualización en tabla

---

## 🧭 Estructura del Proyecto

```
evaluacion_ist/
├── pokemon/              # App principal
│   ├── views.py          # Vistas para dashboard y consumo de API
│   ├── models.py         # Modelos (si fueran necesarios)
│   ├── templates/        # HTML templates (login, dashboard)
│   └── urls.py           # URLs propias de la app
├── evaluacion_ist/       # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## 📄 Notas adicionales

- El consumo de la API se encuentra cacheado para evitar múltiples llamadas consecutivas.
- Se puede extender fácilmente para incluir gráficos, filtros por tipo de pokémon, paginación, etc.
- Configuración de seguridad y despliegue lista para producción al migrar a PostgreSQL y ocultar claves en `.env`.

---


## 🧑‍💻 Autor

David_tkd203

Este proyecto fue desarrollado como parte de una evaluación técnica para una vacante relacionada con desarrollo backend Django.
