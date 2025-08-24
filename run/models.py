from run.db import get_db_connection

def register_customer(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, balance) VALUES (%s, %s)", (name, 0))
    conn.commit()
    new_id = cursor.lastrowid   # ✅ get the last inserted ID
    conn.close()
    return new_id


def deposit_money(customer_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET balance = balance + %s WHERE id = %s", (amount, customer_id))
    conn.commit()
    conn.close()


def withdraw_money(customer_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM customers WHERE id = %s", (customer_id,))
    result = cursor.fetchone()

    if result is None:  # customer not found
        conn.close()
        return "Customer Not Found"

    balance = result[0]

    if balance >= amount:
        cursor.execute("UPDATE customers SET balance = balance - %s WHERE id = %s", (amount, customer_id))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


def check_balance(customer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM customers WHERE id = %s", (customer_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None