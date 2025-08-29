# Proyecto: Todo App con FastAPI, HTMX y SQLite

Este proyecto es una aplicación web de lista de tareas (ToDo) construida con **FastAPI** como backend, **HTMX** para interactividad frontend y **SQLite** como base de datos. Está pensado para personas que desean estudiar cómo se integran estas tecnologías en una aplicación moderna, sencilla y funcional.

## Objetivos de Estudio
- Comprender la estructura de un proyecto FastAPI.
- Aprender a usar HTMX para interacciones dinámicas sin recargar la página.
- Analizar operaciones CRUD con SQLAlchemy y SQLite.
- Explorar la integración de plantillas Jinja2.

## Estructura del Proyecto

```
├── db.py                # Configuración y conexión a la base de datos SQLite
├── main.py              # Rutas y lógica principal de la API con FastAPI
├── operaciones_crud.py  # Funciones CRUD para la tabla de tareas
├── requirements.txt     # Dependencias del proyecto
├── pyproject.toml       # Configuración del proyecto y dependencias
├── todo.db              # Archivo de la base de datos SQLite
├── templates/           # Archivos HTML con Jinja2 y HTMX
│   ├── index.html       # Página principal
│   ├── _todos.html      # Fragmento de lista de tareas
│   ├── _edit.html       # Formulario de edición de tarea
│   └── ejemplo.html     # Ejemplo de estilos y estructura
└── README.md            # Documentación del proyecto
```

## Tecnologías Utilizadas
- **FastAPI**: Framework moderno para construir APIs con Python.
- **HTMX**: Biblioteca JS para interacciones AJAX sencillas.
- **Jinja2**: Motor de plantillas para HTML dinámico.
- **SQLAlchemy**: ORM para operaciones con la base de datos.
- **SQLite**: Base de datos ligera y fácil de usar.

## Descripción Técnica

- El backend expone rutas para crear, leer, actualizar y eliminar tareas.
- Las vistas HTML usan Jinja2 para renderizar datos y HTMX para actualizar partes de la página sin recargar.
- La base de datos almacena las tareas con campos: `id`, `nombre`, `completa`.
- El código está comentado para facilitar el estudio y la comprensión.

## Cómo Ejecutar el Proyecto

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   pip install "fastapi[standard]" sqlalchemy
   ```
2. Ejecuta el servidor:
   ```bash
   fastapi dev main.py
   ```
3. Abre tu navegador en [http://localhost:8000](http://localhost:8000)

## Archivos Clave
- **main.py**: Define las rutas y la lógica principal de la API.
- **operaciones_crud.py**: Implementa las funciones para manipular las tareas en la base de datos.
- **db.py**: Configura la conexión y la sesión con SQLite.
- **templates/**: Contiene los archivos HTML y fragmentos usados por Jinja2 y HTMX.

## Para Estudiar
- Revisa los comentarios en el código fuente para entender cada parte.
- Modifica las rutas o el HTML para experimentar con HTMX y FastAPI.
- Prueba agregar nuevas funcionalidades (filtros, fechas, usuarios, etc.)

## Créditos y Licencia
Este proyecto es educativo y puede ser modificado libremente para fines de aprendizaje.
