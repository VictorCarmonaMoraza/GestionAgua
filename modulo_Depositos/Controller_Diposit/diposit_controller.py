from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import swag_from

from modulo_Depositos.Diposit import Diposit, db

diposit_controller = Blueprint('depositos', __name__, url_prefix='/depositos')


@diposit_controller.route('/', methods=['GET'])
@swag_from({
    'tags': ['Depositos'],
    'description': 'Obtiene todos los depositos',
    'responses': {
        200: {
            'description': 'Lista de depositos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'capacidad': {'type': 'string'},
                        'contenido': {'type': 'string'},
                        'unidades': {'type': 'string'},
                        'descripcion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_depositos():
    depositos = Diposit.query.all()
    resultados = [{
        'id': deposito.id,
        'nombre': deposito.nombre,
        'capacidad': str(deposito.capacidad),
        'contenido': str(deposito.contenido),
        'unidades': deposito.unidades,
        'descripcion': deposito.descripcion,
        'activo': deposito.activo
    } for deposito in depositos]
    return jsonify(resultados)


@diposit_controller.route('/<int:deposito_id>', methods=['GET'])
@swag_from({
    'tags': ['Depositos'],
    'description': 'Obtiene un depósito por su ID',
    'parameters': [
        {
            'name': 'deposito_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del deposito'
        }
    ],
    'responses': {
        200: {
            'description': 'Deposito encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nombre': {'type': 'string'},
                    'capacidad': {'type': 'string'},
                    'contenido': {'type': 'string'},
                    'unidades': {'type': 'string'},
                    'descripcion': {'type': 'string'},
                    'activo': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Deposito no encontrado'
        }
    }
})
def obtener_deposito(deposito_id):
    deposito = Diposit.query.get(deposito_id)
    if deposito:
        return jsonify({
            'id': deposito.id,
            'nombre': deposito.nombre,
            'capacidad': str(deposito.capacidad),
            'contenido': str(deposito.contenido),
            'unidades': deposito.unidades,
            'descripcion': deposito.descripcion,
            'activo': deposito.activo
        })
    return jsonify({'mensaje': 'Deposito no encontrado'}), 404


@diposit_controller.route('/', methods=['POST'])
@swag_from({
    'tags': ['Depositos'],
    'description': 'Crea uno o varios depositos',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'description': 'Datos del deposito',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'capacidad': {'type': 'string'},
                    'contenido': {'type': 'string'},
                    'unidades': {'type': 'string'},
                    'descripcion': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Deposito creado',
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
            'description': 'Error al crear deposito'
        }
    }
})
def crear_depositos():
    datos = request.get_json()
    if not datos:
        return jsonify({'mensaje': 'Datos no proporcionados'}), 400

    if isinstance(datos, list):
        nuevos_depositos = []
        for deposito_data in datos:
            if not all(k in deposito_data for k in ('nombre', 'capacidad', 'contenido')):
                return jsonify({'mensaje': 'Datos incompletos'}), 400
            try:
                nuevo_deposito = Diposit(
                    nombre=deposito_data['nombre'],
                    capacidad=deposito_data['capacidad'],
                    contenido=deposito_data['contenido'],
                    unidades=deposito_data.get('unidades'),
                    descripcion=deposito_data.get('descripcion')
                )
                db.session.add(nuevo_deposito)
                nuevos_depositos.append(nuevo_deposito)
            except Exception as e:
                db.session.rollback()
                return jsonify({'mensaje': f'Error al crear deposito: {str(e)}'}), 500

        db.session.commit()
        return jsonify(
            [{'id': deposito.id, 'nombre': deposito.nombre} for deposito in nuevos_depositos]), 201
    else:
        if not all(k in datos for k in ('nombre', 'capacidad', 'contenido')):
            return jsonify({'mensaje': 'Datos incompletos'}), 400
        try:
            nuevo_deposito = Diposit(
                nombre=datos['nombre'],
                capacidad=datos['capacidad'],
                contenido=datos['contenido'],
                unidades=datos.get('unidades'),
                descripcion=datos.get('descripcion')
            )
            db.session.add(nuevo_deposito)
            db.session.commit()
            return jsonify({'id': nuevo_deposito.id, 'nombre': nuevo_deposito.nombre}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'mensaje': f'Error al crear deposito: {str(e)}'}), 500


@diposit_controller.route('/<int:deposito_id>', methods=['PUT'])
@swag_from({
    'tags': ['Depositos'],
    'description': 'Actualiza un deposito existente',
    'parameters': [
        {
            'name': 'deposito_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del deposito'
        },
        {
            'name': 'body',
            'in': 'body',
            'description': 'Datos actualizados del deposito',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'capacidad': {'type': 'string'},
                    'contenido': {'type': 'string'},
                    'unidades': {'type': 'string'},
                    'descripcion': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Deposito actualizado'
        },
        404: {
            'description': 'Deposito no encontrado'
        }
    }
})
def actualizar_deposito(deposito_id):
    deposito = Diposit.query.get(deposito_id)
    if deposito:
        datos = request.get_json()
        deposito.nombre = datos.get('nombre', deposito.nombre)
        deposito.capacidad = datos.get('capacidad', deposito.capacidad)
        deposito.contenido = datos.get('contenido', deposito.contenido)
        deposito.unidades = datos.get('unidades', deposito.unidades)
        deposito.descripcion = datos.get('descripcion', deposito.descripcion)
        db.session.commit()
        return jsonify({'mensaje': 'Deposito actualizado'})
    return jsonify({'mensaje': 'Deposito no encontrado'}), 404


@diposit_controller.route('/<int:deposito_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Depositos'],
    'description': 'Borra un deposito',
    'parameters': [
        {
            'name': 'deposito_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del deposito'
        }
    ],
    'responses': {
        200: {
            'description': 'Deposito borrado'
        },
        404: {
            'description': 'Deposito no encontrado'
        }
    }
})
def borrar_deposito(deposito_id):
    deposito = Diposit.query.get(deposito_id)
    if deposito:
        db.session.delete(deposito)
        db.session.commit()
        return jsonify({'mensaje': 'Deposito borrado'})
    return jsonify({'mensaje': 'Deposito no encontrado'}), 404


