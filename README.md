# temas_biblicos

Repositorio para hacer diagramas de markdown y plantuml de temas bíblicos

## Temas tratados

[libros de la Biblia](markdown/Libros_de_la_Biblia.md)

[Genealogía de Noé](markdown/Genealogia_de_Noe.md)

[Nube de palabras de cada capítulo de la Biblia](markdown/Nube_palabras_Biblia.md) (en construccción)

## Nuevos pasos a dar

- Crear una nube de palabras con cada capítulo de cada libro de la Biblia,

- Se ha subido varios textos a los que se les ha filtrados unas palabras con los [patrones](Biblia/texto_filtrado/patron-filtro.txt)
- Para extraer los textos utilizamos el navegador de consola **lynx** al que pasamos una URL y luego imprimimos el resultado de la pagina
  - `lynx https://www.vatican.va/archive/ESL0506/__P3.HTM`
    - para imprimir se pulsa `[p]` y luego se selecciona guardar, y se le pone nombre `Gn_1.txt`
  - ~~Para esto se puede usar las macros~~
    - ~~`macro1.mac` pensado en pasar un argumento para poder poner el nombre del fichero... sin probar, se trata de avanzar a la siguiente página con el enlace `6`~~
    - ~~`macro2.mac`, alguien desde fuera te llama y te pasa la `url` y el `nombre del fichero`~~
  - Esto quedó mas sencillo llamando a `lynx -dump -width=80 -nolist url > pagina.txt`
  - Jugando con estos comandos se ha dejado algo en las `notas.sh` y especialmente desde la carpeta `temas_biblicos/src` ejecutar `./lector-url.sh https://www.vatican.va/archive/ESL0506/__PH.HTM` entre todas las salidas se ha encontrado la página que tiene todos los url de los capítulos
  - Con esta información se ha creado un fichero `csv` con todos los capítulos y se ha definido los campos:
    - `URL`: url del capítulo
    - `cap`: número del capítulo
    - `Libro`: libro al que  pertenece la url del capítulo
    - `Abrev`: abreviatura del libro
    - `total`: de capítulos del libro
  - Este csv al tramitarlo extrae todos los capítulos y los vuelca en la carpeta `Biblia_crudo`
    - automatizado aquí para obtener la información, ejecutando:
      - `src/extrae_capitulos_url_desde_csv.py`

    - ~~Se ha creado tres fases para limpiar los ficheros con lenguaje python, el fichero final, queda en mayúsculas y se eliminan las palabras como articulos, pronombres, preprosiciones, números, signos de puntuación...~~
    - ~~para ejecutar los programas~~
      - ~~/bin/python src/limpiar_fichero_1.py~~
      - ~~/bin/python src/limpiar_fichero_2.py~~
      - ~~/bin/python src/limpiar_fichero_3.py~~

    - Simplificado en el fichero, que procesa los ficheros de un origen, y guarda una copia filtrada de las palabras importantes para generar la nube de palabras.
      - `src/ordenar_ficheros_Biblia.py`
      - se ejecuta con este comando `python3 src/ordenar_ficheros_Biblia.py` estando en la carpeta `temas_biblicos/`

- ~~Para generar la nube de palabras nos hemos ayudado de esta herramiente [wordcloud](https://awario.com/es/wordcloud/) al que se le pasa el resultado del fichero fase3_gen1.txt y al generar la nubes de palabras se descarga el fichero en color negro y azul, el nombre Gn_1.png es negro y Gn_1_azul.png es azul~~

- Se ha utilizado python para generar la nube de palabras en vista de que se puede automatizar y el paso anterior era artesanal.
  - Tutorial de la libreria [wordcloud](https://www.datacamp.com/es/tutorial/wordcloud-python)

  - Gen [1](Biblia/texto_filtrado/AT/Gn/Gn_1.txt), [2](Biblia/texto_filtrado/AT/Gn/Gn_2.txt)
  - Imagenes

  - Gen 1

  ![Gen1](Biblia/nube_de_palabras/AT/Gn/Gn_1.png)

  - Gen 2

  ![Gen2](Biblia/nube_de_palabras/AT/Gn/Gn_2.png)

  - **TODO**: ~~Si ves el codigo fuente puedes guardar el SVG donde generar el mapa de palabras y se puede guardar en un fichero con extensión SVG~~
  - **TODO**: El SVG está comentado porque al generar el fichero no vuelca contenido se queda el fichero con 0 kb ya se revisará
  - **TODO**: Crear al igual que [Genesis](/Biblia/Genesis.md) una hoja con acceso a todos los nubes de palabras de cada capítulo de dicho libro, crear una hoja por libro.
  
  ~~![Gen8](Biblia/nube_de_palabras/AT/Gn/Gn_8.svg)~~
