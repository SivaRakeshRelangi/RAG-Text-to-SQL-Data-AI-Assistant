import mysql.connector
from app.config import MYSQL_CONFIG

def get_connection():
    conn = mysql.connector.connect(
        **MYSQL_CONFIG
    )
    return conn