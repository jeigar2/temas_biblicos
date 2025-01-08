import pandas as pd
import time

print("Iniciando el proceso...")
start_time = time.time()

# Definir las bibliotecas
biblioteca_AT = ['Gn', 'Éx', 'Lv', 'Nm', 'Dt', 'Jos', 'Jc', 'Rt', '1_Sm', '2_Sm', '1_Re', '2_Re', '1_Cr', '2_Cr', 'Es', 'Ne', 'Tob', 'Jdt', 'Est', '1_Mac', '2_Mac', 'Job', 'Sal', 'Pr', 'Ec', 'Cant', 'Sab', 'Si', 'Is', 'Jr', 'Lam', 'Ba', 'Ez', 'Dn', 'Os', 'Jl', 'Am', 'Abd', 'Jon', 'Mi', 'Na', 'Hab', 'So', 'Ag', 'Za', 'Mal', 'E-S-G', 'D-S-G', 'C-Jr']
biblioteca_NT = ['Mt', 'Mc', 'Lc', 'Jn', 'Hch', 'Rom', '1_Co', '2_Co', 'Gál', 'Ef', 'Flp', 'Col', '1_Tes', '2_Tes', '1_Tim', '2_Tim', 'Ti', 'Flm', 'Heb', 'St', '1_Pe', '2_Pe', '1_Jn', '2_Jn', '3_Jn', 'Jud', 'Ap']

# Leer la tabla resumen_biblia
resumen_biblia = pd.read_csv('Biblia/resumen_biblia.csv')

# Iterar sobre la tabla y generar el archivo Markdown
for index, row in resumen_biblia.iterrows():

    print(resumen_biblia.columns)
    
    libro = row['Libro']
    abrev = row['Abrev']
    total = row['Total']

    print(f"Iniciando el libro {libro}...")

    # Determinar la biblioteca
    if abrev in biblioteca_AT:
        biblioteca = 'AT'
    elif abrev in biblioteca_NT:
        biblioteca = 'NT'
    else:
        raise ValueError(f"Abreviatura '{abrev}' no encontrada en ninguna biblioteca")

    # Generar el archivo Markdown
    with open(f'Biblia/{libro}.md', 'w') as f:
        f.write(f'# {libro}\n\n')
        for i in range(1, total + 1):
            f.write(f'{i}. Capítulo {i} [texto](texto_filtrado/{biblioteca}/{abrev}/{abrev}_{i}.txt), ![imagen](nube_de_palabras/{biblioteca}/{abrev}/{abrev}_{i}.png)\n')
        
    print(f"Terminando el libro {libro}...")

print(f"Terminando el proceso... (tomó {time.time() - start_time} segundos)")
