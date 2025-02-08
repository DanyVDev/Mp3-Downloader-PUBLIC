import subprocess
import sys
from shutil import which
import os

def verificar_e_instalar_dependencias(paquetes):
    
    verificar_e_instalar_paquetes(paquetes)
    verificar_e_instalar_ffmpeg()

def verificar_e_instalar_paquetes(paquetes):
    
    for paquete in paquetes:
        try:
            __import__(paquete)
            print(f"{paquete} ya está instalado.")
        except ImportError:
            print(f"{paquete} no está instalado. Instalando...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", paquete], check=True)
                print(f"Instalación exitosa de {paquete}.")
            except subprocess.CalledProcessError as e:
                print(f"Error durante la instalación de {paquete}: {e}")

def verificar_e_instalar_ffmpeg():
    
    if which("ffmpeg"):
        print("ffmpeg ya está instalado y disponible en el PATH.")
        return

    print("ffmpeg no está instalado. Intentando configurarlo automáticamente...")
    try:
        # Descarga y configuración para Windows
        if os.name == "nt":
            url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            ffmpeg_zip = "ffmpeg.zip"
            ffmpeg_dir = "ffmpeg_temp"

            # Descargar el archivo ZIP de ffmpeg
            subprocess.run(["curl", "-L", "-o", ffmpeg_zip, url], check=True)
            print("Descarga de ffmpeg completada.")

            # Descomprimir el ZIP
            import zipfile
            with zipfile.ZipFile(ffmpeg_zip, "r") as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
            
            # Mover ffmpeg.exe al PATH
            bin_path = os.path.join(ffmpeg_dir, os.listdir(ffmpeg_dir)[0], "bin")
            os.environ["PATH"] += os.pathsep + bin_path
            print(f"ffmpeg configurado correctamente en el PATH desde {bin_path}.")

        else:
            print("Por favor instala ffmpeg manualmente en tu sistema operativo.")
    except Exception as e:
        print(f"Error al configurar ffmpeg: {e}")


