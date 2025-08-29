"""Operaciones CRUD para la tabla de tareas."""
from sqlalchemy import text
from sqlalchemy.orm import Session


def obtener_todas_las_tareas(db: Session):
    """Obtener todas las tareas como lista de dicts."""
    consulta = db.execute(text("SELECT * FROM tareas"))
    return [
        {"id": tarea.id, "nombre": tarea.nombre, "completa": tarea.completa}
        for tarea in consulta
    ]


def crear_nueva_tarea(nombre: str, db: Session):
    """Crear una nueva tarea."""
    db.execute(
        text("INSERT INTO tareas (nombre, completa) VALUES (:nombre, :completa)"),
        {"nombre": nombre, "completa": 0},
    )
    db.commit()


def eliminar_tarea_por_id(tarea_id: int, db: Session):
    """Eliminar una tarea específica por id."""
    db.execute(text("DELETE FROM tareas WHERE id = :id"), {"id": tarea_id})
    db.commit()


def eliminar_todas_las_tareas_db(db: Session):
    """Eliminar todas las tareas."""
    db.execute(text("DELETE FROM tareas"))
    db.commit()


def obtener_tarea_por_id(tarea_id: int, db: Session):
    """Obtener una tarea específica por id (Row o None)."""
    resultado = db.execute(text("SELECT * FROM tareas WHERE id = :id"), {"id": tarea_id}).fetchone()

    if resultado is None:
        return None

    return {"id": resultado.id, "nombre": resultado.nombre, "completa": resultado.completa}


def actualizar_nombre_tarea(tarea_id: int, db: Session, nombre: str):
    """Actualizar el nombre de una tarea."""
    db.execute(
        text("UPDATE tareas SET nombre = :nombre WHERE id = :id"),
        {"nombre": nombre, "id": tarea_id},
    )
    db.commit()


def toggle_estado_tarea(tarea_id: int, db: Session):
    """Invertir el estado 'completa' de la tarea. Devuelve True si se actualizó."""
    tarea = db.execute(
        text("SELECT completa FROM tareas WHERE id = :id"), {"id": tarea_id}
    ).fetchone()
    if not tarea:
        return False

    nuevo_estado = 1 if tarea.completa == 0 else 0
    db.execute(
        text("UPDATE tareas SET completa = :completa WHERE id = :id"),
        {"completa": nuevo_estado, "id": tarea_id},
    )
    db.commit()
    return True