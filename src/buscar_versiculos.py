import os
import re
from biblia_info import BibliaInfo

def buscar_versiculos(versiculo: str) -> str:
    """
    Busca versículos en los archivos AT.txt y NT.txt
    """
    biblia_info = BibliaInfo()
    match = re.match(r'(\d*)\s*(\w+)\s*(\d+)(?:,\s*(-?\d+)?(?:-(-?\d+)?)?)?', versiculo)
    if not match:
        return "Formato de referencia inválido"

    num, libro_ref, capitulo, versiculo_inicio, versiculo_fin = match.groups()
    libro_info = biblia_info.obtener_info_libro(libro_ref.strip())
    
    if not libro_info:
        return f"Libro no encontrado: {libro_ref}"
    
    abrev, nombre_completo, testamento = libro_info
    es_salmo = abrev == 'Sal'
    
    # Construir el nombre del archivo
    nombre_archivo = f"{num}_{abrev}_{capitulo}" if num else f"{abrev}_{capitulo}"
    
    try:
        with open(f"Biblia_crudo/{nombre_archivo}.txt", 'r', encoding='utf-8') as f:
            # Saltar las primeras líneas
            for _ in range(19):
                next(f)
            # Leer el resto del contenido
            lineas = f.readlines()
            # Excluir las últimas líneas
            lineas = lineas[:-6]
            contenido = ''.join(lineas)
            
        # Dividir en párrafos y filtrar por números
        parrafos = [p.strip() for p in contenido.split('\n\n') if p.strip()]
        
        # Si no hay versículo especificado, devolver todo el contenido
        if versiculo_inicio is None and versiculo_fin is None:
            if es_salmo:
                return '\n\n'.join(parrafos)
            # Para otros libros, limpiar cada párrafo individualmente
            parrafos_limpios = [' '.join(p.split()) for p in parrafos]
            return '\n\n'.join(parrafos_limpios)
        
        resultado = []
        versiculo_inicio = int(versiculo_inicio) if versiculo_inicio else 1
        versiculo_fin = int(versiculo_fin) if versiculo_fin else float('inf')
        
        for parrafo in parrafos:
            # Buscar número de versículo al inicio
            num_versiculo = re.match(r'^\s*(\d+)', parrafo)
            if num_versiculo:
                num = int(num_versiculo.group(1))
                if versiculo_inicio <= num <= versiculo_fin:
                    if es_salmo:
                        # Mantener el formato original para Salmos
                        resultado.append(parrafo.strip())
                    else:
                        # Limpiar el párrafo para otros libros
                        parrafo_limpio = ' '.join(parrafo.split())
                        resultado.append(parrafo_limpio)
        
        return '\n\n'.join(resultado) if resultado else "No se encontraron versículos"
        
    except FileNotFoundError:
        return f"No se encontró el archivo {nombre_archivo}.txt"


# Ejemplos de uso:
"""versiculo  = "1 Co 1, 3-6"  # Rango de versículos
resultado = buscar_versiculos(versiculo)
print(f"\nVersículo: {versiculo}")
print("Resultado:")
print(resultado)

versiculo = "Sal 120"  # Capítulo completo
resultado = buscar_versiculos(versiculo)
print(f"\nVersículo: {versiculo}")
print("Resultado:")
print(resultado)

versiculo = "Gn 7, 2"  # Versículo específico
resultado = buscar_versiculos(versiculo)
print(f"\nVersículo: {versiculo}")
print("Resultado:")
print(resultado)

versiculo = "Gál 6, 17-18"  # Rango de versículos
resultado = buscar_versiculos(versiculo)
print(f"\nVersículo: {versiculo}")
print("Resultado:")
print(resultado) """