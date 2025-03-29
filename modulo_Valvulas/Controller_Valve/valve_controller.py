from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import swag_from

from modulo_Valvulas.Valve import Valve, db

valve_controller = Blueprint('valvulas', __name__, url_prefix='/valvulas')


@valve_controller.route('/', methods=['GET'])
@swag_from({
    'tags': ['Valvulas'],
    'description': 'Obtiene todas las valvulas',
    'responses': {
        200: {
            'description': 'Lista de valvulas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'tipo': {'type': 'string'},
                        'diametro': {'type': 'string'},
                        'deposito_id': {'type': 'integer'},
                        'impulsor_id': {'type': 'integer'},
                        'descripcion': {'type': 'string'},
                        'fecha_instalacion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_valvulas():
    valvulas = Valve.query.all()
    resultados = [{
        'id': valvula.id,
        'nombre': valvula.nombre,
        'tipo': valvula.tipo,
        'diametro': str(valvula.diametro),
        'deposito_id': valvula.deposito_id,
        'impulsor_id': valvula.impulsor_id,
        'descripcion': valvula.descripcion,
        'fecha_instalacion': str(valvula.fecha_instalacion),
        'activo': valvula.activo
    } for valvula in valvulas]
    return jsonify(resultados)


@valve_controller.route('/<int:valvula_id>', methods=['GET'])
@swag_from({
    'tags': ['Valvulas'],
    'description': 'Obtiene una valvula por su ID',
    'parameters': [
        {
            'name': 'valvula_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la valvula'
        }
    ],
    'responses': {
        200: {
            'description': 'Valvula encontrada',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'nombre': {'type': 'string'},
                    'tipo': {'type': 'string'},
                    'diametro': {'type': 'string'},
                    'deposito_id': {'type': 'integer'},
                    'impulsor_id': {'type': 'integer'},
                    'descripcion': {'type': 'string'},
                    'fecha_instalacion': {'type': 'string'},
                    'activo': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Valvula no encontrada'
        }
    }
})
def obtener_valvula(valvula_id):
    valvula = Valve.query.get(valvula_id)
    if valvula:
        return jsonify({
            'id': valvula.id,
            'nombre': valvula.nombre,
            'tipo': valvula.tipo,
            'diametro': str(valvula.diametro),
            'deposito_id': valvula.deposito_id,
            'impulsor_id': valvula.impulsor_id,
            'descripcion': valvula.descripcion,
            'fecha_instalacion': str(valvula.fecha_instalacion),
            'activo': valvula.activo
        })
    return jsonify({'mensaje': 'Válvula no encontrada'}), 404


@valve_controller.route('/', methods=['POST'])
@swag_from({
    'tags': ['Valvulas'],
    'description': 'Crea una o varias valvulas',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'description': 'Datos de la valvula',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'tipo': {'type': 'string'},
                    'diametro': {'type': 'string'},
                    'deposito_id': {'type': 'integer'},
                    'impulsor_id': {'type': 'integer'},
                    'descripcion': {'type': 'string'},
                    'fecha_instalacion': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Valvula creada',
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
            'description': 'Error al crear valvula'
        }
    }
})
def crear_valvulas():
    datos = request.get_json()
    if not datos:
        return jsonify({'mensaje': 'Datos no proporcionados'}), 400

    if isinstance(datos, list):
        nuevas_valvulas = []
        for valvula_data in datos:
            if not all(k in valvula_data for k in ('nombre', 'tipo', 'diametro')):
                return jsonify({'mensaje': 'Datos incompletos'}), 400
            try:
                nueva_valvula = Valve(
                    nombre=valvula_data['nombre'],
                    tipo=valvula_data['tipo'],
                    diametro=valvula_data['diametro'],
                    deposito_id=valvula_data.get('deposito_id'),
                    impulsor_id=valvula_data.get('impulsor_id'),
                    descripcion=valvula_data.get('descripcion'),
                    fecha_instalacion=valvula_data.get('fecha_instalacion')
                )
                db.session.add(nueva_valvula)
                nuevas_valvulas.append(nueva_valvula)
            except Exception as e:
                db.session.rollback()
                return jsonify({'mensaje': f'Error al crear valvula: {str(e)}'}), 500

        db.session.commit()
        return jsonify(
            [{'id': valvula.id, 'nombre': valvula.nombre} for valvula in nuevas_valvulas]), 201
    else:
        if not all(k in datos for k in ('nombre', 'tipo', 'diametro')):
            return jsonify({'mensaje': 'Datos incompletos'}), 400
        try:
            nueva_valvula = Valve(
                nombre=datos['nombre'],
                tipo=datos['tipo'],
                diametro=datos['diametro'],
                deposito_id=datos.get('deposito_id'),
                impulsor_id=datos.get('impulsor_id'),
                descripcion=datos.get('descripcion'),
                fecha_instalacion=datos.get('fecha_instalacion')
            )
            db.session.add(nueva_valvula)
            db.session.commit()
            return jsonify({'id': nueva_valvula.id, 'nombre': nueva_valvula.nombre}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'mensaje': f'Error al crear valvula: {str(e)}'}), 500


@valve_controller.route('/<int:valvula_id>', methods=['PUT'])
@swag_from({
    'tags': ['Valvulas'],
    'description': 'Actualiza una valvula existente',
    'parameters': [
        {
            'name': 'valvula_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la valvula'
        },
        {
            'name': 'body',
            'in': 'body',
            'description': 'Datos actualizados de la valvula',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nombre': {'type': 'string'},
                    'tipo': {'type': 'string'},
                    'diametro': {'type': 'string'},
                    'deposito_id': {'type': 'integer'},
                    'impulsor_id': {'type': 'integer'},
                    'descripcion': {'type': 'string'},
                    'fecha_instalacion': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Valvula actualizada'
        },
        404: {
            'description': 'Valvula no encontrada'
        }
    }
})
def actualizar_valvula(valvula_id):
    valvula = Valve.query.get(valvula_id)
    if valvula:
        datos = request.get_json()
        valvula.nombre = datos.get('nombre', valvula.nombre)
        valvula.tipo = datos.get('tipo', valvula.tipo)
        valvula.diametro = datos.get('diametro', valvula.diametro)
        valvula.deposito_id = datos.get('deposito_id', valvula.deposito_id)
        valvula.impulsor_id = datos.get('impulsor_id', valvula.impulsor_id)
        valvula.descripcion = datos.get('descripcion', valvula.descripcion)
        valvula.fecha_instalacion = datos.get('fecha_instalacion', valvula.fecha_instalacion)
        db.session.commit()
        return jsonify({'mensaje': 'Válvula actualizada'})
    return jsonify({'mensaje': 'Válvula no encontrada'}), 404


@valve_controller.route('/<int:valvula_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Valvulas'],
    'description': 'Borra una valvula',
    'parameters': [
        {
            'name': 'valvula_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la valvula'
        }
    ],
    'responses': {
        200: {
            'description': 'Valvula borrada'
        },
        404: {
            'description': 'Valvula no encontrada'
        }
    }
})
def borrar_valvula(valvula_id):
    valvula = Valve.query.get(valvula_id)
    if valvula:
        db.session.delete(valvula)
        db.session.commit()
        return jsonify({'mensaje': 'Válvula borrada'})
    return jsonify({'mensaje': 'Válvula no encontrada'}), 404


