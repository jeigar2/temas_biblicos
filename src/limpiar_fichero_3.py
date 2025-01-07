import os
import re

ruta_archivos = 'Biblia_crudo/'
ruta_patron_filtro = 'Biblia/texto_filtrado/patron-filtro.txt'

print("Iniciando proceso de filtrado de archivos...")

# Leer el archivo de expresiones regulares
with open(ruta_patron_filtro, 'r') as f:
    patron_filtro = [line.strip() for line in f.readlines()]

print(f"Archivo de patron-filtro: {ruta_patron_filtro} con {len(patron_filtro)} expresiones regulares")

# Iterar sobre los archivos fase2_*.txt
for fichero in os.listdir(ruta_archivos):
    if fichero.startswith('fase2_') and fichero.endswith('.txt'):
        print(f"Tratando archivo: {fichero}")
        with open(os.path.join(ruta_archivos, fichero), 'r') as f:
            contenido = f.readlines()
        print(f"Archivo {fichero} tiene {len(contenido)} líneas")

        with open(os.path.join(ruta_archivos, fichero), 'w') as f:
            for line in contenido:
                line = line.upper()
                for patron in patron_filtro:
                    if re.search(patron, line, re.IGNORECASE):
                        print(f"Encontrado patron {patron} en línea: {line}")
                        line = re.sub(patron, ' ', line, re.IGNORECASE)
                        print(f"Reemplazado patron {patron} en línea: {line}")
                # Eliminar varios espacios
                line = ' '.join(line.split())  # Reemplazar varios espacios en blanco por uno
                f.write(line)

        print(f"Archivo tratado: {fichero}")
        nuevo_nombre = fichero.replace('fase2_', 'fase3_')
        os.rename(os.path.join(ruta_archivos, fichero), os.path.join(ruta_archivos, nuevo_nombre))
        print(f"Archivo guardado como: {nuevo_nombre}")

print("Proceso de filtrado de archivos finalizado.")