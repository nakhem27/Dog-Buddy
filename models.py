from config import db, re, func, flash, bcrypt, datetime, timedelta

users_and_walks = db.Table('users_and_walks',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('walk_id', db.Integer, db.ForeignKey('walk.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    date_of_birth = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    password = db.Column(db.String(60))
    image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_joined_walk = db.relationship('Walk', secondary = users_and_walks, backref='users_on_walk', cascade='all')

    @classmethod
    def validate_user(cls, new_user_data):
        is_valid = True
        if len(new_user_data["first_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_user_data["first_name"]):
            is_valid = False
            flash("Please enter a valid first name.")
        if len(new_user_data["last_name"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_user_data["last_name"]):
            is_valid = False
            flash("Please enter a valid last name. Must be between 3-20 characters in length and contain no numbers or special characters.")
        if len(new_user_data["email"]) < 1 or not re.search("[^@]+@[^@]+\.[^@]+", new_user_data["email"]):
            is_valid = False
            flash("Please enter a valid email address containing @ AND . followed by com/org/etc.")
        if len(new_user_data["phone_number"]) < 1 or not re.search("^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$", new_user_data["phone_number"]):
            is_valid = False
            flash("Please enter a valid phone number.")
        if new_user_data["confirm_password"] != new_user_data["password"]:
            is_valid = False
            flash("Passwords do not match!")
        try:
            birthday = datetime.strptime(new_user_data["birthday"], "%Y-%m-%d")
            diff = datetime.now() - birthday
            if int(diff.total_seconds()) < 56764800:
                is_valid = False
                flash("You must be 18 years old or older to register!")
        except:
            is_valid = False
            flash("Please enter a valid birthday.")
        return is_valid

    @classmethod
    def add_new_user(cls, new_user_data):
        add_user = cls(
            first_name = new_user_data["first_name"],
            last_name = new_user_data["last_name"],
            email = new_user_data["email"],
            phone_number = new_user_data["phone_number"],
            date_of_birth = new_user_data["birthday"],
            password = bcrypt.generate_password_hash(new_user_data["password"])
        )
        db.session.add(add_user)
        db.session.commit()
        flash("User successfully added! Login to view the Dog Buddy Dashboard!")
        return add_user

    @classmethod
    def edit_user(cls, edit_user_data):
        edit_user = User.query.get(edit_user_data["login_id"])
        edit_user.first_name = edit_user_data["first_name"]
        edit_user.last_name = edit_user_data["last_name"]
        edit_user.email = edit_user_data["email"]
        edit_user.date_of_birth = edit_user_data["birthday"]
        edit_user.phone_number = edit_user_data["phone_number"]
        edit_user.password = bcrypt.generate_password_hash(edit_user_data["password"])
        db.session.commit()
        flash("User Information Updated")
        return edit_user

class Dog(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    dog_name = db.Column(db.String(255))
    breed = db.Column(db.String(255))
    age = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    eye_color = db.Column(db.String(255))
    fur_color = db.Column(db.String(255))
    fur_type = db.Column(db.String(255))
    allergies = db.Column(db.String(255))
    brief_bio = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_with_dog = db.relationship('User', backref='Dog', cascade='all')

    @classmethod
    def validate_dog(cls, new_dog_data):
        is_valid = True
        if len(new_dog_data["dog_name"]) < 1:
            is_valid = False
            flash("Please enter a valid dog name.")
        if len(new_dog_data["breed"]) < 1:
            is_valid = False
            flash("Please enter a valid breed.")
        if len(new_dog_data["age"]) < 0:
            is_valid = False
            flash("Please enter a valid dog age.")
        if len(new_dog_data["eye_color"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_dog_data["eye_color"]):
            is_valid = False
            flash("Please enter a valid dog eye color.")
        if len(new_dog_data["fur_color"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_dog_data["fur_color"]):
            is_valid = False
            flash("Please enter a valid dog fur color.")
        if len(new_dog_data["fur_type"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_dog_data["fur_type"]):
            is_valid = False
            flash("Please enter a valid fur type.")
        if len(new_dog_data["allergies"]) < 1 or re.search("[^a-zA-ZäöüßÄÖÜ]", new_dog_data["allergies"]):
            is_valid = False
            flash("Please enter a valid dog allergies.")
        if len(new_dog_data["brief_bio"]) < 1 or len(new_dog_data["brief_bio"]) > 255:
            is_valid = False
            flash("Please enter a valid dog bio.")
        return is_valid

    @classmethod
    def add_dog(cls, new_dog_data):
        add_dog = cls(
            owner_id = new_dog_data["user_id"],
            dog_name = new_dog_data["dog_name"],
            breed = new_dog_data["breed"],
            age = new_dog_data["age"],
            gender = new_dog_data["gender"],
            eye_color = new_dog_data["eye_color"],
            fur_color = new_dog_data["fur_color"],
            fur_type = new_dog_data["fur_type"],
            allergies = new_dog_data["allergies"],
            brief_bio = new_dog_data["brief_bio"]
        )
        db.session.add(add_dog)
        db.session.commit()
        flash("Dog successfully added!")
        return add_dog
        

    @classmethod
    def edit_dog(cls, edit_dog_data):
        edit_dog = Dog.query.get(edit_dog_data["dog_id"])
        edit_dog.name = edit_dog_data["dog_name"]
        edit_dog.breed = edit_dog_data["breed"]
        edit_dog.age = edit_dog_data["age"]
        edit_dog.gender = edit_dog_data["gender"]
        edit_dog.eye_color = edit_dog_data["eye_color"]
        edit_dog.fur_color = edit_dog_data["fur_color"]
        edit_dog.fur_type = edit_dog_data["fur_type"]
        edit_dog.allergies = edit_dog_data["allergies"]
        edit_dog.brief_bio = edit_dog_data["brief_bio"]
        db.session.commit()
        flash(edit_dog.name +"'s Information Was Updated")
        return edit_dog

    @classmethod
    def delete_dog(cls, delete_dog_data):
        delete_dog = Dog.query.filter(Dog.id == delete_dog_data["dog_id"]).delete()
        db.session.commit()
        flash("Dog Information Deleted")
        return delete_dog

class Walk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planned_by_user_id = db.Column(db.Integer)
    location = db.Column(db.String(255))
    date = db.Column(db.String(255))
    time = db.Column(db.String(255))
    dogs = db.Column(db.String(255))
    walk_info = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    users_on_this_walk = db.relationship('User', secondary = users_and_walks, backref='user_joins_walks', cascade='all')
    
    @classmethod
    def validate_new_walk(cls, validate_new_walk):
        is_valid = True
        if len(validate_new_walk["location"]) < 1:
            is_valid = False
            flash("Location cannot be less than 1 character in length. Try again.")
        if validate_new_walk["walk_date"] == "":
            is_valid = False
            flash("Walk date missing.")
        elif validate_new_walk["walk_date"] < str(datetime.today()):
            is_valid = False
            flash("This walk can't be created in the past or on today's date. Please create a walk starting with tomorrow's date.")
        if validate_new_walk["walk_time"] == "":
            is_valid = False
            flash("Please enter a time.")
        if len(validate_new_walk["dogs"]) < 1:
            is_valid = False
            flash("You can't create a walk without dogs!")
        return is_valid

    @classmethod
    def add_walk(cls, add_walk_data):
        add_walk = cls(
            planned_by_user_id = add_walk_data["user_id"],
            location = add_walk_data["location"],
            date = datetime.strptime(add_walk_data["walk_date"], '%Y-%m-%d').strftime('%A, %B %d, %Y'),
            time = datetime.strptime(add_walk_data["walk_time"], '%H:%M').strftime('%I:%M %p'), 
            dogs = add_walk_data["dogs"],
            walk_info = add_walk_data["walk_info"]
        )
        db.session.add(add_walk)
        db.session.commit()
        flash("You created a walk!")
        return add_walk
    
    @classmethod
    def edit_walk(cls, edit_walk_data):
        edit_walk = Walk.query.get(edit_walk_data["edit_walk_value"])
        edit_walk.location = edit_walk_data["location"]
        edit_walk.date = datetime.strptime(edit_walk_data["walk_date"], '%Y-%m-%d').strftime('%A, %B %d, %Y')
        edit_walk.time = datetime.strptime(edit_walk_data["walk_time"], '%H:%M').strftime('%I:%M %p')
        edit_walk.dogs = edit_walk_data["dogs"]
        edit_walk.walk_info = edit_walk_data["walk_info"]
        db.session.add(edit_walk)
        db.session.commit()
        flash("Walk Information Updated")
        return edit_walk


    @classmethod
    def cancel_walk(cls, cancel_walk_data):
        cancel_walk = Walk.query.filter(Walk.id == cancel_walk_data["cancelled_walk_value"]).delete()
        db.session.commit()
        flash("You cancelled this walk!")
        return cancel_walk