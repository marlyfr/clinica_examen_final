import sqlite3

conn = sqlite3.connect("turnos.db")
cur = conn.cursor()

# Pacientes
cur.execute("INSERT INTO pacientes (nombre, apellido) VALUES ('Juan', 'Pérez')")
cur.execute("INSERT INTO pacientes (nombre, apellido) VALUES ('Ana', 'López')")

# Clínicas
cur.execute("INSERT INTO clinicas (nombre) VALUES ('Clínica 1')")
cur.execute("INSERT INTO clinicas (nombre) VALUES ('Clínica 2')")

# Turnos
cur.execute("INSERT INTO turnos (id_paciente, id_clinica, fecha, hora) VALUES (1, 1, '2025-02-10', '08:30')")
cur.execute("INSERT INTO turnos (id_paciente, id_clinica, fecha, hora) VALUES (2, 2, '2025-02-11', '09:00')")

conn.commit()
conn.close()

print("Datos insertados correctamente.")
