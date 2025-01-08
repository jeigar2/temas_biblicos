import csv
import time

start_time = time.time()
print("Iniciando el proceso...")

# Definir las bibliotecas
biblioteca_AT = ['Gn', 'Éx', 'Lv', 'Nm', 'Dt', 'Jos', 'Jc', 'Rt', '1_Sm', '2_Sm', '1_Re', '2_Re', '1_Cr', '2_Cr', 'Es', 'Ne', 'Tob', 'Jdt', 'Est', '1_Mac', '2_Mac', 'Job', 'Sal', 'Pr', 'Ec', 'Cant', 'Sab', 'Si', 'Is', 'Jr', 'Lam', 'Ba', 'Ez', 'Dn', 'Os', 'Jl', 'Am', 'Abd', 'Jon', 'Mi', 'Na', 'Hab', 'So', 'Ag', 'Za', 'Mal', 'E-S-G', 'D-S-G', 'C-Jr']
biblioteca_NT = ['Mt', 'Mc', 'Lc', 'Jn', 'Hch', 'Rom', '1_Co', '2_Co', 'Gál', 'Ef', 'Flp', 'Col', '1_Tes', '2_Tes', '1_Tim', '2_Tim', 'Ti', 'Flm', 'Heb', 'St', '1_Pe', '2_Pe', '1_Jn', '2_Jn', '3_Jn', 'Jud', 'Ap']

# Leer la tabla resumen_biblia
with open('Biblia/resumen_biblia.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    resumen_biblia = [row for row in reader]

# Crear el listado
listado = "# Libros de la Biblia\n\n- Nube de mapas\n\n"

# Agregar la sección Antiguo Testamento
listado += "## Antiguo Testamento\n\n"
for abrev in biblioteca_AT:
    for row in resumen_biblia:
        if row['Abrev'] == abrev:
            libro = row['Libro']
            total = row['Total']
            break
    listado += f"- [{libro} ({abrev} - {total})](../Biblia/{libro}.md)\n"

# Agregar la sección Nuevo Testamento
listado += "\n## Nuevo Testamento\n\n"
for abrev in biblioteca_NT:
    print(f"Escribiendo el libro {libro}...")
    for row in resumen_biblia:
        if row['Abrev'] == abrev:
            libro = row['Libro']
            total = row['Total']
            break
    listado += f"- [{libro} ({abrev} - {total})](../Biblia/{abrev}.md)\n"
    print(f"Terminando el libro {libro}...")

# Escribir el listado en un archivo
with open("markdown/Nube_palabras_Biblia.md", "w") as f:
    for line in listado.split('\n'):
        f.write(line + '\n')

end_time = time.time()
print(f"Terminando el proceso... (tomó {end_time - start_time} segundos)")