from flask import Flask, request, jsonify
import re
from buscar_versiculos import buscar_versiculos
from biblia_info import BibliaInfo

app = Flask(__name__)
biblia_info = BibliaInfo()

@app.route('/api/versiculos', methods=['GET'])
def obtener_versiculos():
    referencia = request.args.get('referencia')
    
    if not referencia:
        return jsonify({
            'error': 'Se requiere el parámetro "referencia"'
        }), 400
        
    try:
        # Extraer los componentes de la referencia
        match = re.match(r'(\d*)\s*([^0-9]+?)\s*(\d+)(?:,\s*(-?\d+)?(?:-(-?\d+)?)?)?', referencia)
        if not match:
            return jsonify({
                'error': 'Formato de referencia inválido'
            }), 400
            
        num, libro_ref, capitulo, versiculo_inicio, versiculo_fin = match.groups()
        libro_ref = libro_ref.strip()
        
        # Validar y obtener información del libro
        libro_info = biblia_info.obtener_info_libro(libro_ref)
        if not libro_info:
            return jsonify({
                'error': f'Libro no encontrado: {libro_ref}'
            }), 400
        
        abrev, nombre_completo = libro_info
        
        # Validar capítulo
        capitulo = int(capitulo)
        if not biblia_info.validar_capitulo(abrev, capitulo):
            return jsonify({
                'error': f'Capítulo {capitulo} no existe en {nombre_completo}'
            }), 400

        # Construir el rango de versículos para la respuesta
        if versiculo_inicio is None and versiculo_fin is None:
            versiculos_rango = "completo"
        else:
            inicio = versiculo_inicio if versiculo_inicio else ""
            fin = versiculo_fin if versiculo_fin else ""
            versiculos_rango = f"{inicio}-{fin}".strip("-")
        
        # Obtener el texto de los versículos
        resultado = buscar_versiculos(f"{abrev} {capitulo}, {versiculos_rango}")
        versiculos_array = [v.strip() for v in resultado.split('\n\n') if v.strip()]
        
        return jsonify({
            'referencia': {
                'libro': {
                    'abreviatura': abrev,
                    'nombre': nombre_completo
                },
                'capitulo': capitulo,
                'versiculos': versiculos_rango
            },
            'versiculos': versiculos_array
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/libros', methods=['GET'])
def obtener_libros():
    return jsonify({
        'libros': biblia_info.obtener_todos_libros()
    })

if __name__ == '__main__':
    app.run(debug=True) 