from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
from logic import check_conflicts

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="dosebuddy"
)
cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    cursor.execute("SELECT * FROM medicines")
    meds = cursor.fetchall()
    return render_template("dashboard.html", medicines=meds)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        dosage = request.form["dosage"]
        time = request.form["time"]
        food = request.form["food"]

        cursor.execute("INSERT INTO medicines(name, dosage, time, food_type) VALUES(%s,%s,%s,%s)",
                       (name, dosage, time, food))
        db.commit()

        warning = check_conflicts(name, time, food)
        return render_template("success.html", warning=warning)

    return render_template("add.html")

@app.route("/get_medicines")
def get_medicines():
    cursor.execute("SELECT * FROM medicines")
    return jsonify(cursor.fetchall())

if __name__ == "__main__":
    app.run(debug=True)
