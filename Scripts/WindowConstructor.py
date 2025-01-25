from tkinter import Tk, Frame, Menu, messagebox, Entry, Button, Label, ttk
from Utils import dependency_checker
from Download import Youtube_Downloader

class Downloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Mp3 Downloader")
        self.root.geometry("700x500")  # Tamaño inicial de la ventana
        self.root.configure(bg="gray")  # Fondo gris de la ventana principal
        root.resizable(False, False)  # Evita que la ventana cambie de tamaño

        self.create_layout()

        self.downloader = Youtube_Downloader(self.showList_frame, self.showInfo_frame)

    def add_to_list(self):
        videoURL = self.inputURL.get()
        self.downloader.agregar_a_playlist(videoURL, self.show_information)

    def create_layout(self):
        # Marco principal
        self.main_frame = Frame(self.root, bg='lightgray', width=700, height=500)
        self.main_frame.pack_propagate(False)  # Tamaño fijo para el marco principal
        self.main_frame.pack(fill='both', expand=False, padx=10, pady=10)

        # Marco de input
        self.input_frame = Frame(self.main_frame, bg='lightgray', height=50)
        self.input_frame.pack(side='top', fill='x', expand=False)

        # Marco de muestra de informacion
        self.showInfo_frame = Frame(self.main_frame, bg='white', width=320, height=450)
        self.showInfo_frame.pack_propagate(False)  # Tamaño fijo para el marco de información
        self.showInfo_frame.pack(side='right', padx=(5, 10), pady=10)

        # Marco para mostrar los videos añadidos
        self.showList_frame = Frame(self.main_frame, bg='white', width=340, height=450)
        self.showList_frame.pack_propagate(False)  # Tamaño fijo para el marco de la lista
        self.showList_frame.pack(side='left', anchor='n', padx=(10, 5), pady=10)

        # Crear el menú principal
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)  # Asignar el menú a la ventana principal

        # Submenú "Archivo"
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label="Download", command=self.download)
        file_menu.add_command(label="Close App", command=self.exit_app)
        main_menu.add_cascade(label="Options", menu=file_menu)

        # Submenú "Ayuda"
        help_menu = Menu(main_menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        main_menu.add_cascade(label="Help", menu=help_menu)

        # Submenú "System"
        system_menu = Menu(main_menu, tearoff=0)
        system_menu.add_command(label="Update Libraries", command=self.update_dependencies)
        main_menu.add_cascade(label='System', menu=system_menu)

        # Input information
        self.input_information = Label(self.input_frame, text='Insert URL: ', bg='lightgray')
        self.input_information.grid(column=0, row=0, pady=10, padx=(10, 0))

        # Input para URL
        self.inputURL = Entry(self.input_frame, width=80)
        self.inputURL.grid(column=1, row=0, pady=10, padx=10, sticky="ew")

        # Boton de descarga
        add_button = Button(self.input_frame, text='Agregar', command=self.add_to_list)
        add_button.grid(column=2, row=0, pady=10, padx=10, sticky="ew")

        self.show_information = Label(self.showInfo_frame, text='No data loaded', anchor='nw', bg='white', justify="left", wraplength=280)
        self.show_information.pack(side='top', anchor='n', fill='both', expand=True, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(self.input_frame, orient='horizontal', mode='determinate', length=400)
        self.progress_bar.grid(column=1, row=1, columnspan=1, pady=(0,10))

    def update_progress_bar(self, progress):
        self.progress_bar['value'] = progress
        self.root.update_idletask()

    def update_dependencies(self):
        dependencies = ['yt_dlp']
        dependency_checker.actualizar_paquetes(dependencies)

    def download(self):
        self.progress_bar['value'] = 0
        self.downloader.download_youtube_audio(progress_callback=self.update_progress_bar)

    def exit_app(self):
        self.root.quit()  # Cierra la aplicación

    def show_about(self):
        messagebox.showinfo("Acerca de", "Aplicación para descargar MP3 de YouTube.")

if __name__ == '__main__':
    root = Tk()
    downloader = Downloader(root)
    root.mainloop()
