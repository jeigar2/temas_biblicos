import os
import sys

ruta = 'Biblia_crudo/'
argumento = sys.argv[1]

for fichero in os.listdir(ruta):
    if fichero.startswith(argumento) and fichero.endswith('.txt'):
        with open(os.path.join(ruta, fichero), 'r') as f:
            contenido = f.readlines()
        print(f"Archivo: {fichero}")
        print(f"Primera línea: {contenido[0].strip()}")
        if contenido[0].strip() == "La Santa Sede":
            print("Encontré el texto buscado!")
            contenido = contenido[18:-7]
        else:
            print("No encontré el texto buscado")
        with open(os.path.join(ruta, 'limpio_' + fichero), 'w') as f:
            f.writelines(contenido)