# Importamos las herramientas necesarias de diferentes bibliotecas.
# "Annotated" y "Depends" de FastAPI nos ayudan con la inyección de dependencias.
# "create_engine" de SQLAlchemy nos permiten conectarnos a la base de datos y ejecutar SQL.
# "sessionmaker" y "Session" de SQLAlchemy ORM son para gestionar las "sesiones" o conversaciones con la base de datos.
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# --- Configuración de la Base de Datos ---

# Esta es la "cadena de conexión". Le dice a SQLAlchemy dónde está nuestra base de datos y de qué tipo es.
# En este caso, estamos usando SQLite, que es una base de datos basada en un solo archivo.
# El archivo de la base de datos se llamará "todo.db" y estará en el mismo directorio que nuestro proyecto.
cadena_de_conexion = f"sqlite:///todo.db"

# SQLite, por defecto, solo permite que un hilo (thread) hable con él a la vez.
# Como FastAPI puede usar múltiples hilos, necesitamos decirle a SQLite que permita conexiones desde diferentes hilos.
# Este diccionario de argumentos de conexión se encarga de eso.
connect_args = {"check_same_thread": False}

# Aquí creamos el "motor" (engine) de la base de datos.
# El motor es el punto de entrada principal a la base de datos.
# Utiliza la cadena de conexión para saber a dónde conectarse y los argumentos extra que definimos antes.
engine = create_engine(cadena_de_conexion, connect_args=connect_args)

# Creamos una "fábrica" de sesiones llamada SessionLocal.
# Una sesión es como una conversación temporal con la base de datos. Te permite agrupar una serie de operaciones
# (como leer, insertar, actualizar datos) antes de confirmarlas (hacer "commit").
# - autocommit=False: Las operaciones no se guardan automáticamente. Debemos decirle explícitamente cuándo guardar.
# - autoflush=False: La sesión no enviará automáticamente los cambios a la base de datos antes de cada consulta.
# - bind=engine: Le decimos a esta fábrica de sesiones que debe usar nuestro motor (engine) para crear nuevas sesiones.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# --- Dependencia de FastAPI para la Sesión ---

# Esta es una función "generadora" que FastAPI usará para darnos una sesión de base de datos en cada petición (request).
# Funciona como una "dependencia".
def get_db():
    # Creamos una nueva sesión usando nuestra fábrica de sesiones.
    # El "with" se asegura de que la sesión se cierre correctamente al final, incluso si hay errores.
    with SessionLocal() as session:
        # "yield" es lo que hace a esta función un generador.
        # Entrega la sesión a la función de la ruta que la pidió y pausa su propia ejecución.
        yield session
        # Una vez que la función de la ruta termina, el código aquí se reanuda.
        # En este caso no hay nada que hacer después, porque el "with" ya se encarga de cerrar la sesión.

# Esta es una forma moderna (usando "Annotated") de declarar una dependencia en FastAPI.
# Le decimos a FastAPI: "Cuando veas una variable de tipo SessionDepends en una función de ruta,
# ejecuta la función get_db() y pasa lo que devuelve (la sesión) a esa variable".
# Esto hace que obtener una sesión de base de datos en nuestras rutas sea muy limpio y fácil.
SessionDepends = Annotated[Session, Depends(get_db)]