@diposit_controller.route('/<int:deposito_id>/activar', methods=['PUT'])
@swag_from({
    'tags': ['Depositos'],
    'description': 'Activa un deposito',
    'parameters': [
        {
            'name': 'deposito_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del deposito'
        }
    ],
    'responses': {
        200: {
            'description': 'Deposito activado'
        },
        404: {
            'description': 'Deposito no encontrado'
        }
    }
})
def activar_deposito(deposito_id):
    deposito = Diposit.query.get(deposito_id)
    if deposito:
        deposito.activo = True
        db.session.commit()
        return jsonify({'mensaje': 'Deposito activado'})
    return jsonify({'mensaje': 'Deposito no encontrado'}), 404


@diposit_controller.route('/activos', methods=['GET'])
@swag_from({
    'tags': ['Depositos'],
    'description': 'Obtiene todos los depositos activos',
    'responses': {
        200: {
            'description': 'Lista de depositos activos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'capacidad': {'type': 'string'},
                        'contenido': {'type': 'string'},
                        'unidades': {'type': 'string'},
                        'descripcion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_depositos_activos():
    depositos_activos = Diposit.query.filter_by(activo=True).all()
    resultados = [{
        'id': deposito.id,
        'nombre': deposito.nombre,
        'capacidad': str(deposito.capacidad),
        'contenido': str(deposito.contenido),
        'unidades': deposito.unidades,
        'descripcion': deposito.descripcion,
        'activo': deposito.activo
    } for deposito in depositos_activos]
    return jsonify(resultados)


@diposit_controller.route('/inactivos', methods=['GET'])
@swag_from({
    'tags': ['Depositos'],
    'description': 'Obtiene todos los depositos inactivos',
    'responses': {
        200: {
            'description': 'Lista de depositos inactivos',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'capacidad': {'type': 'string'},
                        'contenido': {'type': 'string'},
                        'unidades': {'type': 'string'},
                        'descripcion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_depositos_inactivos():
    depositos_inactivos = Diposit.query.filter_by(activo=False).all()
    resultados = [{
        'id': deposito.id,
        'nombre': deposito.nombre,
        'capacidad': str(deposito.capacidad),
        'contenido': str(deposito.contenido),
        'unidades': deposito.unidades,
        'descripcion': deposito.descripcion,
        'activo': deposito.activo
    } for deposito in depositos_inactivos]
    return jsonify(resultados)