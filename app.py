import streamlit as st
import pandas as pd
from fpdf import FPDF

# Configuración básica de la página
st.set_page_config(page_title="Diagnóstico MKT", page_icon="📊")

# --- FUNCIÓN PARA GENERAR PDF ---
def generar_pdf(empresa, puntaje, recomendaciones):
    # Clase PDF personalizada para manejar mejor los caracteres
    pdf = FPDF()
    pdf.add_page()
    
    # Título
    pdf.set_font("Arial", 'B', 16)
    # Usamos encode('latin-1', 'replace') para manejar tildes básicas
    titulo = f"Informe de Diagnostico: {empresa}"
    pdf.cell(200, 10, txt=titulo.encode('latin-1', 'replace').decode('latin-1'), ln=1, align='C')
    pdf.ln(10)
    
    # Puntaje
    pdf.set_font("Arial", 'B', 12)
    texto_puntaje = f"Puntaje de Salud Digital: {puntaje}/100"
    pdf.cell(200, 10, txt=texto_puntaje, ln=1, align='L')
    
    # Estado
    estado = "EXCELENTE" if puntaje > 75 else "MEJORABLE" if puntaje > 40 else "CRITICO"
    pdf.cell(200, 10, txt=f"Estado General: {estado}", ln=1, align='L')
    pdf.ln(10)
    
    # Recomendaciones
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Recomendaciones Clave:", ln=1, align='L')
    
    pdf.set_font("Arial", size=12)
    for rec in recomendaciones:
        # Limpieza básica de texto para el PDF
        texto_rec = f"- {rec}"
        # Multi_cell ajusta el texto largo
        try:
            pdf.multi_cell(0, 10, txt=texto_rec.encode('latin-1', 'replace').decode('latin-1'))
        except:
            pdf.multi_cell(0, 10, txt="- Recomendacion general (caracter no soportado)")
            
    # Retornar el binario del PDF
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFAZ DE USUARIO (WEB) ---
st.title("📊 Diagnóstico de Presencia Digital")
st.markdown("Responde las siguientes preguntas para obtener tu informe y recomendaciones.")

with st.form("marketing_form"):
    st.write("### Datos del Negocio")
    nombre_empresa = st.text_input("Nombre de tu empresa")
    
    st.write("### Estrategia Actual")
    frecuencia = st.selectbox("¿Con qué frecuencia publicas contenido?", 
                              ("Diariamente", "2-3 veces por semana", "1 vez por semana", "Casi nunca"))
    
    canales = st.multiselect("¿En qué redes tienes presencia activa?", 
                             ["Instagram", "LinkedIn", "TikTok", "Facebook", "YouTube", "Email Marketing"])
    
    inversion = st.radio("¿Haces publicidad pagada (Ads)?", 
                         ("Sí, mensualmente", "A veces", "Nunca"))
    
    submitted = st.form_submit_button("Generar Diagnóstico")

# --- LÓGICA DE PUNTUACIÓN ---
if submitted:
    if not nombre_empresa:
        st.error("⚠️ Por favor, ingresa el nombre de tu empresa para continuar.")
    else:
        # 1. Cálculo de puntaje
        score = 0
        if frecuencia == "Diariamente": score += 30
        elif frecuencia == "2-3 veces por semana": score += 20
        elif frecuencia == "1 vez por semana": score += 10
        
        score += len(canales) * 5  # 5 puntos por red social
        
        if inversion == "Sí, mensualmente": score += 40
        elif inversion == "A veces": score += 20
        
        score_final = min(score, 100) # Tope máximo de 100

        # 2. Generar recomendaciones textuales
        lista_recomendaciones = []
        if "Email Marketing" not in canales:
            lista_recomendaciones.append("Implementar Email Marketing para fidelizar clientes.")
        if frecuencia == "Casi nunca":
            lista_recomendaciones.append("Crear un calendario editorial para publicar al menos semanalmente.")
        if inversion == "Nunca":
            lista_recomendaciones.append("Considerar un presupuesto mensual minimo para Ads (Publicidad).")
        if len(canales) < 2:
            lista_recomendaciones.append("Diversificar canales: Depender de una sola red es riesgoso.")
        if score_final < 50:
            lista_recomendaciones.append("Se recomienda una auditoria profesional urgente.")
        
        if not lista_recomendaciones:
            lista_recomendaciones.append("Mantener la estrategia actual y monitorear metricas.")

        # 3. Mostrar resultados en pantalla
        st.divider()
        st.subheader(f"Resultados para {nombre_empresa}")
        
        col1, col2 = st.columns(2)
        col1.metric("Tu Puntaje Digital", f"{score_final}/100")
        
        if score_final > 75:
            col2.success("Estado: EXCELENTE 🚀")
        elif score_final > 40:
            col2.warning("Estado: MEJORABLE ⚠️")
        else:
            col2.error("Estado: CRÍTICO 🚨")

        st.write("#### Tus Recomendaciones:")
        for rec in lista_recomendaciones:
            st.info(rec)

        # 4. Botón de descarga
        st.write("---")
        st.write("#### 📥 Guarda tu reporte")
        
        # Generar PDF
        pdf_bytes = generar_pdf(nombre_empresa, score_final, lista_recomendaciones)
        
        st.download_button(
            label="Descargar Informe PDF",
            data=pdf_bytes,
            file_name=f"Diagnostico_{nombre_empresa}.pdf",
            mime="application/pdf"
        )