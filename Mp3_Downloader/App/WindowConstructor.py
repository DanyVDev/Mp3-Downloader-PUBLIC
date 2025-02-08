from tkinter import Tk, Frame, Menu, messagebox, Entry, Button, Label, Canvas, Scrollbar
from Utils import dependency_checker
from Download import Youtube_Downloader
import threading


class Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Mp3 Downloader ALFA")
        self.root.geometry("700x500")
        self.root.configure(bg="gray")
        root.resizable(False, False)

        # Crear la interfaz antes de inicializar el downloader
        self.create_layout()

        # Inicializa el objeto Youtube_Downloader con los frames correctamente definidos
        # Se usa scrollable_list_frame en lugar de showList_frame
        self.downloader = Youtube_Downloader(self.scrollable_list_frame, self.showInfo_frame, self.update_status)

        dependencies = ['tkinter', 'yt_dlp']
        dependency_checker.verificar_e_instalar_dependencias(dependencies)

    def add_to_list(self):
        # Actualizar el texto del statusLabel antes de iniciar el proceso
        self.update_status.config(text="Agregando...", fg='black')
        self.root.update()  # Forzar la actualización de la interfaz gráfica

        videoURL = self.inputURL.get().strip()
        if videoURL:

            thread_createPlaylist = threading.Thread(target=self.downloader.agregar_a_playlist, args=(videoURL,))
            thread_createPlaylist.start()

            #self.downloader.agregar_a_playlist(videoURL)
            self.inputURL.delete(0, 'end')

        # Borrar el texto del statusLabel al finalizar el proceso
        self.update_status.config(text="")


    def create_layout(self):
        # Marco principal
        self.main_frame = Frame(self.root, bg='lightgray', width=700, height=500)
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(fill='both', expand=False, padx=10, pady=10)

        # Marco de entrada de datos
        self.input_frame = Frame(self.main_frame, bg='lightgray', height=50)
        self.input_frame.pack(side='top', fill='x', expand=False)

        # Marco de información
        self.showInfo_frame = Frame(self.main_frame, bg='white', width=320, height=450)
        self.showInfo_frame.pack_propagate(False)
        self.showInfo_frame.pack(side='right', padx=(5, 10), pady=10)

        # Canvas para el marco desplazable
        self.canvas_list = Canvas(self.main_frame, bg='white', width=340, height=450)
        self.canvas_list.pack(side='left', fill='both', expand=True, padx=(10, 5), pady=10)

        # Scrollbar para el canvas
        self.scrollbar_list = Scrollbar(self.canvas_list, orient="vertical", command=self.canvas_list.yview)
        self.scrollbar_list.pack(side='right', fill='y')

        # Configuración del canvas con el scrollbar
        self.canvas_list.configure(yscrollcommand=self.scrollbar_list.set)

        # Frame interno desplazable dentro del canvas
        self.scrollable_list_frame = Frame(self.canvas_list, bg='white')
        self.scrollable_list_frame.bind("<Configure>", lambda e: self.canvas_list.configure(scrollregion=self.canvas_list.bbox("all")))

        # Vincular el frame desplazable con el canvas
        self.canvas_list.create_window((0, 0), window=self.scrollable_list_frame, anchor="nw")

        # Menú principal
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="Cerrar App", command=self.exit_app)
        file_menu.add_command(label="Parar Procesos", command=self.stop_process)
        main_menu.add_cascade(label="Options", menu=file_menu)

        help_menu = Menu(main_menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        main_menu.add_cascade(label="Help", menu=help_menu)

        system_menu = Menu(main_menu, tearoff=0)
        system_menu.add_command(label="Actualizar", command=self.update_dependencies)
        main_menu.add_cascade(label='System', menu=system_menu)

        # Input para URL
        self.input_information = Label(self.input_frame, text='Agregar URL: ', bg='lightgray')
        self.input_information.grid(column=0, row=0, pady=10, padx=(10, 0))

        self.inputURL = Entry(self.input_frame, width=80)
        self.inputURL.grid(column=1, row=0, pady=10, padx=10, sticky="ew")

        add_button = Button(self.input_frame, text='Agregar', command=self.add_to_list)
        add_button.grid(column=2, row=0, pady=10, padx=10, sticky="nwe")

        self.update_status = Label(self.input_frame, text='', bg='lightgray')
        self.update_status.grid(column=1, row=1, columnspan=1, pady=(0, 10))

        download_button = Button(self.input_frame, text='Descargar', command=self.download)
        download_button.grid(column=0, row=1, pady=(0, 10), padx=(10, 0), sticky="nwe")

        clear_playlist = Button(self.input_frame, text='Eliminar', command=self.clear_playlist)
        clear_playlist.grid(column=2, row=1, pady=(10, 0), padx=(10, 0), sticky='nwe')

    def stop_process(self):
        self.downloader.detener_descarga()

    def clear_playlist(self):
        clear_data = messagebox.askokcancel("Alerta", "Se borraran todos los datos de la Playlist\n\n\t¿Desea Continuar?")
        if clear_data:
            self.downloader.clear_playlist()

    def update_dependencies(self):
        dependencies = ['tkinter', 'yt_dlp', 'pillow', 'shutil']
        self.update_status.config(text="Actualizando Librerias...", fg='black')
        self.root.update()  # Forzar la actualización de la interfaz gráfica
        dependency_checker.verificar_e_instalar_dependencias(dependencies)

    def download(self):
        self.update_status.config(text='Descargando...', fg='black')
        self.root.update()

        thread_download = threading.Thread(target=self.downloader.download_youtube_audio, )
        thread_download.start()
        #self.downloader.download_youtube_audio()

    def exit_app(self):
        self.root.quit()

    def show_about(self):
        messagebox.showinfo("Acerca de", "Aplicación para descargar MP3 de YouTube.")

if __name__ == '__main__':
    root = Tk()
    downloader = Downloader(root)
    root.mainloop()