from flask import Flask, render_template, redirect, flash, request, session
from config import app, db, func, IntegrityError, bcrypt, re, datetime, timedelta
from models import User, Dog, Walk

def home():
    return render_template("login.html")

def register():
    validation_check = User.validate_user(request.form)
    if "_flashes" in session.keys() or not validation_check:
        flash("Registration unsuccessful. Please Try Again!")
        return redirect("/")
    else:
        try:
            new_User = User.add_new_user(request.form)
            return redirect("/")
        except IntegrityError:
            db.session.rollback()
            flash("Sorry. This email already exists! Please Try Again!")
            return redirect("/")

def login():
    login_user = User.query.filter_by(email = request.form["email"]).all()

    if login_user:
        session['user_id'] = login_user[0].id
        session['first_name'] = login_user[0].first_name
        hashed_password = login_user[0].password
        if bcrypt.check_password_hash(hashed_password, request.form['password']):
            session["logged_in"] = True
            session['user_id'] = login_user[0].id
            flash("You are logged in!")
            return redirect('/dashboard')
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
    past = datetime.now() - timedelta(days=1)
    present = datetime.now()

    your_dogs = db.session.query(Dog).filter(Dog.owner_id == login_id).all()
    your_walks = db.session.query(Walk, User).filter(Walk.planned_by_user_id == User.id).filter(User.id == login_id).all()
    your_joined_walks = db.session.query(User, Walk).join(Walk, User.user_joined_walk).filter(User.id == login_id).all()
    other_walks = db.session.query(Walk, User).filter(Walk.planned_by_user_id == User.id).filter(User.id != login_id).all()
    print(db.session.query(User, Walk).join(Walk, User.user_joined_walk))
    print(other_walks)
    return render_template("dashboard.html", login_name = login_name, login_id = login_id, your_dogs = your_dogs, your_walks = your_walks, your_joined_walks = your_joined_walks, other_walks = other_walks, past = past, present = present)

def myaccount():
    login_id = session["user_id"]
    your_dogs = db.session.query(Dog).filter(Dog.owner_id == login_id).all()
    return render_template("myaccount.html", your_dogs = your_dogs)

def addadog():
    validation_check = Dog.validate_dog(request.form)
    if "_flashes" in session.keys() or not validation_check:
        return redirect("/dashboard")
    else:
        new_dog = Dog.add_dog(request.form)
        return redirect("/dashboard")

def viewdog(id):
    login_name = session["first_name"]
    login_id = session["user_id"]
    your_dogs = db.session.query(Dog).filter(Dog.owner_id == login_id).all()
    one_dog = db.session.query(Dog).filter(Dog.id == id).all()
    return render_template("view_dog.html", one_dog = one_dog, your_dogs = your_dogs)

def add_walk():
    validation_check = Walk.validate_new_walk(request.form)
    if "_flashes" in session.keys() or not validation_check:
        return redirect("/dashboard")
    else:
        new_walk = Walk.add_walk(request.form)
        return redirect("/dashboard")

def cancel_walk():
    cancel_walk = Walk.cancel_walk(request.form)
    return redirect("/dashboard")

def leave_walk():
    existing_walk = Walk.query.get(request.form["leave_walk_value"])
    existing_user = User.query.get(request.form["your_id"])
    existing_user.user_joined_walk.remove(existing_walk)
    db.session.commit()
    flash("You left this walk!")
    return redirect("/dashboard")

def join_walk():
    login_id = session["user_id"]
    join_once_walks = db.session.query(User, Walk).join(Walk, User.user_joined_walk).filter(Walk.id == request.form["join_walk_value"]).all()

    try:
        str(join_once_walks[0].User.id) == str(login_id)
        flash("You already joined this Walk!")
        return redirect("/dashboard")
    except:
        existing_walk = Walk.query.get(request.form["join_walk_value"])
        existing_user = User.query.get(request.form["your_id"])
        existing_user.user_joined_walk.append(existing_walk)
        db.session.commit()
        flash("You joined this Walk!")
        return redirect("/dashboard")

def see_view_walk_page(id):
    login_name = session["first_name"]
    login_id = session["user_id"]
    your_dogs = db.session.query(Dog).filter(Dog.owner_id == login_id).all()

    view_plan_with_creator = db.session.query(Walk, User).filter(Walk.planned_by_user_id == User.id).filter(Walk.id == id).all()
    first_name = view_plan_with_creator[0].User.first_name
    last_name = view_plan_with_creator[0].User.last_name
    email = view_plan_with_creator[0].User.email
    phone_number = view_plan_with_creator[0].User.phone_number
    walk_date = view_plan_with_creator[0].Walk.date
    walk_time = view_plan_with_creator[0].Walk.time
    walk_location = view_plan_with_creator[0].Walk.location
    walk_info = view_plan_with_creator[0].Walk.walk_info
    travel_start_date = view_plan_with_creator[0].Walk.travel_start_date
    travel_end_date = view_plan_with_creator[0].Walk.travel_end_date

    users_on_this_Walk = db.session.query(Walk, User).join(User, Walk.users_on_this_walk).filter(Walk.id == id).all()
    return render_template("view.html", login_name = login_name, login_id = login_id, first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, walk_date = walk_date, talk_time = walk_time, walk_location = walk_location, this_walk = users_on_this_walk, your_dogs = your_dogs)

def logout():
    session['logged_in'] = False
    session.clear()
    flash("You have been logged out. Thank you for visiting Dog Buddy.")
    return redirect('/')