import subprocess
import sys

def verificar_e_instalar_paquetes(paquetes):
    """
    Verifica si los paquetes en la lista están instalados y, si no lo están, los instala.
    
    Parámetros:
        paquetes (list): Lista de nombres de paquetes a verificar e instalar.
    """
    for paquete in paquetes:
        try:
            # Intentar importar el paquete para verificar si está instalado
            __import__(paquete)
            print(f"{paquete} ya está instalado.")
        except ImportError:
            print(f"{paquete} no está instalado. Procediendo a instalar...")
            try:
                # Ejecutar el comando para instalar el paquete
                comando = f"{sys.executable} -m pip install {paquete}"
                resultado = subprocess.run(comando, shell=True, text=True, capture_output=True)

                if resultado.returncode == 0:
                    print(f"Instalación exitosa de {paquete}.")
                    print(resultado.stdout)
                else:
                    print(f"Error durante la instalación de {paquete}.")
                    print(resultado.stderr)
            except Exception as e:
                print(f"Error al intentar instalar {paquete}:", str(e))

def actualizar_paquetes(paquetes):
    """
    Verifica si los paquetes en la lista están instalados y, si no lo están, los instala.
    
    Parámetros:
        paquetes (list): Lista de nombres de paquetes a verificar e instalar.
    """
    for paquete in paquetes:
        print(f"{paquete} Actualiando...")
        try:
            # Ejecutar el comando para instalar el paquete
            comando = f"{sys.executable} -m pip install --upgrade {paquete}"
            resultado = subprocess.run(comando, shell=True, text=True, capture_output=True)

            if resultado.returncode == 0:
                print(f"Actualización exitosa de {paquete}.")
                print(resultado.stdout)
            else:
                print(f"Error durante la Actualización de {paquete}.")
                print(resultado.stderr)
        except Exception as e:
            print(f"Error al intentar Actualizar {paquete}:", str(e))

if __name__ == '__main__':
    # Lista de paquetes a verificar e instalar
    paquetes_a_instalar = ["yt_dlp"]

    # Ejecutar la función
    actualizar_paquetes(paquetes_a_instalar)