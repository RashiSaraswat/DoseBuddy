from flask import Flask, render_template, request, redirect, jsonify, url_for
import mysql.connector
from logic import check_conflicts
from datetime import datetime 

app = Flask(__name__)


# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql123",
        database="dosebuddy"
    )


# ---------------------------------------------------
# 🟢 DASHBOARD ROUTE (MAIN PAGE)
# ---------------------------------------------------
@app.route("/")
@app.route("/dashboard")
def dashboard():
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM medicines ORDER BY time ASC")
    meds = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", medicines=meds)



# ---------------------------------------------------
# 🟢 ADD MEDICINE (Modal)
# ---------------------------------------------------
@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    dosage = request.form["dosage"]
    time = request.form["time"]
    food = request.form["food"]

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "INSERT INTO medicines(name, dosage, time, food_type) VALUES (%s, %s, %s, %s)",
        (name, dosage, time, food)
    )
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("dashboard"))



# ---------------------------------------------------
# 🟢 GET ALL MEDICINES (JS Fetch API)
# ---------------------------------------------------
@app.route("/get_medicines")
def get_medicines():
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM medicines")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(data)



# ---------------------------------------------------
# 🟢 EDIT MEDICINE (Modal)
# ---------------------------------------------------
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    name = request.form["name"]
    dosage = request.form["dosage"]
    time = request.form["time"]
    food = request.form["food"]

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "UPDATE medicines SET name=%s, dosage=%s, time=%s, food_type=%s WHERE id=%s",
        (name, dosage, time, food, id)
    )
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("dashboard"))



# ---------------------------------------------------
# 🟢 DELETE MEDICINE (Modal, POST ONLY)
# ---------------------------------------------------
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("DELETE FROM medicines WHERE id=%s", (id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for("dashboard"))
@app.route("/mark_taken/<int:id>", methods=["POST"])
def mark_taken(id):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("UPDATE medicines SET status='taken' WHERE id=%s", (id,))
    db.commit()

    cursor.close()
    db.close()
    return jsonify({"success": True})



# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
