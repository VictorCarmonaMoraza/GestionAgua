from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Crea una instancia de SQLAlchemy


class Diposit(db.Model):
    __tablename__ = 'Deposito'  # Especifica el nombre de la tabla

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    capacidad = db.Column(db.DECIMAL, nullable=False)
    contenido = db.Column(db.DECIMAL, nullable=False)
    unidades = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.TIMESTAMP)
    activo = db.Column(db.Boolean, default=True)

    def __init__(self, id, nombre, capacidad, contenido, unidades=None, descripcion=None, fecha_creacion=None, activo=True):
        self.id = id
        self.nombre = nombre
        self.capacidad = capacidad
        self.contenido = contenido
        self.unidades = unidades
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.activo = activo

    def __repr__(self):
        return f'<Deposito {self.nombre}>'