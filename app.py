from flask import Flask, render_template, request, redirect, jsonify, url_for
import mysql.connector
from logic import check_conflicts
from datetime import datetime, timedelta

app = Flask(__name__)


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql123",
        database="dosebuddy"
    )


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


@app.route("/get_medicines")
def get_medicines():
    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM medicines")
    data = cursor.fetchall()

    # compute delayed status server-side (if not taken and > 30min late)
    now = datetime.now()
    for med in data:
        # med["time"] stored as "HH:MM" (string)
        try:
            med_time = datetime.combine(now.date(), datetime.strptime(med["time"], "%H:%M").time())
        except Exception:
            # if parsing fails, skip
            med_time = now

        # if status is not 'taken' and more than 30 minutes passed since scheduled time -> delayed
        if med.get("status") != "taken":
            if now > med_time + timedelta(minutes=30):
                med["status"] = "delayed"
            else:
                # keep stored status if not delayed
                med["status"] = med.get("status", "not_taken")

    cursor.close()
    db.close()

    return jsonify(data)


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
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT status FROM medicines WHERE id=%s", (id,))
    row = cursor.fetchone()
    current_status = row["status"] if row else "not_taken"

    if current_status == "taken":
        cursor.execute("UPDATE medicines SET status='not_taken', taken_time=NULL WHERE id=%s", (id,))
    else:
        cursor.execute("UPDATE medicines SET status='taken', taken_time=NOW() WHERE id=%s", (id,))

    db.commit()
    cursor.close()
    db.close()

    return jsonify({"success": True})




if __name__ == "__main__":
    app.run(debug=True)
