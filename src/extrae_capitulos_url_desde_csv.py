import csv
import os
import subprocess
import time
import shutil

# Inicio del proceso
start_time = time.time()
print("Inicio del proceso")

# Abrimos el archivo CSV
with open('Biblia/listado_url_biblia.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Traza de inicio de lectura de fila
        print(f"Procesando fila {reader.line_num} - {row['Abrev']}")

        # Recuperamos los campos URL y Abrev
        url = row['URL']
        abrev = row['Abrev']

        # Traza de cap
        print(f"Cap: {row['cap']}")

        # Si el campo cap es diferente de 0, ejecutamos lynx y guardamos el resultado en un fichero
        if int(row['cap']) != 0:
            filename = f"{abrev}_{row['cap']}.txt"
            print(f"Procesando URL {url} y guardando en {filename}")
            if os.path.exists('/usr/bin/lynx'):
                subprocess.run(['/usr/bin/lynx', '-dump', '-width=80', '-nolist', url], stdout=open(filename, 'w'))
                shutil.move(filename, 'Biblia_crudo')
            else:
                print("El ejecutable lynx no existe")
            #subprocess.run(['lynx', '-dump', '-width=80', '-nolist', url], stdout=open(filename, 'w'))
        else:
            print("Cap igual a 0, se descarta")

        # Traza de fin de lectura de fila
        print(f"Fin de procesamiento de fila {reader.line_num} - {row['Abrev']} - Cap: {row['cap']} de {row['total']}")

# Fin del proceso
end_time = time.time()
print(f"Tiempo de ejecución: {end_time - start_time} segundos")