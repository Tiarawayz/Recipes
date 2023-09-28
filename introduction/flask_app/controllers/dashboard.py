from flask_app import app
from flask import render_template, request, flash, redirect, session
from flask_app.models.user import User

@app.route('/dashboard')
def list():

    if "uid" not in session:
        flash("You're not logged in!")
        return redirect("/login")
    user = User.get_user_by_id(session["uid"])
    return render_template("dashboard.html", user=user)

@app.route('/report')
def report():
    return render_template('report.html')