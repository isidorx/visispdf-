import streamlit as st
from PIL import Image
import io
import os
import subprocess
import tempfile
from pypdf import PdfWriter

# --- ARREGLO DE FUENTES: MAGIA INTERNA ---
@st.cache_resource
def refrescar_fuentes():
    # Obligamos al servidor a recargar el catálogo de fuentes para que LibreOffice 
    # reconozca las fuentes métricas (Liberation/Carlito) instaladas en packages.txt
    subprocess.run(['fc-cache', '-f', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

refrescar_fuentes()
# -----------------------------------------

# 1. Configuración básica de la página
st.set_page_config(page_title="VitisPDF+ :3 🎀", page_icon="🌸", layout="centered")

# 2. Inyectamos la Magia Kawaii (CSS para colores y estilo)
st.markdown("""
    <style>
    /* Fondo general (My Melody pink soft) */
    .stApp {
        background-color: #FFF0F5;
    }
    /* Títulos principales (Hatsune Miku Teal) */
    h1, h2, h3 {
        color: #39C5BB !important;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    /* Textos generales (Kuromi dark purple) */
    p, label, .stMarkdown {
        color: #3B314B !important;
        font-size: 16px;
    }
    /* Estilo de los botones */
    .stButton>button {
        background-color: #E4A9E8; /* Lila Kuromi */
        color: white;
        border-radius: 20px;
        border: 2px solid #3B314B;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FFB7D5; /* Rosa My Melody */
        color: #3B314B;
        border: 2px solid #39C5BB;
    }
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #FFFFFF;
        border-radius: 10px 10px 0px 0px;
        color: #39C5BB;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFB7D5 !important;
        color: #3B314B !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Encabezado de la App
st.title("🌸 Bienvenida a VitisPDF+ :3 🎵")
st.write("¡Hola jefa! 🦇 Elige qué necesitas unir hoy y deja que la magia haga el resto.")

# 4. Creamos las pestañas
tab_fotos, tab_words = st.tabs(["📸 Imágenes a PDF", "📝 Words a PDF"])

# ==========================================
# PESTAÑA 1: IMÁGENES A PDF
# ==========================================
with tab_fotos:
    st.subheader("🎀 Convertir múltiples fotos a un solo PDF")
    st.write("Sube tus fotos (boletas, comprobantes, facturas) y se unirán en un solo archivo.")
    
    archivos_fotos = st.file_uploader("Sube tus imágenes aquí 📸", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key="fotos")

    if archivos_fotos:
        st.success(f"🎵 ¡Genial! Has subido {len(archivos_fotos)} foto(s).")
        
        if st.button("✨ Generar PDF con Imágenes ✨", key="btn_fotos"):
            with st.spinner('Uniendo tus fotos con mucho amor... 🌸'):
                lista_imagenes = []
                # Ordenamos alfabéticamente
                archivos_fotos.sort(key=lambda x: x.name)
                
                for archivo in archivos_fotos:
                    img = Image.open(archivo).convert('RGB')
                    lista_imagenes.append(img)
                    
                pdf_bytes = io.BytesIO()
                lista_imagenes[0].save(
                    pdf_bytes, format='PDF', save_all=True, append_images=lista_imagenes[1:]
                )
                pdf_bytes.seek(0)
                
                st.download_button(
                    label="⬇️ Descargar PDF de Imágenes",
                    data=pdf_bytes,
                    file_name="Documento_Imagenes_Unidas.pdf",
                    mime="application/pdf"
                )

# ==========================================
# PESTAÑA 2: WORD A PDF
# ==========================================
with tab_words:
    st.subheader("🦇 Convertir múltiples Words a un solo PDF")
    st.write("Sube tus documentos Word y los apilaremos en un solo PDF conservando el formato original lo mejor posible.")
    
    archivos_words = st.file_uploader("Sube tus archivos Word aquí 📝", type=['docx'], accept_multiple_files=True, key="words")

    if archivos_words:
        st.success(f"🖤 ¡Perfecto! Has subido {len(archivos_words)} archivo(s).")
        
        if st.button("✨ Generar PDF con Words ✨", key="btn_words"):
            with st.spinner('Cocinando tus documentos... esto puede tardar un poquito 🦇'):
                
                # Ordenamos los archivos por nombre
                archivos_words.sort(key=lambda x: x.name)
                
                # Usamos una carpeta temporal en el servidor para trabajar sin dejar basura
                with tempfile.TemporaryDirectory() as temp_dir:
                    merger = PdfWriter()
                    
                    # Guardamos y procesamos cada Word
                    for archivo in archivos_words:
                        word_path = os.path.join(temp_dir, archivo.name)
                        
                        # Escribimos el archivo en el servidor
                        with open(word_path, "wb") as f:
                            f.write(archivo.read())
                            
                        # Convertimos a PDF usando LibreOffice (ahora usando las fuentes métricas)
                        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', word_path, '--outdir', temp_dir], 
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        
                        # Buscamos el PDF recién creado y lo añadimos al unificador
                        pdf_path = word_path.replace('.docx', '.pdf')
                        if os.path.exists(pdf_path):
                            merger.append(pdf_path)
                            
                    # Guardamos el resultado final en memoria
                    pdf_bytes = io.BytesIO()
                    merger.write(pdf_bytes)
                    merger.close()
                    pdf_bytes.seek(0)
                    
                    st.download_button(
                        label="⬇️ Descargar PDF de Documentos",
                        data=pdf_bytes,
                        file_name="Documento_Words_Unidos.pdf",
                        mime="application/pdf"
                    )