@valve_controller.route('/<int:valvula_id>/activar', methods=['PUT'])
@swag_from({
    'tags': ['Valvulas'],
    'description': 'Activa una valvula',
    'parameters': [
        {
            'name': 'valvula_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la valvula'
        }
    ],
    'responses': {
        200: {
            'description': 'Valvula activada'
        },
        404: {
            'description': 'Valvula no encontrada'
        }
    }
})
def activar_valvula(valvula_id):
    valvula = Valve.query.get(valvula_id)
    if valvula:
        valvula.activo = True
        db.session.commit()
        return jsonify({'mensaje': 'Válvula activada'})
    return jsonify({'mensaje': 'Válvula no encontrada'}), 404


@valve_controller.route('/activas', methods=['GET'])
@swag_from({
    'tags': ['Valvulas'],
    'description': 'Obtiene todas las valvulas activas',
    'responses': {
        200: {
            'description': 'Lista de valvulas activas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'tipo': {'type': 'string'},
                        'diametro': {'type': 'string'},
                        'deposito_id': {'type': 'integer'},
                        'impulsor_id': {'type': 'integer'},
                        'descripcion': {'type': 'string'},
                        'fecha_instalacion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_valvulas_activas():
    valvulas_activas = Valve.query.filter_by(activo=True).all()
    resultados = [{
        'id': valvula.id,
        'nombre': valvula.nombre,
        'tipo': valvula.tipo,
        'diametro': str(valvula.diametro),
        'deposito_id': valvula.deposito_id,
        'impulsor_id': valvula.impulsor_id,
        'descripcion': valvula.descripcion,
        'fecha_instalacion': str(valvula.fecha_instalacion),
        'activo': valvula.activo
    } for valvula in valvulas_activas]
    return jsonify(resultados)


@valve_controller.route('/inactivas', methods=['GET'])
@swag_from({
    'tags': ['Valvulas'],
    'description': 'Obtiene todas las valvulas inactivas',
    'responses': {
        200: {
            'description': 'Lista de valvulas inactivas',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'nombre': {'type': 'string'},
                        'tipo': {'type': 'string'},
                        'diametro': {'type': 'string'},
                        'deposito_id': {'type': 'integer'},
                        'impulsor_id': {'type': 'integer'},
                        'descripcion': {'type': 'string'},
                        'fecha_instalacion': {'type': 'string'},
                        'activo': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def obtener_valvulas_inactivas():
    valvulas_inactivas = Valve.query.filter_by(activo=False).all()
    resultados = [{
        'id': valvula.id,
        'nombre': valvula.nombre,
        'tipo': valvula.tipo,
        'diametro': str(valvula.diametro),
        'deposito_id': valvula.deposito_id,
        'impulsor_id': valvula.impulsor_id,
        'descripcion': valvula.descripcion,
        'fecha_instalacion': str(valvula.fecha_instalacion),
        'activo': valvula.activo
    } for valvula in valvulas_inactivas]
    return jsonify(resultados)