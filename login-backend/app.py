from flask import Flask, request
from flask_cors import CORS
import mysql.connector

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

    try:
        query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (email, username, password))
        db.commit()
        return "Registration Successful ✅"
    except:
        return "Email already exists ❌"

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        return "Login Successful 🎉"
    else:
        return "Invalid Credentials ❌"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)