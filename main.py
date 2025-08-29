
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import SessionDepends

from operaciones_crud import (
    obtener_todas_las_tareas,
    crear_nueva_tarea,
    eliminar_tarea_por_id,
    obtener_tarea_por_id,
    actualizar_nombre_tarea,
    toggle_estado_tarea,
)


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: SessionDepends):
    """Renderiza la página principal con la lista de tareas."""
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse(request=request, name="index.html", context= {"todos": todos_list})

@app.post("/add", response_class=HTMLResponse)
async def add_todo(request: Request, db: SessionDepends, task: str = Form(...)):
    """Añade una nueva tarea y devuelve la lista actualizada."""
    if task:
        crear_nueva_tarea(task, db)
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse(request=request, name="_todos.html", context={"todos": todos_list})

@app.post("/toggle/{todo_id}", response_class=HTMLResponse)
async def toggle_todo(request: Request, todo_id: int, db:SessionDepends):
    """Cambia el estado 'done' de una tarea y devuelve la lista actualizada."""
    toggle_estado_tarea(todo_id, db)
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("_todos.html", {"request": request, "todos": todos_list})

@app.delete("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_todo(request: Request, todo_id: int, db:SessionDepends):
    """Elimina una tarea y devuelve la lista actualizada."""
    eliminar_tarea_por_id(todo_id, db)
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("_todos.html", {"request": request, "todos": todos_list}) 

@app.get("/edit/{todo_id}", response_class=HTMLResponse)
async def edit_form(request: Request, todo_id: int, db:SessionDepends):
    """Devuelve el formulario para editar una tarea específica."""
    todos_list = obtener_tarea_por_id(todo_id, db)
    if todos_list:
        return templates.TemplateResponse("_edit.html", {"request": request, "todo": todos_list})
    return HTMLResponse(content="", status_code=404)

@app.put("/update/{todo_id}", response_class=HTMLResponse)
async def update_todo(request: Request, todo_id: int,  db:SessionDepends, nombre: str = Form(...)):
    """Actualiza el texto de una tarea y devuelve la lista completa."""
    actualizar_nombre_tarea(todo_id, db, nombre)
    todos_list = obtener_todas_las_tareas(db)
    return templates.TemplateResponse("_todos.html", {"request": request, "todos": todos_list})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
