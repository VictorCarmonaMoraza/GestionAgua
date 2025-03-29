from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Crea una instancia de SQLAlchemy

class Driving(db.Model):
    __tablename__ = 'Impulsores'  # Especifica el nombre de la tabla

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    caudal = db.Column(db.DECIMAL, nullable=False)
    potencia = db.Column(db.DECIMAL)
    deposito_id = db.Column(db.Integer, db.ForeignKey('Deposito.id'))  # Clave foránea
    descripcion = db.Column(db.Text)
    fecha_instalacion = db.Column(db.DATE)
    activo = db.Column(db.Boolean, default=True)

    def __init__(self, id, nombre, tipo, caudal, potencia=None, deposito_id=None, descripcion=None, fecha_instalacion=None, activo=True):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.caudal = caudal
        self.potencia = potencia
        self.deposito_id = deposito_id
        self.descripcion = descripcion
        self.fecha_instalacion = fecha_instalacion
        self.activo = activo

    def __repr__(self):
        return f"Impulsor(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}', caudal={self.caudal}, potencia={self.potencia}, deposito_id={self.deposito_id}, descripcion='{self.descripcion}', fecha_instalacion='{self.fecha_instalacion}', activo={self.activo})"