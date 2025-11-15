📋 Gestión de Turnos – Reasignación entre Clínicas

Aplicación web desarrollada con Streamlit y SQLite para gestionar turnos médicos, filtrar citas y realizar reasignaciones entre clínicas.
Incluye también un módulo para visualizar el historial de cambios con motivo, fecha y hora del movimiento.

🚀 Características principales

✔️ Visualización completa de los turnos registrados

✔️ Filtro por paciente, clínica o fecha

✔️ Reasignación rápida de un turno a otra clínica

✔️ Registro histórico de cambios de clínica

✔️ Interfaz moderna y fácil de usar

✔️ Base de datos local en SQLite

📁 Estructura del Proyecto
📦 Turnos
│
├── app.py                # Aplicación principal en Streamlit
├── crear_bd.py           # Script para crear la base de datos y tablas
├── insertar_datos.py     # Script opcional para insertar datos iniciales
├── turnos.db             # Archivo SQLite con los datos
└── README.md

🛠️ Requisitos

Debe estar instalado:

Python 3.8 o superior

Streamlit

SQLite (ya viene con Python)

Instalación de dependencias:

pip install streamlit

▶️ Cómo ejecutar la aplicación

1️⃣ Abrir CMD o PowerShell
2️⃣ Ir al directorio del proyecto:

cd C:\Users\strea\Desktop\Turnos


3️⃣ Ejecutar el servidor de Streamlit:

streamlit run app.py


4️⃣ Se abrirá automáticamente en tu navegador.

🗄️ Base de datos

La aplicación usa una base local llamada turnos.db, generada por crear_bd.py.

📌 Tabla: turnos
Campo	Tipo	Descripción
id_turno	INTEGER	ID del turno
paciente	TEXT	Nombre del paciente
clinica_actual	INTEGER	ID de la clínica
fecha	TEXT	Fecha de la cita
hora	TEXT	Hora de la cita
📌 Tabla: reasignaciones
Campo	Tipo	Descripción
id_reasignacion	INTEGER	ID del cambio
id_turno	INTEGER	Turno reasignado
clinica_anterior	INTEGER	Antes
clinica_nueva	INTEGER	Después
motivo	TEXT	Razón del cambio
fecha_cambio	TEXT	Fecha del movimiento
hora_cambio	TEXT	Hora del movimiento
✨ Funciones Principales en la App
🔎 obtener_turnos()

Devuelve la lista de turnos con filtros aplicados.

🔄 reasignar_turno()

Guarda una reasignación y actualiza el turno en la tabla principal.

📑 obtener_historial()

Muestra los cambios realizados para un paciente en específico.

💻 Ejemplo de Uso

Seleccionar un paciente

Ver su información actual

Elegir nueva clínica

Añadir motivo

Guardar → Automáticamente se registra en historial

🧑‍⚕️ Propósito del Sistema

El sistema está diseñado para uso administrativo en clínicas u hospitales que necesitan gestionar turnos y reasignarlos según disponibilidad, residencia del paciente o cambios internos.
