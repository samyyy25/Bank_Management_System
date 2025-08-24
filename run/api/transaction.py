from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from config import get_db_connection

transaction_bp = Blueprint("transaction", __name__, template_folder="../templates")

@transaction_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, balance FROM users WHERE id=%s", (session["user_id"],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("dashboard.html", user=user)

@transaction_bp.route("/deposit", methods=["POST"])
def deposit():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    amount = float(request.form["amount"])
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET balance = balance + %s WHERE id=%s", (amount, session["user_id"]))
    cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
                   (session["user_id"], "deposit", amount))
    conn.commit()

    cursor.close()
    conn.close()
    flash("Deposit successful!")
    return redirect(url_for("transaction.dashboard"))

@transaction_bp.route("/withdraw", methods=["POST"])
def withdraw():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    amount = float(request.form["amount"])
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE id=%s", (session["user_id"],))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE id=%s", (amount, session["user_id"]))
        cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)",
                       (session["user_id"], "withdraw", amount))
        conn.commit()
        flash("Withdrawal successful!")
    else:
        flash("Insufficient balance!")

    cursor.close()
    conn.close()
    return redirect(url_for("transaction.dashboard"))

@transaction_bp.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, amount, created_at FROM transactions WHERE user_id=%s ORDER BY created_at DESC", (session["user_id"],))
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("history.html", transactions=transactions)
