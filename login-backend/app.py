from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import random

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

# Temporary OTP storage
otp_storage = {}

# REGISTER (No password stored)
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data["email"]
    username = data["username"]

    try:
        query = "INSERT INTO users (email, username) VALUES (%s, %s)"
        cursor.execute(query, (email, username))
        db.commit()
        return jsonify({"message": "Registration Successful ✅"})
    except:
        return jsonify({"message": "Email already exists ❌"})


# SEND OTP
@app.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    email = data["email"]

    query = "SELECT * FROM users WHERE email=%s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "User not registered ❌"})

    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    print("OTP for", email, "is:", otp)  # For testing (check terminal)

    return jsonify({"message": "OTP Sent ✅"})


# VERIFY OTP (Login)
@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data["email"]
    user_otp = data["otp"]

    if email in otp_storage and otp_storage[email] == user_otp:
        del otp_storage[email]
        return jsonify({"message": "Login Successful 🎉"})
    
    return jsonify({"message": "Invalid OTP ❌"})


if __name__ == "__main__":
    app.run(debug=True)