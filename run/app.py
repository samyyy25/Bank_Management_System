from flask import Flask, render_template, redirect, url_for, session
from api.auth import auth_bp
from api.transaction import transaction_bp

app = Flask(__name__)
app.secret_key = "secretkey"

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(transaction_bp, url_prefix="/transaction")

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("transaction.dashboard"))
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)
