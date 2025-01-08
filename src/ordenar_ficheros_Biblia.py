import os
import re
import logging
import time

import wordcloud
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import svglib.svglib as svglib

# Funcion que trunca el contenido del fichero 
# siempre que tenga en la primera línea
# el patrón "La Santa Sede"
# elimina las líneas iniciales y finales
def truncar_contenido_fichero(ruta, fichero):
    #ruta, fichero = os.path.split(nombre_fichero)
    with open(os.path.join(ruta, fichero), 'r') as f:
        contenido = f.readlines()
    print(f"Archivo: {fichero}")
    print(f"Primera línea: {contenido[0].strip()}")
    if contenido[0].strip() == "La Santa Sede":
        print("Encontré el texto buscado!")
        contenido = contenido[18:-7]
    else:
        print("No encontré el texto buscado")
    return contenido

def obtener_listado_palabras(contenido):
    ruta_patron_filtro = 'Biblia/texto_filtrado/patron-filtro.txt'
    print("Iniciando proceso de filtrado de archivos...")

    # Leer el archivo de expresiones regulares
    with open(ruta_patron_filtro, 'r') as f:
        patron_filtro = [line.strip() for line in f.readlines()]

    print(f"Archivo de patron-filtro: {ruta_patron_filtro} con {len(patron_filtro)} expresiones regulares")

    resultado = ''
    for line in contenido:
        line = line.upper()
        for patron in patron_filtro:
            if re.search(patron, line, re.IGNORECASE):
                print(f"Encontrado patron {patron} en línea: {line}")
                line = re.sub(patron, ' ', line, re.IGNORECASE)
                print(f"Reemplazado patron {patron} en línea: {line}")
        # Eliminar saltos de línea y espacios
        line = line.replace('\n', ' ')
        resultado += line

    return resultado.strip()

def escribir_fichero(contenido, ruta_destino, nombre_fichero):
    with open(os.path.join(ruta_destino, nombre_fichero), 'w') as f:
        f.write(contenido)
    print(f"Archivo creado en {ruta_destino} con éxito")

def generar_nube_palabras(texto, directorio, nombre_sin_extension, color=None):
    # Crea la nube de palabras
    wc = wordcloud.WordCloud(width=800, height=600, background_color='white', max_words=25, max_font_size=100)
    #wc = wordcloud.WordCloud(width=800, height=600, mode='RGBA', background_color='None', max_words=50, max_font_size=100)
    print("Generando nube de palabras...")

    wc.generate(texto)

    # Convierte el resultado en un archivo PNG
    png_bytes = BytesIO()
    img = wc.to_image()
    if color:
        img.putalpha(128)  # Aplica un alpha de 50% para hacer el texto azul
        nombre_fichero = nombre_sin_extension + '_azul.png'
    else:
        nombre_fichero = nombre_sin_extension + '.png'
    img.save(png_bytes, format='PNG')
    png_bytes.seek(0)
    
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    ruta_completa = os.path.join(directorio, nombre_fichero)

    # Escribir el resultado en un archivo PNG
    with open(ruta_completa, 'wb') as f:
        f.write(png_bytes.getvalue())

def generar_nube_palabras_azul(texto, directorio, nombre_sin_extension):
    generar_nube_palabras(texto, directorio, nombre_sin_extension, color='azul')

def generar_nube_palabras_svg(texto, directorio, nombre_sin_extension):
    # Crea la nube de palabras
    wc = wordcloud.WordCloud(width=800, height=600, background_color='white', max_words=25, max_font_size=100)
    #wc = wordcloud.WordCloud(width=800, height=600, mode='RGBA', background_color='None', max_words=50, max_font_size=100)

    wc.generate(texto)

    # Convierte el resultado en un archivo SVG
    svg_bytes = BytesIO()
    wc.to_svg(svg_bytes)
    svg_bytes.seek(0)

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    ruta_completa = os.path.join(directorio, nombre_fichero.replace('.txt',''))

    # Escribir el resultado en un archivo SVG
    with open(ruta_completa + '.svg', 'wb') as f:
        f.write(svg_bytes.getvalue())


# Configuración del logging
logging.basicConfig(filename='log/proceso_mover_fichero.log', level=logging.INFO)

# Traza inicial
logging.info("Inicio del proceso")

# Tiempo inicial
start_time = time.time()
print(f"Inicio del proceso: {time.ctime(start_time)}")

# Bibliotecas
at_biblioteca = set(open('Biblia/AT.txt', 'r').read().splitlines())
nt_biblioteca = set(open('Biblia/NT.txt', 'r').read().splitlines())

# Directorio de entrada
#directorio_entrada = sys.argv[1] # 'Biblia_crudo/'
#directorio_entrada = 'tmp/'
directorio_entrada = 'Biblia_crudo/'


# Expresión regular para filtrar archivos
patron = re.compile(r'^\w{2,8}_\d{1,3}\.txt$')

# Directorio de destino
directorio_salida = 'Biblia/texto_filtrado/'
directorio_salida_imagenes = 'Biblia/nube_de_palabras/'


# Crear directorios de bibliotecas si no existen
if not os.path.exists(os.path.join(directorio_salida, 'AT')):
    os.makedirs(os.path.join(directorio_salida, 'AT'))
if not os.path.exists(os.path.join(directorio_salida, 'NT')):
    os.makedirs(os.path.join(directorio_salida, 'NT'))

# Recorrer directorio de entrada
for nombre_fichero in os.listdir(directorio_entrada):
    if patron.match(nombre_fichero):

        contenido_truncado = truncar_contenido_fichero(directorio_entrada, nombre_fichero)
        listado_palabras = obtener_listado_palabras(contenido_truncado)
        # Itero por segunda vez para dejarlo limpio
        listado_palabras_final = obtener_listado_palabras(listado_palabras)

        # Descomponer nombre del archivo
        nombre, extension = os.path.splitext(nombre_fichero)
        libro, capitulo = nombre.rsplit('_', 1)
        libro = libro.strip('_')

        # Comprobar libro en bibliotecas
        if libro in at_biblioteca:
            biblioteca = 'AT'
        elif libro in nt_biblioteca:
            biblioteca = 'NT'
        else:
            print(f"Error: libro '{libro}' no encontrado en bibliotecas")
            continue

        # Crear directorio del libro si no existe
        directorio_libro = os.path.join(directorio_salida, biblioteca, libro)
        if not os.path.exists(directorio_libro):
            os.makedirs(directorio_libro)

        # escribir el archivo en el directorio del libro
        escribir_fichero(listado_palabras_final, directorio_libro, nombre_fichero)
        print(f"Archivo '{nombre_fichero}' generado en '{directorio_libro}'")

        nombre_sin_extension = os.path.splitext(nombre_fichero)[0]
        directorio_libro_imagen = directorio_libro.replace(directorio_salida,directorio_salida_imagenes)

        generar_nube_palabras(listado_palabras_final, directorio_libro_imagen, nombre_sin_extension)
        generar_nube_palabras_azul(listado_palabras_final, directorio_libro_imagen, nombre_sin_extension)
        #generar_nube_palabras_svg(listado_palabras_final, directorio_libro_imagen, nombre_sin_extension)

# Traza final
logging.info(f"Fin del proceso. Tiempo total: {time.time() - start_time:.2f} segundos")

# Imprimir traza en la salida estandar
print(f"Fin del proceso: {time.ctime(time.time())}")
print(f"Tiempo total: {time.time() - start_time:.2f} segundos")