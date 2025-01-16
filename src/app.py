from flask import Flask, request, jsonify
import re
from buscar_versiculos import buscar_versiculos
from biblia_info import BibliaInfo
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
biblia_info = BibliaInfo()

# Configuración de Swagger UI
SWAGGER_URL = '/docs'  # URL para acceder a UI
API_URL = '/static/swagger.json'  # Nuestro archivo API spec

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de la Biblia"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Endpoint para servir el archivo swagger.json
@app.route("/static/swagger.json")
def specs():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "API de la Biblia",
            "description": "API para consultar versículos y libros de la Biblia",
            "version": "1.0.0",
            "contact": {
                "name": "API Biblia",
                "url": "https://github.com/tuusuario/temas_biblicos"
            }
        },
        "paths": {
            "/api/versiculos": {
                "get": {
                    "tags": ["Versículos"],
                    "summary": "Obtener versículos de la Biblia",
                    "description": "Retorna versículos específicos de la Biblia según la referencia proporcionada",
                    "parameters": [
                        {
                            "name": "referencia",
                            "in": "query",
                            "required": True,
                            "schema": {
                                "type": "string"
                            },
                            "description": "Referencia bíblica en formato: 'Libro Capítulo, Versículo(s)'\nEjemplos:\n- 'Gn 1, 1'\n- 'Sal 23'\n- '1 Co 1, 3-6'\n- 'Is 40, 3-'\n- 'Jn 1, -5'"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Versículos encontrados",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "referencia": {
                                                "type": "object",
                                                "properties": {
                                                    "libro": {
                                                        "type": "object",
                                                        "properties": {
                                                            "abreviatura": {"type": "string"},
                                                            "nombre": {"type": "string"},
                                                            "testamento": {"type": "string", "enum": ["AT", "NT"]}
                                                        }
                                                    },
                                                    "capitulo": {"type": "integer"},
                                                    "versiculos": {"type": "string"}
                                                }
                                            },
                                            "versiculos": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Error en la petición",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "error": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/libros": {
                "get": {
                    "tags": ["Libros"],
                    "summary": "Obtener lista de libros de la Biblia",
                    "description": "Retorna la lista completa de libros de la Biblia con su información",
                    "responses": {
                        "200": {
                            "description": "Lista de libros",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "libros": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "Libro": {"type": "string"},
                                                        "Abrev": {"type": "string"},
                                                        "Total": {"type": "integer"},
                                                        "Testamento": {"type": "string", "enum": ["AT", "NT"]}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    })

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
        
        abrev, nombre_completo, testamento = libro_info
        
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
                    'nombre': nombre_completo,
                    'testamento': testamento
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
    libros = biblia_info.obtener_todos_libros()
    # Reemplazar guiones bajos por espacios en el campo 'Libro'
    for libro in libros:
        libro['Libro'] = libro['Libro'].replace('_', ' ')
    return jsonify({
        'libros': libros
    })

if __name__ == '__main__':
    app.run(debug=True) 