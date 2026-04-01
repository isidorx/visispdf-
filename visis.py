import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="App Gastronómica", page_icon="📝")

st.title("📸 Cierre de Turno: Fotos a PDF")
st.write("Sube las fotos de tus boletas Z, facturas o comprobantes. El sistema las unirá en un solo documento listo para tu reporte de finanzas.")

# Botón para subir archivos
archivos_subidos = st.file_uploader("Sube o arrastra tus fotos aquí", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if archivos_subidos:
    st.success(f"¡Excelente! Has subido {len(archivos_subidos)} foto(s).")
    
    if st.button("Generar PDF de Cierre"):
        with st.spinner('Cocinando tu documento...'):
            lista_imagenes = []
            
            for archivo in archivos_subidos:
                # Abrimos y aseguramos el formato de color correcto
                img = Image.open(archivo).convert('RGB')
                lista_imagenes.append(img)
                
            # Creamos el PDF en la memoria virtual
            pdf_bytes = io.BytesIO()
            lista_imagenes[0].save(
                pdf_bytes, format='PDF', save_all=True, append_images=lista_imagenes[1:]
            )
            pdf_bytes.seek(0)
            
            st.download_button(
                label="⬇️ Descargar Reporte en PDF",
                data=pdf_bytes,
                file_name="Reporte_Finanzas_Fotos.pdf",
                mime="application/pdf"
            )
