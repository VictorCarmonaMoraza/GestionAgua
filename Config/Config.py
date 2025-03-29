import os


import os

def obtener_variable_utf8(nombre_variable):
    valor = os.environ.get(nombre_variable)
    if valor:
        try:
            return valor.encode('latin-1').decode('utf-8')  # o usa cp1252 en windows
        except UnicodeDecodeError:
            return valor
    return valor
class Config:
    URL_DB = os.environ.get('POSTGRES_URL', 'localhost')  # Usar variable de entorno o 'localhost' por defecto
    NAME_DB = os.environ.get('POSTGRES_DB', 'GestionAgua')  # Usar variable de entorno o 'ProyectoNumpy' por defecto
    USER_DB = os.environ.get('POSTGRES_USER', 'postgres')  # Usar variable de entorno o 'postgres' por defecto
    PASS_DB = os.environ.get('POSTGRES_PASSWORD', 'admin')  # Usar variable de entorno o 'admin' por defecto
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

'''class Config:
    URL_DB = os.environ.get('POSTGRES_URL', 'localhost')
    NAME_DB = os.environ.get('POSTGRES_DB', 'GestionAgua')
    USER_DB = os.environ.get('POSTGRES_USER', 'postgres')
    PASS_DB = os.environ.get('POSTGRES_PASSWORD', 'admin')
    PORT_DB = os.environ.get('POSTGRES_PORT', '5432')  # Porta padrão do PostgreSQL
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}:{PORT_DB}/{NAME_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def test_connection():
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=Config.URL_DB,
                database=Config.NAME_DB,
                user=Config.USER_DB,
                password=Config.PASS_DB,
                port=Config.PORT_DB
            )
            conn.close()
            print("Conexão com a base de dados bem-sucedida!")
        except psycopg2.Error as e:
            print(f"Erro ao conectar com a base de dados: {e}")'''