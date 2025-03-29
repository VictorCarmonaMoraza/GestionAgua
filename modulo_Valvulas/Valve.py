from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Crea una instancia de SQLAlchemy

class Valve(db.Model):
    __tablename__ = 'Valvulas'  # Especifica el nombre de la tabla

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    diametro = db.Column(db.DECIMAL, nullable=False)
    deposito_id = db.Column(db.Integer, db.ForeignKey('Deposito.id'))  # Clave foránea
    impulsor_id = db.Column(db.Integer, db.ForeignKey('Impulsores.id'))  # Clave foránea
    descripcion = db.Column(db.Text)
    fecha_instalacion = db.Column(db.DATE)
    activo = db.Column(db.Boolean, default=True)

    def __init__(self, id, nombre, tipo, diametro, deposito_id=None, impulsor_id=None, descripcion=None, fecha_instalacion=None, activo=True):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.diametro = diametro
        self.deposito_id = deposito_id
        self.impulsor_id = impulsor_id
        self.descripcion = descripcion
        self.fecha_instalacion = fecha_instalacion
        self.activo = activo

    def __repr__(self):
        return f"Valvula(id={self.id}, nombre='{self.nombre}', tipo='{self.tipo}', diametro={self.diametro}, deposito_id={self.deposito_id}, impulsor_id={self.impulsor_id}, descripcion='{self.descripcion}', fecha_instalacion='{self.fecha_instalacion}', activo={self.activo})"