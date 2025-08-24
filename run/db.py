import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",       # change to your MySQL username
        password="samriddhi25",   # change to your MySQL password
        database="bankdb"
    )
    return connection