import os
import re

def buscar_versiculos(versiculo):
    # Formato: "1 Co 1, 3-6" o "Gn 7, 2" o "Sal 120"
    match = re.match(r'(\d*)\s*(\w+)\s*(\d+)(?:,\s*(\d+)(?:-(\d+))?)?', versiculo)
    if not match:
        return "Formato de referencia inválido"
    
    num, libro, capitulo, versiculo_inicio, versiculo_fin = match.groups()
    nombre_archivo = f"{num}_{libro}_{capitulo}" if num else f"{libro}_{capitulo}"
    
    # Buscar el archivo
    try:
        with open(f"Biblia_crudo/{nombre_archivo}.txt", 'r', encoding='utf-8') as f:
            # Saltar las primeras 16 líneas
            for _ in range(19):
                next(f)
            # Leer el resto del contenido
            lineas = f.readlines()
            # Excluir las últimas 5 líneas
            lineas = lineas[:-6]
            contenido = ''.join(lineas)
            
        # Dividir en párrafos y filtrar por números
        parrafos = contenido.split('\n\n')  # Asume párrafos separados por línea en blanco
        resultado = []
        
        # Si no hay versículo especificado, devolver todo el contenido
        if versiculo_inicio is None:
            return contenido
            
        # Convertir a enteros para comparación
        inicio = int(versiculo_inicio)
        fin = int(versiculo_fin) if versiculo_fin else inicio
            
        for parrafo in parrafos:
            # Buscar número de versículo al inicio
            num_versiculo = re.match(r'^\s*(\d+)', parrafo)
            if num_versiculo:
                num = int(num_versiculo.group(1))
                if inicio <= num <= fin:
                    resultado.append(parrafo.strip())
                    
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