import subprocess
import os
import shutil
import logging
import time

# Configuración del logging
logging.basicConfig(filename='log/proceso_mover_fichero.log', level=logging.INFO)

# Traza inicial
logging.info("Inicio del proceso")

# Define la lista de comandos a ejecutar
comandos = [
    "python3 src/limpiar_fichero.py Gn",
    "python3 src/limpiar_fichero_2.py",
    "python3 src/limpiar_fichero_3.py"
]

# Tiempo inicial
start_time = time.time()
print(f"Inicio del proceso: {time.ctime(start_time)}")

# Ejecutar los comandos de manera secuencial
for i, comando in enumerate(comandos):
    logging.info(f"Ejecutando comando {i+1}: {comando}")
    subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.info(f"Comando {i+1} terminado con código {subprocess.CalledProcessError}")
    if subprocess.CalledProcessError:
        logging.error(f"Error al ejecutar comando {i+1}: {subprocess.CalledProcessError}")

# Mover los archivos y renombrarlos
ruta_inicial = "Biblia_crudo/"
ruta_final = "Biblia/texto_filtrado/AT/Gn"
for archivo in os.listdir(ruta_inicial):
    if archivo.startswith("fase3_"):
        archivo_min = archivo.replace("fase3_", "")
        shutil.move(os.path.join(ruta_inicial, archivo), os.path.join(ruta_final, archivo_min))
        logging.info(f"Renombrado archivo {archivo} a {archivo_min}")

# Traza final
logging.info(f"Fin del proceso. Tiempo total: {time.time() - start_time:.2f} segundos")

# Imprimir traza en la salida estandar
print(f"Fin del proceso: {time.ctime(time.time())}")
print(f"Tiempo total: {time.time() - start_time:.2f} segundos")