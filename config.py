import MySQLdb

def get_db_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        password="samriddhi25",
        database="bank_db"
    )
