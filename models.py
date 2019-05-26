from config import db, re, func, flash, bcrypt, datetime, timedelta

travelers_and_trips = db.Table('travelers_and_trips',
    db.Column('traveler_id', db.Integer, db.ForeignKey('traveler.id'), primary_key=True),
    db.Column('trip_id', db.Integer, db.ForeignKey('trip.id'), primary_key=True)
)

class Traveler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    date_of_birth = db.Column(db.String(255))
    password = db.Column(db.String(60))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    traveler_joined_trip = db.relationship('Trip', secondary = travelers_and_trips, backref='travelers_on_trip', cascade='all')

# dog data base not implemented but the code is written out 
class Dog(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    dog_name = db.Column(db.String(255))
    breed = db.Column(db.String(255))
    eye_color = db.Column(db.String(255))
    date_of_birth = db.Column(db.String(255))
    fur_color = db.Column(db.String(255))
    fur_type = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    def validate_traveler(cls, new_traveler_data):
        is_valid = True
        if len(new_traveler_data["first_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_traveler_data["first_name"]):
            is_valid = False
            flash("Please enter a valid first name.")
        if len(new_traveler_data["last_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_traveler_data["last_name"]):
            is_valid = False
            flash("Please enter a valid last name. Must be between 3-20 characters in length and contain no numbers or special characters.")
        if len(new_traveler_data["email"]) < 1 or not re.search("[^@]+@[^@]+\.[^@]+", new_traveler_data["email"]):
            is_valid = False
            flash("Please enter a valid email address containing @ AND . followed by com/org/etc.")
        if len(new_traveler_data["password"]) < 8:
            is_valid = False
            flash("Password should be at least 8 characters and contain one number and uppercase letter")
        if new_traveler_data["confirm_password"] != new_traveler_data["password"]:
            is_valid = False
            flash("Passwords do not match!")
        try:
            birthday = datetime.strptime(new_traveler_data["dob"], "%Y-%m-%d")
            diff = datetime.now() - birthday
            if int(diff.total_seconds()) < 56764800:
                is_valid = False
                flash("You must be 18 years old or older to register!")
        except:
            is_valid = False
            flash("Please enter a valid birthday.")
        return is_valid

    @classmethod
    def add_new_traveler(cls, new_traveler_data):
        add_traveler = cls(
            first_name = new_traveler_data["first_name"],
            last_name = new_traveler_data["last_name"],
            email = new_traveler_data["email"],
            date_of_birth = new_traveler_data["dob"],
            password = bcrypt.generate_password_hash(new_traveler_data["password"])
        )
        db.session.add(add_traveler)
        db.session.commit()
        flash("User successfully added! Login to view the Travel Buddy Dashboard!")
        return add_traveler

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planned_by_traveler_id = db.Column(db.Integer)
    destination = db.Column(db.String(255))
    travel_plan = db.Column(db.String(255))
    travel_start_date = db.Column(db.String(255))
    travel_end_date = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    travelers_on_this_trip = db.relationship('Traveler', secondary = travelers_and_trips, backref='traveler_joins_trip', cascade='all')
    
    @classmethod
    def validate_new_trip(cls, validate_trip):
        is_valid = True

        if len(validate_trip["destination"]) < 1:
            is_valid = False
            flash("Destination cannot be less than 1 character in length. Try again.")
        if len(validate_trip["plan"]) < 1:
            is_valid = False
            flash("Travel plan cannot be less than 1 character in length. Try again.")

        if validate_trip["travel_start_date"] == "":
            is_valid = False
            flash("Start travel date missing.")
        elif validate_trip["travel_start_date"] < str(datetime.today()):
            is_valid = False
            flash("This trip can't be created in the past or on today's date. Please create a trip starting with tomorrow's date.")
        
        if validate_trip["travel_end_date"] == "":
            is_valid = False
            flash("End travel date missing.")
        elif validate_trip["travel_end_date"] <= validate_trip["travel_start_date"]:
            is_valid = False
            flash("End travel date can't end before the start date.")
        return is_valid

    @classmethod
    def add_trip(cls, add_trip_data):
        add_trip = cls(
            planned_by_traveler_id = add_trip_data["user_id"],
            destination = add_trip_data["destination"],
            travel_plan = add_trip_data["plan"],
            travel_start_date = add_trip_data["travel_start_date"],
            travel_end_date = add_trip_data["travel_end_date"]
        )
        db.session.add(add_trip)
        db.session.commit()
        flash("You added a trip!")
        return add_trip

    @classmethod
    def cancel_trip(cls, cancel_trip_data):
        cancel_trip = Trip.query.filter(Trip.id == cancel_trip_data["cancelled_trip_value"]).delete()
        db.session.commit()
        flash("You cancelled this trip!")
        return cancel_trip