from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import swag_from

from modulo_Impulsores.Driving import Driving, db

driving_controller = Blueprint('impulsores', __name__, url_prefix='/impulsores')

@driving_controller.route('/', methods=['GET'])
@swag_from({
    'tags': ['Impulsores'],
    'description': 'Obtiene todos los impulsores',
    'responses': {
        200: {
            'description': 'Lista de impulsores',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'tipo': {'type': 'string'},
                        'caudal': {'type': 'string'},
                        'potencia': {'type': 'string'},
                        'deposito_id': {'type': 'integer'},
                        'descripcion': {'type': 'string'},
                        'fecha_instalacion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_impulsores():
    impulsores = Driving.query.all()
    resultados = [{
        'id': impulsor.id,
        'nombre': impulsor.nombre,
        'tipo': impulsor.tipo,
        'caudal': str(impulsor.caudal),
        'potencia': str(impulsor.potencia),
        'deposito_id': impulsor.deposito_id,
        'descripcion': impulsor.descripcion,
        'fecha_instalacion': str(impulsor.fecha_instalacion),
        'activo': impulsor.activo
    } for impulsor in impulsores]
    return jsonify(resultados)

@driving_controller.route('/<int:impulsor_id>', methods=['GET'])
@swag_from({
    'tags': ['Impulsores'],
    'description': 'Obtiene un impulsor por su ID',
    'parameters': [
        {
            'name': 'impulsor_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del impulsor'
        }
    ],
    'responses': {
        200: {
            'description': 'Impulsor encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nombre': {'type': 'string'},
                    'tipo': {'type': 'string'},
                    'caudal': {'type': 'string'},
                    'potencia': {'type': 'string'},
                    'deposito_id': {'type': 'integer'},
                    'descripcion': {'type': 'string'},
                    'fecha_instalacion': {'type': 'string'},
                    'activo': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Impulsor no encontrado'
        }
    }
})
def obtener_impulsor(impulsor_id):
    impulsor = Driving.query.get(impulsor_id)
    if impulsor:
        return jsonify({
            'id': impulsor.id,
            'nombre': impulsor.nombre,
            'tipo': impulsor.tipo,
            'caudal': str(impulsor.caudal),
            'potencia': str(impulsor.potencia),
            'deposito_id': impulsor.deposito_id,
            'descripcion': impulsor.descripcion,
            'fecha_instalacion': str(impulsor.fecha_instalacion),
            'activo': impulsor.activo
        })
    return jsonify({'mensaje': 'Impulsor no encontrado'}), 404

@driving_controller.route('/', methods=['POST'])
@swag_from({
    'tags': ['Impulsores'],
    'description': 'Crea uno o varios impulsores',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'description': 'Datos del impulsor',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'tipo': {'type': 'string'},
                    'caudal': {'type': 'string'},
                    'potencia': {'type': 'string'},
                    'deposito_id': {'type': 'integer'},
                    'descripcion': {'type': 'string'},
                    'fecha_instalacion': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Impulsor creado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nombre': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Datos no proporcionados o incompletos'
        },
        500: {
            'description': 'Error al crear impulsor'
        }
    }
})
def crear_impulsores():
    datos = request.get_json()
    if not datos:
        return jsonify({'mensaje': 'Datos no proporcionados'}), 400

    if isinstance(datos, list):
        nuevos_impulsores = []
        for impulsor_data in datos:
            if not all(k in impulsor_data for k in ('nombre', 'tipo', 'caudal')):
                return jsonify({'mensaje': 'Datos incompletos'}), 400
            try:
                nuevo_impulsor = Driving(
                    nombre=impulsor_data['nombre'],
                    tipo=impulsor_data['tipo'],
                    caudal=impulsor_data['caudal'],
                    potencia=impulsor_data.get('potencia'),
                    deposito_id=impulsor_data.get('deposito_id'),
                    descripcion=impulsor_data.get('descripcion'),
                    fecha_instalacion=impulsor_data.get('fecha_instalacion')
                )
                db.session.add(nuevo_impulsor)
                nuevos_impulsores.append(nuevo_impulsor)
            except Exception as e:
                db.session.rollback()
                return jsonify({'mensaje': f'Error al crear impulsor: {str(e)}'}), 500

        db.session.commit()
        return jsonify([{'id': impulsor.id, 'nombre': impulsor.nombre} for impulsor in nuevos_impulsores]), 201
    else:
        try:
            nuevo_impulsor = Driving(
                nombre=datos['nombre'],
                tipo=datos['tipo'],
                caudal=datos['caudal'],
                potencia=datos.get('potencia'),
                deposito_id=datos.get('deposito_id'),
                descripcion=datos.get('descripcion'),
                fecha_instalacion=datos.get('fecha_instalacion')
            )
            db.session.add(nuevo_impulsor)
            db.session.commit()
            return jsonify({'id': nuevo_impulsor.id, 'nombre': nuevo_impulsor.nombre}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'mensaje': f'Error al crear impulsor: {str(e)}'}), 500

@driving_controller.route('/<int:impulsor_id>', methods=['PUT'])
@swag_from({
    'tags': ['Impulsores'],
    'description': 'Actualiza un impulsor existente',
    'parameters': [
        {
            'name': 'impulsor_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del impulsor'
        },
        {
            'name': 'body',
            'in': 'body',
            'description': 'Datos actualizados del impulsor',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'tipo': {'type': 'string'},
                    'caudal': {'type': 'string'},
                    'potencia': {'type': 'string'},
                    'deposito_id': {'type': 'integer'},
                    'descripcion': {'type': 'string'},
                    'fecha_instalacion': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Impulsor actualizado'
        },
        404: {
            'description': 'Impulsor no encontrado'
        }
    }
})
def actualizar_impulsor(impulsor_id):
    impulsor = Driving.query.get(impulsor_id)
    if impulsor:
        datos = request.get_json()
        impulsor.nombre = datos.get('nombre', impulsor.nombre)
        impulsor.tipo = datos.get('tipo', impulsor.tipo)
        impulsor.caudal = datos.get('caudal', impulsor.caudal)
        impulsor.potencia = datos.get('potencia', impulsor.potencia)
        impulsor.deposito_id = datos.get('deposito_id', impulsor.deposito_id)
        impulsor.descripcion = datos.get('descripcion', impulsor.descripcion)
        impulsor.fecha_instalacion = datos.get('fecha_instalacion', impulsor.fecha_instalacion)
        db.session.commit()
        return jsonify({'mensaje': 'Impulsor actualizado'})
    return jsonify({'mensaje': 'Impulsor no encontrado'}), 404

@driving_controller.route('/<int:impulsor_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Impulsores'],
    'description': 'Borra un impulsor',
    'parameters': [
        {
            'name': 'impulsor_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del impulsor'
        }
    ],
    'responses': {
        200: {
            'description': 'Impulsor borrado'
        },
        404: {
            'description': 'Impulsor no encontrado'
        }
    }
})
def borrar_impulsor(impulsor_id):
    impulsor = Driving.query.get(impulsor_id)
    if impulsor:
        db.session.delete(impulsor)
        db.session.commit()
        return jsonify({'mensaje': 'Impulsor borrado'})
    return jsonify({'mensaje': 'Impulsor no encontrado'}), 404

