
# main.py
# Archivo principal de la aplicación Todo App.
# Aquí se definen las rutas y la lógica de interacción entre el usuario, la base de datos y las plantillas HTML.

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Importa la dependencia para obtener la sesión de base de datos
from db import SessionDepends

# Importa las funciones CRUD para manipular las tareas
from operaciones_crud import (
    obtener_todas_las_tareas,      # Obtener todas las tareas
    crear_nueva_tarea,             # Crear una nueva tarea
    eliminar_tarea_por_id,         # Eliminar una tarea por su id
    obtener_tarea_por_id,          # Obtener una tarea específica
    actualizar_nombre_tarea,       # Actualizar el nombre de una tarea
    toggle_estado_tarea,           # Cambiar el estado de completada/no completada
)

# Instancia principal de FastAPI
app = FastAPI()
# Configura el motor de plantillas Jinja2
templates = Jinja2Templates(directory="templates")

# Ruta principal: muestra la lista de tareas
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: SessionDepends):
    """
    Renderiza la página principal con la lista de tareas.
    - request: información de la petición HTTP
    - db: sesión de base de datos
    """
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse(request=request, name="index.html", context={"todos": todos_list})

# Ruta para agregar una nueva tarea
@app.post("/add", response_class=HTMLResponse)
async def add_todo(request: Request, db: SessionDepends, task: str = Form(...)):
    """
    Añade una nueva tarea y devuelve la lista actualizada.
    - task: nombre de la tarea (recibido desde el formulario)
    """
    if task:
        crear_nueva_tarea(task, db)
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse(request=request, name="_todos.html", context={"todos": todos_list})

# Ruta para cambiar el estado de una tarea (completada/no completada)
@app.post("/toggle/{todo_id}", response_class=HTMLResponse)
async def toggle_todo(request: Request, todo_id: int, db: SessionDepends):
    """
    Cambia el estado 'completa' de una tarea y devuelve la lista actualizada.
    - todo_id: id de la tarea a modificar
    """
    toggle_estado_tarea(todo_id, db)
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("_todos.html", {"request": request, "todos": todos_list})

# Ruta para eliminar una tarea
@app.delete("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: int, db: SessionDepends):
    """
    Elimina una tarea y devuelve la lista actualizada.
    - todo_id: id de la tarea a eliminar
    """
    eliminar_tarea_por_id(todo_id, db)
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("_todos.html", {"request": request, "todos": todos_list})

# Ruta para mostrar el formulario de edición de una tarea
@app.get("/edit/{todo_id}", response_class=HTMLResponse)
async def edit_form(request: Request, todo_id: int, db: SessionDepends):
    """
    Devuelve el formulario para editar una tarea específica.
    - todo_id: id de la tarea a editar
    """
    todos_list = obtener_tarea_por_id(todo_id, db)
    if todos_list:
        return templates.TemplateResponse("_edit.html", {"request": request, "todo": todos_list})
    return HTMLResponse(content="", status_code=404)

# Ruta para actualizar el nombre de una tarea
@app.put("/update/{todo_id}", response_class=HTMLResponse)
async def update_todo(request: Request, todo_id: int, db: SessionDepends, nombre: str = Form(...)):
    """
    Actualiza el texto de una tarea y devuelve la lista completa.
    - todo_id: id de la tarea a actualizar
    - nombre: nuevo nombre de la tarea
    """
    actualizar_nombre_tarea(todo_id, db, nombre)
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("_todos.html", {"request": request, "todos": todos_list})


