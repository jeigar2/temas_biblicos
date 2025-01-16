import pandas as pd
from typing import Optional, Dict, Tuple

class BibliaInfo:
    def __init__(self):
        self.df = pd.read_csv('Biblia/resumen_biblia.csv')
        self._crear_mapeos()

    def _crear_mapeos(self):
        # Crear diccionarios para búsqueda rápida
        self.libro_a_abrev = dict(zip(self.df['Libro'], self.df['Abrev']))
        self.abrev_a_libro = dict(zip(self.df['Abrev'], self.df['Libro']))
        self.total_capitulos = dict(zip(self.df['Abrev'], self.df['Total']))
        
        # Agregar entradas adicionales para búsqueda por nombre completo
        self.abrev_a_libro.update(dict(zip(self.df['Libro'], self.df['Libro'])))

    def obtener_info_libro(self, referencia: str) -> Optional[Tuple[str, str]]:
        """Retorna (abreviatura, nombre_completo) si existe el libro"""
        if referencia in self.abrev_a_libro:
            nombre = self.abrev_a_libro[referencia]
            abrev = self.libro_a_abrev.get(nombre, referencia)
            return abrev, nombre
        return None

    def validar_capitulo(self, abrev: str, capitulo: int) -> bool:
        """Valida si el capítulo existe en el libro"""
        return 1 <= capitulo <= self.total_capitulos.get(abrev, 0)

    def obtener_todos_libros(self):
        """Retorna la lista completa de libros con su información"""
        return self.df.to_dict('records') 

#ejemplo = BibliaInfo()
#print(ejemplo.obtener_todos_libros())