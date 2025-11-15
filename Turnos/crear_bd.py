import sqlite3

conn = sqlite3.connect("turnos.db")
cur = conn.cursor()

# Tabla de pacientes
cur.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL
);
""")

# Tabla de clínicas
cur.execute("""
CREATE TABLE IF NOT EXISTS clinicas (
    id_clinica INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);
""")

# Tabla de turnos
cur.execute("""
CREATE TABLE IF NOT EXISTS turnos (
    id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER NOT NULL,
    id_clinica INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_clinica) REFERENCES clinicas(id_clinica)
);
""")

# Tabla de reasignaciones
cur.execute("""
CREATE TABLE IF NOT EXISTS reasignaciones (
    id_reasignacion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_turno INTEGER NOT NULL,
    clinica_anterior INTEGER NOT NULL,
    clinica_nueva INTEGER NOT NULL,
    motivo TEXT NOT NULL,
    fecha_cambio TEXT NOT NULL,
    hora_cambio TEXT NOT NULL,
    FOREIGN KEY (id_turno) REFERENCES turnos(id_turno)
);
""")

conn.commit()
conn.close()

print("Base de datos y tablas creadas correctamente.")
