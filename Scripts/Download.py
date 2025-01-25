import yt_dlp
from tkinter import Tk, Label, Button, Frame
import os

class Youtube_Downloader:
    def __init__(self, listFrame, infoFrame):
        self.playlist = []
        self.listFrame = listFrame
        self.infoFrame = infoFrame

    def obtener_datos_youtube(self, mode='REQUEST'):
        """
        Obtiene datos del video de YouTube usando yt-dlp.

        Parámetros:
            mode (str): Puede ser 'REQUEST' para mostrar información o 'RESPONSE' para obtener el título.
        """
        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)

            if mode == 'REQUEST':
                for widget in self.infoFrame.winfo_children():
                    widget.destroy()

                data = f'''Name: {info.get('title')}
Duration: {info.get('duration')} seconds
Author: {info.get('uploader')}
Publication date: {info.get('upload_date')}
Views: {info.get('view_count')}
URL: {self.url}
'''
                self.infoLabel = Label(self.infoFrame, text=data, wraplength=300, justify="left", anchor="nw")
                self.infoLabel.pack()

            elif mode == 'RESPONSE':
                return info.get('title')

        except Exception as e:
            if mode == 'REQUEST':
                self.infoLabel.config(text=f"Error: {str(e)}", wraplength=400, justify="left", anchor="nw")
            elif mode == 'RESPONSE':
                return f"Error: {str(e)}"

    def agregar_a_playlist(self, url, infoLabel):
        """
        Agrega un video de YouTube a la playlist y actualiza la interfaz.
        """
        self.url = url
        self.infoLabel = infoLabel

        # Obtiene el nombre del video
        name = self.obtener_datos_youtube('RESPONSE')
        if "Error" in name:
            print(f"No se pudo obtener la información del video: {name}")
            return

        self.playlist.append(url)

        # Actualiza la lista de reproducción en la interfaz
        def update_playlist():
            for widget in self.listFrame.winfo_children():
                widget.destroy()

            for index, url in enumerate(self.playlist):
                video_name = name if len(name) <= 42 else f"{name[:42]}..."
                label = Label(self.listFrame, text=video_name, anchor="w", justify="left", wraplength=380, bg='white')
                label.grid(row=index, column=0, sticky="w", padx=5, pady=2)

                info_button = Button(self.listFrame, text='info', command=lambda url=url: self.obtener_datos_youtube('REQUEST'))
                info_button.grid(row=index, column=1, sticky="w", padx=5, pady=2)

        update_playlist()

    def download_youtube_audio(self, progress_callback=None):      


        CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(CURRENT_FOLDER, 'downloads')

        # Opciones de configuración para yt_dlp
        ydl_opts = {
            'format': 'bestaudio/best',  # Descargar solo la mejor calidad de audio
            'outtmpl': f'{output_folder}/%(title)s.%(ext)s',  # Plantilla para nombres de archivo
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',  # Calidad de audio
                },
            ],
            'quiet': False,  # Mostrar progreso en la terminal
        }

        # Crear la carpeta de salida si no existe
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Descargar cada URL en la lista
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            total_videos =len(self.playlist)
            for index, url in enumerate(self.playlist):
                try:
                    ydl.download([url])

                    if progress_callback:
                        progress = int(((index + 1) / total_videos) * 100)
                        progress_callback(progress)
                except Exception as e:
                    print(f"Error al descargar {url}: {e}") 

if __name__ == '__main__':
    root = Tk()
    root.geometry("800x600")

    # Marco principal
    main_frame = Frame(root, width=800, height=600)
    main_frame.pack()

    # Marco de lista con tamaño fijo
    list_frame = Frame(main_frame, width=200, height=580, bg='lightgray')
    list_frame.pack_propagate(False)  # Evita que el tamaño del frame cambie dinámicamente
    list_frame.place(x=10, y=10)

    # Marco de información con tamaño fijo
    info_frame = Frame(main_frame, width=370, height=580, bg='white', relief='sunken', bd=2)
    info_frame.pack_propagate(False)  # Evita que el tamaño del frame cambie dinámicamente
    info_frame.place(x=420, y=10)

    # Etiqueta dentro del marco de información
    info_label = Label(info_frame, text="No data loaded", bg='white', wraplength=350, justify="left", anchor="w")
    info_label.pack(fill='both', expand=True)

    downloader = Youtube_Downloader(list_frame)

    example_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    downloader.agregar_a_playlist(example_url, info_label)

    root.mainloop()
