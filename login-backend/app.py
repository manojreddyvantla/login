from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt

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

# REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    password = data["password"]

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, username, hashed_password))
        db.commit()
        return jsonify({"message": "Registration Successful ✅"})
    except Exception as e:
        return jsonify({"message": "Email already exists ❌"})

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    query = "SELECT password FROM users WHERE email=%s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if user:
        stored_password = user[0]

        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return jsonify({"message": "Login Successful 🎉"})
    
    return jsonify({"message": "Invalid Credentials ❌"})


if __name__ == "__main__":
    app.run(debug=True)