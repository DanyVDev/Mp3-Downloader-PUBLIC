import threading
import yt_dlp
import os
import json
from tkinter import Label, Button
from datetime import datetime
from Utils import utils

class Youtube_Downloader:
    def __init__(self, listFrame, infoFrame, statusLabel):
        CURRENT_FILE = os.path.dirname(os.path.abspath(__file__))

        # Ruta del archivo para guardar la playlist
        self.dataSavedFile = os.path.join(CURRENT_FILE, 'Data', 'Playlist_LogFile.txt')
        self.jsonSavedFile = os.path.join(CURRENT_FILE, 'Data', 'Playlist.json')

        self.infoIcofile = utils.cargar_imagen_tkinter(os.path.join(CURRENT_FILE, 'Image', '1176.png'))

        self.playlist = []
        self.listFrame = listFrame
        self.infoFrame = infoFrame
        self.statusLabel = statusLabel
        self.playlistInfoSaved = []

        # Crear la carpeta "Data" si no existe
        if not os.path.exists(os.path.join(CURRENT_FILE, 'Data')):
            os.makedirs(os.path.join(CURRENT_FILE, 'Data'))

        # Evento para detener la descarga
        self.stop_event = threading.Event()
        self.download_thread = None  # Variable para manejar el hilo de descarga

    def obtener_datos_youtube(self, url, mode='REQUEST'):
        """Obtiene información del video en un hilo separado y permite detenerse."""
        def search_info(url):
            ydl_opts = {
                'progress_hooks': [progress_hook]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
            return info

        try:
            if self.stop_event.is_set():  # Detener si el usuario cancela
                return

            info = search_info(url)

            if self.stop_event.is_set():
                return

            if mode == 'RESPONSE':
                data = {
                    'Title': info.get('title'),
                    'Duration': f"{info.get('duration')} seconds",
                    'Author': info.get('uploader'),
                    'Publication_date': info.get('upload_date'),
                    'Views': info.get('view_count'),
                    'URL': url
                }

                self.playlist.append(url)
                self.playlistInfoSaved.append(data)

                with open(self.dataSavedFile, 'a') as f:
                    currentDateTime = str(datetime.now())
                    f.write(currentDateTime + ': ' + json.dumps(data) + ',' + '\n')

                if os.path.exists(self.jsonSavedFile):
                    with open(self.jsonSavedFile, 'r+') as f:
                        try:
                            existing_data = json.load(f)
                        except json.JSONDecodeError:
                            existing_data = []
                        existing_data.append(data)
                        f.seek(0)
                        json.dump(existing_data, f, indent=4)
                else:
                    with open(self.jsonSavedFile, 'w') as f:
                        json.dump([data], f, indent=4)

                print(f"Datos guardados en {self.jsonSavedFile}")
                return data['Title']

        except Exception as e:
            self.statusLabel.config(text=f"Error: {str(e)}", fg="red")

    def agregar_a_playlist(self, url):
        """Ejecuta obtener_datos_youtube en un hilo separado."""
        self.stop_event.clear()  # Asegurar que el evento esté limpio antes de iniciar

        hilo = threading.Thread(target=self.obtener_datos_youtube, args=(url, 'RESPONSE'), daemon=True)
        hilo.start()

    def download_youtube_audio(self):
        """Descarga los audios de la playlist en un hilo separado y permite detener la ejecución."""
        def download():
            CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
            output_folder = os.path.join(CURRENT_FOLDER, 'downloads')

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    },
                ],
                'quiet': False,
            }

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for index, url in enumerate(self.playlist):
                    if self.stop_event.is_set():  # Detener antes de descargar el siguiente video
                        self.statusLabel.config(text="Descarga detenida", fg="red")
                        print("Descarga detenida por el usuario.")
                        return  # Sale de la función inmediatamente

                    try:
                        info = ydl.extract_info(url, download=True)
                        video_title = info.get('title', 'Desconocido')
                        self.statusLabel.config(text=f'Descarga completa: {video_title}', fg='green')
                        print(f"Descarga completada: {video_title}")

                    except Exception as e:
                        self.statusLabel.config(text=f"Fallo al descargar {url}", fg='red')
                        print(f"Error al descargar {url}: {e}")

        self.stop_event.clear()  # Asegurar que el evento esté limpio antes de iniciar
        self.download_thread = threading.Thread(target=download, daemon=True)
        self.download_thread.start()

    def detener_descarga(self):
        """Detiene la descarga en curso inmediatamente antes del siguiente video."""
        self.stop_event.set()  # Activa el evento de parada
        self.statusLabel.config(text="Deteniendo descarga...", fg="red")
        print("Se solicitó la detención de la descarga.")
            
    def clear_playlist(self):
        with open(self.jsonSavedFile, "w") as archivo:
            json.dump([], archivo)
        
        self.playlistInfoSaved = []
        self.playlist = []

        self.actualizar_playlist()