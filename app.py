import streamlit as st
import yt_dlp
import os
import io

def download_media(url, progress_text, progress_bar, format_option):
    if format_option == "Audio (Mejor Calidad)":
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [(lambda d: mostrar_progreso(d, progress_text, progress_bar))],
            'verbose': True
        }
    elif format_option == "Video MP4 (Alta Calidad)":
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [(lambda d: mostrar_progreso(d, progress_text, progress_bar))],
            'verbose': True
        }
    elif format_option == "Video MP4 (720p)":
        ydl_opts = {
            'format': 'best[height<=720][ext=mp4]',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [(lambda d: mostrar_progreso(d, progress_text, progress_bar))],
            'verbose': True
        }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            progress_text.text("Obteniendo información del video...")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return info['title'], filename
        except Exception as e:
            st.error(f"Error específico: {str(e)}")
            raise e

def mostrar_progreso(d, progress_text, progress_bar):
    if d['status'] == 'downloading':
        try:
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 0)
            if total > 0:
                percentage = (downloaded / total) * 100
                progress_bar.progress(int(percentage))
                progress_text.text(f"Descargando: {percentage:.1f}% ({downloaded}/{total} bytes)")
        except:
            progress_text.text("Descargando...")
    elif d['status'] == 'finished':
        progress_text.text('Finalizando descarga...')

def main():
    st.title("YouTube Downloader Pro")
    st.subheader("Descarga videos y audio en alta calidad")
    
    url = st.text_input("📝 Ingresa la URL del video:")
    
    format_options = [
        "Audio (Mejor Calidad)",
        "Video MP4 (Alta Calidad)",
        "Video MP4 (720p)"
    ]
    
    format_choice = st.selectbox(
        "Selecciona el formato de descarga:",
        format_options
    )
    
    if st.button("⬇️ Descargar"):
        if url:
            try:
                progress_text = st.empty()
                progress_bar = st.progress(0)
                progress_text.text("Iniciando descarga...")
                
                titulo, filename = download_media(url, progress_text, progress_bar, format_choice)
                
                progress_bar.progress(100)
                progress_text.text("¡Descarga completada!")
                
                # Leer el archivo y crear el botón de descarga
                with open(filename, 'rb') as file:
                    st.download_button(
                        label="📥 Descargar archivo",
                        data=file,
                        file_name=filename,
                        mime="application/octet-stream"
                    )
                
                # Eliminar el archivo temporal
                os.remove(filename)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Ingresa una URL válida")

if __name__ == "__main__":
    main()
