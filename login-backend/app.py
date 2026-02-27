from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# ================= DATABASE CONNECTION =================
DATABASE_URL = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# ================= REGISTER =================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data["email"]
    username = data["username"]
    password = data["password"]

    hashed_password = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)",
            (email, username, hashed_password)
        )
        conn.commit()
        return "Registration Successful ✅"
    except:
        return "Email already exists ❌"

# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    cursor.execute("SELECT password FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        if check_password_hash(user[0], password):
            return "Login Successful 🎉"
        else:
            return "Invalid Credentials ❌"
    else:
        return "Invalid Credentials ❌"

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)