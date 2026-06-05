import csv
import os
import subprocess
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)

app = Flask(__name__)

# -------------------------
# HOME
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# REGISTER
# -------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]

        subprocess.run(
            ["python", "src/register.py", name]
        )

        return redirect("/")
    return render_template("register.html")


# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        subprocess.run(
            ["python", "src/recognize.py"]
        )

        return redirect("/attendance")

    return render_template("login.html")
# -------------------------
# ATTENDANCE DASHBOARD
# -------------------------

@app.route("/attendance")
def attendance():

    records = []

    os.makedirs("logs", exist_ok=True)

    attendance_file = "logs/attendance.csv"

    if os.path.exists(attendance_file):

        try:

            with open(
                attendance_file,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.reader(file)

                next(reader, None)

                records = list(reader)

        except Exception as e:

            print("Attendance Read Error:")
            print(e)

    total_users = 0
    total_records = len(records)

    if records:

        users = []

        for row in records:

            if len(row) > 0:
                users.append(row[0])

        total_users = len(set(users))

    # -------------------------
    # CREATE GRAPH
    # -------------------------

    try:

        import matplotlib.pyplot as plt

        dates = []

        for row in records:

            if len(row) > 1 and row[1]:

                date_part = row[1].split(" ")[0]

                dates.append(date_part)

        if len(dates) > 0:

            plt.figure(figsize=(6, 3))

            plt.hist(
                dates,
                bins=len(set(dates))
            )

            plt.title(
                "Daily Attendance Trend"
            )

            plt.xlabel("Date")
            plt.ylabel("Logins")

            plt.tight_layout()

            os.makedirs(
                "static",
                exist_ok=True
            )

            plt.savefig(
                "static/graph.png"
            )

            plt.close()

    except Exception as e:

        print("Graph Error:")
        print(e)

    return render_template(
        "attendance.html",
        records=records,
        total_users=total_users,
        total_records=total_records
    )


# -------------------------
# DOWNLOAD EXCEL
# -------------------------

@app.route("/download-excel")
def download_excel():

    csv_file = "logs/attendance.csv"

    excel_file = "logs/attendance.xlsx"

    if not os.path.exists(csv_file):

        return "Attendance file not found"

    try:

        df = pd.read_csv(csv_file)

        df.to_excel(
            excel_file,
            index=False
        )

        return send_file(
            excel_file,
            as_attachment=True
        )

    except Exception as e:

        return f"Excel Export Error: {e}"


# -------------------------
# REFRESH
# -------------------------

@app.route("/refresh")
def refresh():

    return redirect("/attendance")


# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )
