import mysql.connector 
from utils.app_config import AppConfig

class DAL:

    # Constructor - start connection
    def __init__(self):
        self.connection = mysql.connector.connect(
            host= AppConfig.mysql_host,
            user= AppConfig.mysql_user,
            password= AppConfig.mysql_password,
            database= AppConfig.mysql_database
        )
    
    # Get table from DB 👍 
    def get_table(self, sql, params=None) -> dict:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(sql, params)
            table = cursor.fetchall()
            return table

    # Get one row from DB 👍
    def get_scalar(self, sql, params=None) -> dict:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(sql, params)
            row = cursor.fetchone() 
            return row  

    # Insert a row to DB 👍
    def insert(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()  #save to database now
            last_row_id = cursor.lastrowid
            return last_row_id
    
    # Update a row from DB 👍
    def update(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()
            row_count = cursor.rowcount
            return row_count  

    # Delete a row from DB 👍
    def delete(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()
            row_count = cursor.rowcount
            return row_count  
        
    # Close connection
    def close(self):
        self.connection.close()
