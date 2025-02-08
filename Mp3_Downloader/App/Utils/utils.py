from PIL import Image, ImageTk

def cargar_imagen_tkinter(ruta_imagen, tamaño=(16, 16)):
    
    # Cargar la imagen usando Pillow
    imagen = Image.open(ruta_imagen)
    
    # Redimensionar la imagen al tamaño especificado
    imagen_redimensionada = imagen.resize(tamaño)
    
    # Convertir la imagen redimensionada a un formato que Tkinter pueda usar
    imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
    
    return imagen_tk