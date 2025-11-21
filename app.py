from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector
from logic import check_conflicts
from datetime import datetime 

app = Flask(__name__)


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql123",
        database="dosebuddy"
    )


# ---------------------------------------------------
# 🟢 HOME ROUTE (Working)
# ---------------------------------------------------
@app.route('/')
def home():

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    # If your table "sample" doesn't exist, create it or remove this query
    try:
        cursor.execute("SELECT message FROM sample LIMIT 1")
        result = cursor.fetchone()
        message = result["message"] if result else "Welcome!"
    except:
        message = "Welcome!"

    cursor.close()
    db.close()

    return render_template("index.html", message=message)


# ---------------------------------------------------
# 🟢 ADD MEDICINE
# ---------------------------------------------------
@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":
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

        warning = check_conflicts(name, time, food)
        return render_template("success.html", warning=warning)

    return render_template("add.html")


# ---------------------------------------------------
# 🟢 GET ALL MEDICINES (for JS)
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
# 🟢 EDIT MEDICINE
# ---------------------------------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM medicines WHERE id=%s", (id,))
    med = cursor.fetchone()

    if request.method == "POST":
        name = request.form["name"]
        dosage = request.form["dosage"]
        time = request.form["time"]
        food = request.form["food"]

        cursor.execute(
            "UPDATE medicines SET name=%s, dosage=%s, time=%s, food_type=%s WHERE id=%s",
            (name, dosage, time, food, id)
        )
        db.commit()

        cursor.close()
        db.close()
        return redirect("/")

    cursor.close()
    db.close()
    return render_template("edit.html", med=med)


# ---------------------------------------------------
# 🟢 DELETE MEDICINE
# ---------------------------------------------------
@app.route("/delete/<int:id>")
def delete(id):
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("DELETE FROM medicines WHERE id=%s", (id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
