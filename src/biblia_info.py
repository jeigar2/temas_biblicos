import pandas as pd
from typing import Optional, Dict, Tuple

class BibliaInfo:
    def __init__(self):
        self.df = pd.read_csv('Biblia/resumen_biblia.csv')
        self._determinar_testamentos()
        self._crear_mapeos()

    def _determinar_testamentos(self):
        """Determina si cada libro pertenece al AT o NT basado en los archivos"""
        # Leer archivos AT.txt y NT.txt
        with open('Biblia/AT.txt', 'r', encoding='utf-8') as f:
            contenido_at = f.read()
        with open('Biblia/NT.txt', 'r', encoding='utf-8') as f:
            contenido_nt = f.read()

        # Crear columna de testamento
        def determinar_testamento(abrev):
            if abrev in contenido_at:
                return 'AT'
            elif abrev in contenido_nt:
                return 'NT'
            return 'Desconocido'

        self.df['Testamento'] = self.df['Abrev'].apply(determinar_testamento)

    def _crear_mapeos(self):
        # Crear diccionarios para búsqueda rápida
        self.libro_a_abrev = dict(zip(self.df['Libro'].apply(lambda x: x.replace('_', ' ')), self.df['Abrev']))
        self.abrev_a_libro = dict(zip(self.df['Abrev'], self.df['Libro'].apply(lambda x: x.replace('_', ' '))))
        self.total_capitulos = dict(zip(self.df['Abrev'], self.df['Total']))
        self.testamentos = dict(zip(self.df['Abrev'], self.df['Testamento']))
        
        # Agregar entradas adicionales para búsqueda por nombre completo
        self.abrev_a_libro.update(dict(zip(self.df['Libro'].apply(lambda x: x.replace('_', ' ')), 
                                          self.df['Libro'].apply(lambda x: x.replace('_', ' ')))))

    def obtener_info_libro(self, referencia: str) -> Optional[Tuple[str, str, str]]:
        """Retorna (abreviatura, nombre_completo, testamento) si existe el libro"""
        if referencia in self.abrev_a_libro:
            nombre = self.abrev_a_libro[referencia]
            abrev = self.libro_a_abrev.get(nombre, referencia)
            testamento = self.testamentos.get(abrev, 'Desconocido')
            return abrev, nombre, testamento
        return None

    def validar_capitulo(self, abrev: str, capitulo: int) -> bool:
        """Valida si el capítulo existe en el libro"""
        return 1 <= capitulo <= self.total_capitulos.get(abrev, 0)

    def obtener_todos_libros(self):
        """Retorna la lista completa de libros con su información"""
        return self.df.to_dict('records') 

#ejemplo = BibliaInfo()
#print(ejemplo.obtener_todos_libros())