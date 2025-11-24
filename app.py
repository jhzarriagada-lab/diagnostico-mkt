
import streamlit as st
from fpdf import FPDF
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Scanner de Marca", page_icon="🚀", layout="centered")

# --- 2. ESTILOS PERSONALIZADOS (CSS) ---
# Aquí aplicamos el Azul Marino (#0A2A43) y ajustes finos
st.markdown("""
    <style>
    /* Títulos H1, H2, H3 en Azul Marino Profundo */
    h1, h2, h3 {
        color: #0A2A43 !important;
    }
    
    /* Métricas grandes en Azul Marino */
    [data-testid="stMetricValue"] {
        color: #0A2A43 !important;
    }
    
    /* Botones personalizados (Turquesa con texto blanco) */
    div.stButton > button {
        background-color: #4BB7A1;
        color: white;
        border: none;
        border-radius: 5px;
    }
    div.stButton > button:hover {
        background-color: #3AA690;
        color: white;
    }
    
    /* Ajuste de color texto en la barra lateral (Arena) para que se lea bien */
    [data-testid="stSidebar"] {
        color: #333333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CARGA DEL LOGO EN LA BARRA LATERAL ---
# Intenta buscar 'logo.png', si no está, busca 'logo.jpg'
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
elif os.path.exists("logo.jpg"):
    st.sidebar.image("logo.jpg", use_container_width=True)
else:
    st.sidebar.header("Tu Empresa") # Texto de respaldo si no hay imagen

st.sidebar.markdown("---")
st.sidebar.write("Esta herramienta realiza un diagnóstico 360° de tu presencia digital.")

# --- 4. FUNCIÓN GENERADORA DE PDF ---
def generar_pdf(empresa, puntaje, recomendaciones):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado con color Azul Marino (RGB: 10, 42, 67)
    pdf.set_text_color(10, 42, 67) 
    pdf.set_font("Arial", 'B', 16)
    # encode/decode para manejar tildes básicas
    pdf.cell(0, 10, txt=f"Informe: {empresa}".encode('latin-1', 'replace').decode('latin-1'), ln=1, align='C')
    pdf.ln(5)
    
    # Reset color a negro para el texto normal
    pdf.set_text_color(0, 0, 0)
    
    # Puntaje
    pdf.set_font("Arial", 'B', 12)
    estado = "EXCELENTE" if puntaje > 80 else "BUENO" if puntaje > 50 else "CRITICO"
    pdf.cell(0, 10, txt=f"Puntaje Final: {puntaje}/100 - Estado: {estado}", ln=1, align='L')
    pdf.ln(5)
    
    # Recomendaciones
    pdf.set_font("Arial", 'B', 14)
    # Título en Turquesa (RGB: 75, 183, 161)
    pdf.set_text_color(75, 183, 161)
    pdf.cell(0, 10, txt="Plan de Accion Recomendado:", ln=1, align='L')
    
    pdf.set_text_color(51, 51, 51) # Gris oscuro
    pdf.set_font("Arial", size=11)
    for rec in recomendaciones:
        texto = f"- {rec}"
        pdf.multi_cell(0, 8, txt=texto.encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(2)
            
    return pdf.output(dest='S').encode('latin-1')

# --- 5. INTERFAZ DEL FORMULARIO ---
st.title("🚀 Scanner de Marca 360°")
st.markdown("Diagnóstico profesional de presencia digital e identidad de marca.")

with st.form("audit_form"):
    st.subheader("1. Identidad y Activos")
    
    col1, col2 = st.columns(2)
    with col1:
        identidad = st.radio(
            "¿Tienes una identidad visual definida?",
            ("Sí, manual de marca completo", "Solo tengo un logotipo", "No, uso colores al azar")
        )
    with col2:
        web = st.selectbox("¿Estado de tu sitio web?", 
                           ("No tengo", "Básico / Informativo", "Tienda Online / E-commerce Optimizado"))

    st.divider()
    st.subheader("2. Estrategia de Contenidos")

    frecuencia = st.select_slider(
        "Frecuencia de publicación",
        options=["Casi nunca", "1 vez/semana", "2-3 veces/semana", "Diario"]
    )
    
    calidad = st.slider("Autoevaluación: Calidad de foto/video (1-10)", 1, 10, 5)

    canales = st.multiselect(
        "Canales activos",
        ["Instagram", "LinkedIn", "TikTok", "Facebook", "YouTube", "Email Marketing"]
    )

    st.divider()
    st.subheader("3. Inversión y Gestión")
    
    col3, col4 = st.columns(2)
    with col3:
        inversion = st.radio("Publicidad Pagada (Ads)", ("Nunca", "Esporádica", "Mensual Constante"))
    with col4:
        crm = st.checkbox("¿Usas CRM o Base de Datos organizada?")

    st.markdown("---")
    submitted = st.form_submit_button("📊 Generar Informe Profesional")

# --- 6. LÓGICA DE NEGOCIO Y RESULTADOS ---
if submitted:
    score = 0
    recomendaciones = []

    # Cálculos
    if identidad == "Sí, manual de marca completo": score += 15
    elif identidad == "Solo tengo un logotipo": 
        score += 5
        recomendaciones.append("Identidad: Necesitas definir tipografias y colores, no solo el logo.")
    else: recomendaciones.append("URGENTE: Tu marca no es reconocible. Crea un manual de identidad.")

    if web == "Tienda Online / E-commerce Optimizado": score += 10
    elif web == "Básico / Informativo": score += 5
    else: recomendaciones.append("Web: Un sitio web aumenta tu credibilidad y ventas automaticas.")

    if frecuencia == "Diario": score += 20
    elif frecuencia == "2-3 veces/semana": score += 15
    elif frecuencia == "1 vez/semana": score += 5; recomendaciones.append("Frecuencia: Sube a 3 posts semanales.")
    else: recomendaciones.append("Constancia: Publicar 'casi nunca' mata tu alcance.")

    score += calidad
    if calidad < 6: recomendaciones.append("Contenido: Mejora la iluminacion y audio. La calidad vende.")

    puntos_canales = len(canales) * 4
    score += min(puntos_canales, 20)
    if len(canales) < 2: recomendaciones.append("Diversificacion: No dependas de una sola red social.")

    if inversion == "Mensual Constante": score += 20
    elif inversion == "Esporádica": score += 10
    else: recomendaciones.append("Ads: Invierte aunque sea un monto pequeño en publicidad.")

    if crm: score += 5
    else: recomendaciones.append("Gestion: Implementa un CRM para no perder clientes.")

    score_final = min(score, 100)
    
    # Mostrar Resultados
    st.divider()
    col_res1, col_res2 = st.columns([1, 2])
    
    with col_res1:
        st.metric("Puntaje de Marca", f"{score_final}/100")
        
    with col_res2:
        if score_final >= 80: st.success("Estado: LÍDER DE MERCADO 🏆")
        elif score_final >= 50: st.warning("Estado: EN CRECIMIENTO 🚧")
        else: st.error("Estado: INVISIBLE 👻")
        st.progress(score_final)

    st.write("### 💡 Hoja de Ruta Sugerida")
    for rec in recomendaciones:
        st.info(rec)
    
    # Botón PDF
    pdf_bytes = generar_pdf("Cliente", score_final, recomendaciones)
    st.download_button("📥 Descargar Auditoría PDF", data=pdf_bytes, file_name="Auditoria_Marca.pdf", mime="application/pdf")