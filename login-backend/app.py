from flask import Flask, request
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="r00t1234",
    database="login_systemss"
)

cursor = db.cursor()

# ================= REGISTER =================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data["email"]
    username = data["username"]
    password = data["password"]

    # 🔐 Hash the password before storing
    hashed_password = generate_password_hash(password)

    try:
        query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, username, hashed_password))
        db.commit()
        return "Registration Successful ✅"
    except Exception as e:
        return "Email already exists ❌"

# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    # Get user by email
    query = "SELECT password FROM users WHERE email=%s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if user:
        stored_password = user[0]

        # 🔐 Check hashed password
        if check_password_hash(stored_password, password):
            return "Login Successful 🎉"
        else:
            return "Invalid Credentials ❌"
    else:
        return "Invalid Credentials ❌"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)