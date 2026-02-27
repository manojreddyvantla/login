const express = require("express");
const mysql = require("mysql2");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// MySQL Connection
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "r00t1234",
  database: "login_db"
});

db.connect((err) => {
  if (err) {
    console.log("Database connection failed:", err);
  } else {
    console.log("Connected to MySQL ✅");
  }
});

// REGISTER API
app.post("/register", (req, res) => {
  console.log("Register Body:", req.body);

  const { email, username, password } = req.body;

  const sql = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)";

  db.query(sql, [email, username, password], (err, result) => {
    if (err) {
      console.log("Register Error:", err);
      res.status(500).send("Register Error");
    } else {
      res.send("Registered Successfully ✅");
    }
  });
});

// LOGIN API
app.post("/login", (req, res) => {
  const { email, password } = req.body;

  const sql = "SELECT * FROM users WHERE email=? AND password=?";
  
  db.query(sql, [email, password], (err, result) => {
    if (err) {
      res.status(500).send("Error");
    } else if (result.length > 0) {
      res.send("Login Successful ✅");
    } else {
      res.send("Invalid Email or Password ❌");
    }
  });
});

app.listen(5000, () => {
  console.log("Server running on http://localhost:5000");
});