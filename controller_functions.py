from flask import Flask, render_template, redirect, flash, request, session
from config import app, db, func, IntegrityError, bcrypt, re
from models import Traveler, Trip

def home():
    return render_template("login.html")

def register():
    validation_check = Traveler.validate_traveler(request.form)
    if "_flashes" in session.keys() or not validation_check:
        flash("Registration unsuccessful. Please Try Again!")
        return redirect("/")
    else:
        try:
            new_traveler = Traveler.add_new_traveler(request.form)
            return redirect("/")
        except IntegrityError:
            db.session.rollback()
            flash("Sorry. This email already exists! Please Try Again!")
            return redirect("/")

def login():
    login_user = Traveler.query.filter_by(email = request.form["email"]).all()

    if login_user:
        session['user_id'] = login_user[0].id
        session['first_name'] = login_user[0].first_name
        hashed_password = login_user[0].password
        if bcrypt.check_password_hash(hashed_password, request.form['password']):
            session["logged_in"] = True
            session['user_id'] = login_user[0].id
            flash("You are logged in!")
            return redirect('/travels')
        else:
            session["logged_in"] = False
            flash("You could not be logged in. Try again or register")
        return redirect("/")
    else:
        flash("Email was not found. Please try again.")
        return redirect("/")
    return redirect("/")

def dashboard():
    try:
        login_name = session["first_name"]
    except:
        flash("Please login or register to continue.")
        return redirect("/")

    login_name = session["first_name"]
    login_id = session["user_id"]

    your_trips = db.session.query(Trip, Traveler).filter(Trip.planned_by_traveler_id == Traveler.id).filter(Traveler.id == login_id).all()

    your_joined_trips = db.session.query(Traveler, Trip).join(Trip, Traveler.traveler_joined_trip).filter(Traveler.id == login_id).all()



    other_trips = db.session.query(Trip, Traveler).filter(Trip.planned_by_traveler_id == Traveler.id).filter(Traveler.id != login_id).all()
    print(db.session.query(Traveler, Trip).join(Trip, Traveler.traveler_joined_trip))
    print(other_trips)

    # moved_trips = db.session.query(Traveler, Trip).join(Trip, Traveler.traveler_joined_trip).all()
    # print(moved_trips)

    return render_template("dashboard.html", login_name = login_name, login_id = login_id, your_trips = your_trips, your_joined_trips = your_joined_trips, other_trips = other_trips)

def view_add_trip_page():
    login_name = session["first_name"]
    login_id = session["user_id"]
    return render_template("add.html", login_name = login_name, login_id = login_id)

def add_trip():
    validation_check = Trip.validate_new_trip(request.form)
    if "_flashes" in session.keys() or not validation_check:
        return redirect("/travels/add")
    else:
        new_trip = Trip.add_trip(request.form)
        return redirect("/travels")

def cancel_trip():
    cancel_trip = Trip.cancel_trip(request.form)
    return redirect("/travels")

def leave_trip():
    existing_trip = Trip.query.get(request.form["leave_trip_value"])
    existing_traveler = Traveler.query.get(request.form["your_id"])
    existing_traveler.traveler_joined_trip.remove(existing_trip)
    db.session.commit()
    flash("You left this trip!")
    return redirect("/travels")

def join_trip():
    login_id = session["user_id"]
    join_once_trips = db.session.query(Traveler, Trip).join(Trip, Traveler.traveler_joined_trip).filter(Trip.id == request.form["join_trip_value"]).all()

    try:
        str(join_once_trips[0].Traveler.id) == str(login_id)
        flash("You already joined this trip!")
        return redirect("/travels")
    except:
        existing_trip = Trip.query.get(request.form["join_trip_value"])
        existing_traveler = Traveler.query.get(request.form["your_id"])
        existing_traveler.traveler_joined_trip.append(existing_trip)
        db.session.commit()
        flash("You joined this trip!")
        return redirect("/travels")

def see_view_trip_page(id):
    login_name = session["first_name"]
    login_id = session["user_id"]

    view_plan_with_creator = db.session.query(Trip, Traveler).filter(Trip.planned_by_traveler_id == Traveler.id).filter(Trip.id == id).all()
    first_name = view_plan_with_creator[0].Traveler.first_name
    last_name = view_plan_with_creator[0].Traveler.last_name
    plan = view_plan_with_creator[0].Trip.travel_plan
    travel_start_date = view_plan_with_creator[0].Trip.travel_start_date
    travel_end_date = view_plan_with_creator[0].Trip.travel_end_date

    travelers_on_this_trip = db.session.query(Trip, Traveler).join(Traveler, Trip.travelers_on_this_trip).filter(Trip.id == id).all()
    return render_template("view.html", login_name = login_name, login_id = login_id, first_name = first_name, last_name = last_name, plan = plan, travel_start_date = travel_start_date, travel_end_date = travel_end_date, this_trip = travelers_on_this_trip)

def logout():
    session['logged_in'] = False
    session.clear()
    flash("You have been logged out. Thank you for visiting Travel Buddy.")
    return redirect('/')