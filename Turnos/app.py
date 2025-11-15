import streamlit as st
import sqlite3
from datetime import datetime

# -----------------------------------------------------
#             CONEXIÓN A LA BASE DE DATOS
# -----------------------------------------------------
def get_connection():
    conn = sqlite3.connect("turnos.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Obtener turnos
def obtener_turnos():
    conn = get_connection()
    turnos = conn.execute("""
        SELECT t.id_turno,
               p.nombre || ' ' || p.apellido AS paciente,
               c.nombre AS clinica,
               t.fecha,
               t.hora,
               t.id_clinica,
               p.id_paciente
        FROM turnos t
        JOIN pacientes p ON p.id_paciente = t.id_paciente
        JOIN clinicas c ON c.id_clinica = t.id_clinica
        ORDER BY t.fecha, t.hora
    """).fetchall()
    conn.close()
    return turnos

# Obtener clínicas
def obtener_clinicas():
    conn = get_connection()
    clinicas = conn.execute("SELECT id_clinica, nombre FROM clinicas").fetchall()
    conn.close()
    return clinicas

# Historial por paciente
def obtener_reasignaciones_por_paciente(nombre_paciente):
    conn = get_connection()
    reas = conn.execute("""
        SELECT r.id_reasignacion,
               t.fecha AS fecha_turno,
               c1.nombre AS clinica_anterior,
               c2.nombre AS clinica_nueva,
               r.motivo,
               r.fecha_cambio,
               r.hora_cambio
        FROM reasignaciones r
        JOIN turnos t ON t.id_turno = r.id_turno
        JOIN clinicas c1 ON c1.id_clinica = r.clinica_anterior
        JOIN clinicas c2 ON c2.id_clinica = r.clinica_nueva
        JOIN pacientes p ON p.id_paciente = t.id_paciente
        WHERE p.nombre || ' ' || p.apellido LIKE ?
        ORDER BY r.fecha_cambio DESC, r.hora_cambio DESC
    """, (f"%{nombre_paciente}%",)).fetchall()
    conn.close()
    return reas

# Guardar reasignación
def guardar_reasignacion(id_turno, clinica_anterior, clinica_nueva, motivo):
    conn = get_connection()
    cursor = conn.cursor()

    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    cursor.execute("""
        INSERT INTO reasignaciones 
        (id_turno, clinica_anterior, clinica_nueva, motivo, fecha_cambio, hora_cambio)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_turno, clinica_anterior, clinica_nueva, motivo, fecha, hora))

    cursor.execute("""
        UPDATE turnos 
        SET id_clinica = ?
        WHERE id_turno = ?
    """, (clinica_nueva, id_turno))

    conn.commit()
    conn.close()


# -----------------------------------------------------
#                INTERFAZ STREAMLIT
# -----------------------------------------------------
st.set_page_config(page_title="Gestión de Turnos", page_icon="📋", layout="wide")
st.title("📋 Gestión de Turnos - Reasignación entre Clínicas")

# Estilo
st.markdown("""
<style>
.stButton>button {
    background-color: #617073;
    color: white;
    border-radius: 8px;
    padding: 6px 20px;
}
.stButton>button:hover {
    background-color: #4e5a5c;
}
</style>
""", unsafe_allow_html=True)

turnos = obtener_turnos()
clinicas = obtener_clinicas()

# -----------------------------------------------------
#                      FILTROS
# -----------------------------------------------------
st.subheader("🔍 Búsqueda y Filtros")

col_f1, col_f2, col_f3 = st.columns([2,2,2])

buscar_paciente = col_f1.text_input("Buscar por paciente:")

lista_clinicas = ["Todas"] + [c["nombre"] for c in clinicas]
filtro_clinica = col_f2.selectbox("Filtrar por clínica:", lista_clinicas)

filtro_fecha = col_f3.date_input("Filtrar por fecha:", value=None)

# Aplicar filtros
turnos_filtrados = turnos

# Filtro por paciente
if buscar_paciente.strip() != "":
    turnos_filtrados = [t for t in turnos_filtrados if buscar_paciente.lower() in t["paciente"].lower()]

# Filtro por clínica
if filtro_clinica != "Todas":
    turnos_filtrados = [t for t in turnos_filtrados if t["clinica"] == filtro_clinica]

# Filtro por fecha
if filtro_fecha:
    fecha_str = filtro_fecha.strftime("%Y-%m-%d")
    turnos_filtrados = [t for t in turnos_filtrados if t["fecha"] == fecha_str]


# -----------------------------------------------------
#     HISTORIAL DE REASIGNACIONES DEL PACIENTE
# -----------------------------------------------------
if buscar_paciente.strip() != "":
    st.subheader("📂 Historial de Reasignaciones del Paciente")

    historial = obtener_reasignaciones_por_paciente(buscar_paciente)

    if not historial:
        st.info("Este paciente no tiene reasignaciones registradas.")
    else:
        for h in historial:
            with st.container(border=True):
                st.write(f"🔄 **Reasignación ID:** {h['id_reasignacion']}")
                st.write(f"📅 Fecha del turno: {h['fecha_turno']}")
                st.write(f"➡ De: **{h['clinica_anterior']}** → **{h['clinica_nueva']}**")
                st.write(f"📝 Motivo: {h['motivo']}")
                st.write(f"📆 Cambio realizado: {h['fecha_cambio']} — 🕒 {h['hora_cambio']}")


# -----------------------------------------------------
#               LISTA DE TURNOS
# -----------------------------------------------------
st.subheader("📆 Lista de Turnos")

if not turnos_filtrados:
    st.warning("No hay turnos con los filtros aplicados.")
else:
    for t in turnos_filtrados:
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([3,2,2,2,1])

            col1.write(f"👤 **{t['paciente']}**")
            col2.write(f"🏥 {t['clinica']}")
            col3.write(f"📅 {t['fecha']}")
            col4.write(f"⏰ {t['hora']}")

            if col5.button("Reasignar", key=f"btn_{t['id_turno']}"):
                st.session_state["reasignar"] = t


# -----------------------------------------------------
#            FORMULARIO DE REASIGNACIÓN
# -----------------------------------------------------
if "reasignar" in st.session_state:
    st.markdown("---")
    st.subheader("🔄 Reasignar Turno")

    turno = st.session_state["reasignar"]

    st.markdown(f"""
    **Paciente:** {turno['paciente']}  
    **Clínica actual:** 🏥 {turno['clinica']}  
    **Fecha:** {turno['fecha']} — **Hora:** {turno['hora']}
    """)

    opciones = {c["nombre"]: c["id_clinica"] for c in clinicas if c["id_clinica"] != turno["id_clinica"]}

    nueva_clinica_nombre = st.selectbox("Nueva clínica:", list(opciones.keys()))
    nueva_clinica_id = opciones[nueva_clinica_nombre]

    motivo = st.text_area("Motivo de la reasignación (obligatorio)", max_chars=200)

    colA, colB = st.columns([1,1])

    if colA.button("✔ Guardar"):
        if motivo.strip() == "":
            st.error("⚠ Debe escribir un motivo.")
        else:
            guardar_reasignacion(
                id_turno=turno["id_turno"],
                clinica_anterior=turno["id_clinica"],
                clinica_nueva=nueva_clinica_id,
                motivo=motivo
            )
            st.success("Turno reasignado correctamente.")
            del st.session_state["reasignar"]
            st.rerun()

    if colB.button("✖ Cancelar"):
        del st.session_state["reasignar"]
        st.rerun()
