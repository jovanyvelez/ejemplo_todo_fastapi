
"""
operaciones_crud.py
Funciones para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre la tabla de tareas en la base de datos.
Cada función está pensada para ser sencilla y fácil de entender para quienes estudian el proyecto.
"""

# Importa herramientas de SQLAlchemy para ejecutar consultas SQL y manejar sesiones.
from sqlalchemy import text
from sqlalchemy.orm import Session


def obtener_todas_las_tareas(db: Session):
    """
    Obtiene todas las tareas almacenadas en la base de datos.
    Devuelve una lista de diccionarios con los campos de cada tarea.
    """
    consulta = db.execute(text("SELECT * FROM tareas"))
    # Convierte cada fila en un diccionario para facilitar su uso en la vista
    return [
        {"id": tarea.id, "nombre": tarea.nombre, "completa": tarea.completa}
        for tarea in consulta
    ]


def crear_nueva_tarea(nombre: str, db: Session):
    """
    Crea una nueva tarea en la base de datos.
    El campo 'completa' se inicializa en 0 (no completada).
    """
    db.execute(
        text("INSERT INTO tareas (nombre, completa) VALUES (:nombre, :completa)"),
        {"nombre": nombre, "completa": 0},
    )
    db.commit()


def eliminar_tarea_por_id(tarea_id: int, db: Session):
    """
    Elimina una tarea específica según su id.
    """
    db.execute(text("DELETE FROM tareas WHERE id = :id"), {"id": tarea_id})
    db.commit()


def eliminar_todas_las_tareas_db(db: Session):
    """
    Elimina todas las tareas de la base de datos.
    Útil para pruebas o reinicio del sistema.
    """
    db.execute(text("DELETE FROM tareas"))
    db.commit()


def obtener_tarea_por_id(tarea_id: int, db: Session):
    """
    Obtiene una tarea específica según su id.
    Devuelve un diccionario con los datos de la tarea, o None si no existe.
    """
    resultado = db.execute(text("SELECT * FROM tareas WHERE id = :id"), {"id": tarea_id}).fetchone()

    if resultado is None:
        return None

    return {"id": resultado.id, "nombre": resultado.nombre, "completa": resultado.completa}


def actualizar_nombre_tarea(tarea_id: int, db: Session, nombre: str):
    """
    Actualiza el nombre (texto) de una tarea específica.
    """
    db.execute(
        text("UPDATE tareas SET nombre = :nombre WHERE id = :id"),
        {"nombre": nombre, "id": tarea_id},
    )
    db.commit()


def toggle_estado_tarea(tarea_id: int, db: Session):
    """
    Invierte el estado 'completa' de la tarea (de 0 a 1 o de 1 a 0).
    Devuelve True si la tarea fue encontrada y actualizada, False si no existe.
    """
    tarea = db.execute(
        text("SELECT completa FROM tareas WHERE id = :id"), {"id": tarea_id}
    ).fetchone()
    if not tarea:
        return False

    # Si la tarea está incompleta (0), la marca como completa (1), y viceversa
    nuevo_estado = 1 if tarea.completa == 0 else 0
    db.execute(
        text("UPDATE tareas SET completa = :completa WHERE id = :id"),
        {"completa": nuevo_estado, "id": tarea_id},
    )
    db.commit()
    return True