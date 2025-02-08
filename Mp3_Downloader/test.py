import threading
import yt_dlp
import os
import tkinter as tk
from tkinter import messagebox

class YoutubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("400x250")

        # Evento para detener el proceso
        self.stop_event = threading.Event()
        self.download_thread = None  # Variable para el hilo de descarga

        # Etiqueta para mostrar el estado
        self.status_label = tk.Label(root, text="Estado: Esperando acción...", fg="black", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # Campo de entrada para la URL
        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.pack(pady=5)
        self.url_entry.insert(0, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # URL de prueba

        # Botón para iniciar la búsqueda
        self.start_button = tk.Button(root, text="Iniciar Búsqueda", command=self.iniciar_busqueda, bg="green", fg="white", font=("Arial", 10, "bold"))
        self.start_button.pack(pady=5)

        # Botón para detener la búsqueda
        self.stop_button = tk.Button(root, text="Detener Búsqueda", command=self.detener_busqueda, bg="red", fg="white", font=("Arial", 10, "bold"))
        self.stop_button.pack(pady=5)

    def obtener_datos_youtube(self, url):
        """Función que obtiene información del video y permite detenerse"""
        def progress_hook(d):
            """Verifica si se debe detener la descarga"""
            if self.stop_event.is_set():
                raise Exception("🛑 Búsqueda detenida por el usuario.")

        ydl_opts = {
            'progress_hooks': [progress_hook],  # Hook para detener el proceso
            'quiet': True  # Oculta mensajes de `yt_dlp`
        }

        try:
            self.status_label.config(text="🔍 Buscando información...", fg="blue")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            
            if self.stop_event.is_set():
                self.status_label.config(text="⛔ Búsqueda detenida", fg="red")
                return

            # Mostrar información en la interfaz
            video_title = info.get('title', 'Desconocido')
            video_duration = info.get('duration', 'Desconocida')
            video_author = info.get('uploader', 'Desconocido')

            result = f"✅ Video encontrado:\nTítulo: {video_title}\nDuración: {video_duration} segundos\nAutor: {video_author}"
            self.status_label.config(text=result, fg="green")

        except Exception as e:
            self.status_label.config(text=f"⚠ Error: {str(e)}", fg="red")

    def iniciar_busqueda(self):
        """Inicia la búsqueda en un hilo separado"""
        self.stop_event.clear()  # Asegurar que el evento esté limpio antes de iniciar
        url = self.url_entry.get()

        # Verificar si la URL es válida
        if not url.startswith("http"):
            messagebox.showerror("Error", "Ingresa una URL válida de YouTube.")
            return

        # Crear e iniciar el hilo
        self.download_thread = threading.Thread(target=self.obtener_datos_youtube, args=(url,), daemon=True)
        self.download_thread.start()

    def detener_busqueda(self):
        """Detiene la búsqueda en curso"""
        self.stop_event.set()  # Activa la bandera para detener el proceso
        self.status_label.config(text="⛔ Deteniendo búsqueda...", fg="red")
        print("🔴 Se ha solicitado detener la búsqueda.")

# Iniciar la aplicación
root = tk.Tk()
app = YoutubeDownloaderApp(root)
root.mainloop()
