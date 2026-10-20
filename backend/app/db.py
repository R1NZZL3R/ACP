import sqlite3


def conexion(app):
    con = sqlite3.connect(app.config["DB_PATH"])
    con.row_factory = sqlite3.Row
    return con


def iniciar_db(app):
    # SQLite basta para guardar usuarios y mensajes de las páginas.
    with conexion(app) as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                clave_hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL,
                asunto TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                fecha TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