@driving_controller.route('/<int:impulsor_id>/activar', methods=['PUT'])
@swag_from({
    'tags': ['Impulsores'],
    'description': 'Activa un impulsor',
    'parameters': [
        {
            'name': 'impulsor_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del impulsor'
        }
    ],
    'responses': {
        200: {
            'description': 'Impulsor activado'
        },
        404: {
            'description': 'Impulsor no encontrado'
        }
    }
})
def activar_impulsor(impulsor_id):
    impulsor = Driving.query.get(impulsor_id)
    if impulsor:
        impulsor.activo = True
        db.session.commit()
        return jsonify({'mensaje': 'Impulsor activado'})
    return jsonify({'mensaje': 'Impulsor no encontrado'}), 404

@driving_controller.route('/activos', methods=['GET'])
@swag_from({
    'tags': ['Impulsores'],
    'description': 'Obtiene todos los impulsores activos',
    'responses': {
        200: {
            'description': 'Lista de impulsores activos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'tipo': {'type': 'string'},
                        'caudal': {'type': 'string'},
                        'potencia': {'type': 'string'},
                        'deposito_id': {'type': 'integer'},
                        'descripcion': {'type': 'string'},
                        'fecha_instalacion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_impulsores_activos():
    impulsores_activos = Driving.query.filter_by(activo=True).all()
    resultados = [{
        'id': impulsor.id,
        'nombre': impulsor.nombre,
        'tipo': impulsor.tipo,
        'caudal': str(impulsor.caudal),
        'potencia': str(impulsor.potencia),
        'deposito_id': impulsor.deposito_id,
        'descripcion': impulsor.descripcion,
        'fecha_instalacion': str(impulsor.fecha_instalacion),
        'activo': impulsor.activo
    } for impulsor in impulsores_activos]
    return jsonify(resultados)

@driving_controller.route('/inactivos', methods=['GET'])
@swag_from({
    'tags': ['Impulsores'],
    'description': 'Obtiene todos los impulsores inactivos',
    'responses': {
        200: {
            'description': 'Lista de impulsores inactivos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'tipo': {'type': 'string'},
                        'caudal': {'type': 'string'},
                        'potencia': {'type': 'string'},
                        'deposito_id': {'type': 'integer'},
                        'descripcion': {'type': 'string'},
                        'fecha_instalacion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_impulsores_inactivos():
    impulsores_inactivos = Driving.query.filter_by(activo=False).all()
    resultados = [{
        'id': impulsor.id,
        'nombre': impulsor.nombre,
        'tipo': impulsor.tipo,
        'caudal': str(impulsor.caudal),
        'potencia': str(impulsor.potencia),
        'deposito_id': impulsor.deposito_id,
        'descripcion': impulsor.descripcion,
        'fecha_instalacion': str(impulsor.fecha_instalacion),
        'activo': impulsor.activo
    } for impulsor in impulsores_inactivos]
    return jsonify(resultados)