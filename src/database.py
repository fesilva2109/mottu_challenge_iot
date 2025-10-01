#pip install oracledb

import oracledb
import os

class DatabaseManager:
    def __init__(self):
        user = os.environ.get('DB_USER', 'rm555307')
        password = os.environ.get('DB_PASSWORD', '210905')
        dsn = os.environ.get('DB_DSN', 'oracle.fiap.com.br:1521/orcl')

        try:
            self.connection = oracledb.connect(user=user, password=password, dsn=dsn)
            self.cursor = self.connection.cursor()
            print("Conexão com o Oracle DB bem-sucedida.")
        except oracledb.DatabaseError as e:
            print(f"Erro ao conectar ao Oracle DB: {e}")
            self.connection = None
            self.cursor = None

    def insert_detection(self, moto_id, x, y):
        if not self.cursor:
            print("Não há conexão com o banco para inserir dados.")
            return

        sql = "INSERT INTO Detections (moto_id, center_x, center_y) VALUES (:1, :2, :3)"
        try:
            self.cursor.execute(sql, [moto_id, x, y])
            self.connection.commit()
        except oracledb.DatabaseError as e:
            print(f"Erro ao inserir no banco de dados: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Conexão com o Oracle DB fechada.")