import flask
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

EMAIL_ERROR_TEXT = 'The email address does not exist.'
PASSWORD_ERROR_TEXT = 'Password incorrect.'
REGISTER_ERROR_TEXT = 'You have already registered with this email address. Please log in instead.'

app = Flask(__name__)
app.config['SECRET_KEY'] = '08f3144fa9e589c8bebb26e24bb01faecf379ae849afd604156cddf8ea20e796'

# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


#create Flask-Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Creates a user loader callback
@login_manager.user_loader
def loader_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    ## Passing True or False if the user is authenticated.
    return render_template("index.html",logged_in=current_user.is_authenticated)


@app.route('/register', methods=['GET','POST'])
def register():
# """allow user to register and direct user to secrets page to download file."""
    error = None
    if request.method == "POST":
        # Find user by email entered.
        email_attempt = request.form.get("email")
        result = db.session.execute(db.select(User).where(User.email == email_attempt))
        user = result.scalar()
        if user: #if user is already in the db
            error = REGISTER_ERROR_TEXT
            return redirect(url_for('login'))
        else:

            # Hashing and salting the password entered by the user
            hash_and_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )

            # Storing the hashed password in our database
            new_user = User(email = request.form.get('email'),
                        password=hash_and_salted_password,
                        name = request.form.get('name'),
                        )
            db.session.add(new_user)
            db.session.commit()
            #Log in and authenticate user after adding details to the db
            login_user(new_user)

            # Can redirect() and get name from the current_user
            return redirect(url_for("secrets"))
    return render_template("register.html", error=error, logged_in=current_user.is_authenticated)


@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == "POST":
        email_attempt = request.form.get("email")
        password_attempt = request.form.get("password")

        # Find user by email entered.
        result = db.session.execute(db.select(User).where(User.email == email_attempt))
        user = result.scalar()
        if user: #if email address is valid
            # Check if the password entered is the same as the user's hash password in db
            if check_password_hash(user.password, password_attempt):
                login_user(user)
                return redirect(url_for('secrets'))
            else:
                error = PASSWORD_ERROR_TEXT
        else:
            error = EMAIL_ERROR_TEXT
    return flask.render_template('login.html', error=error,logged_in=current_user.is_authenticated)


## Only logged-in users can access the route
@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)   # this is to show you can pass the current_user name directly
    return render_template("secrets.html", name=current_user.name, logged_in=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Only logged-in users can down download the pdf
@app.route('/download', methods=['POST'])
@login_required
def download():
    filename = request.form['filename']
    """allow user to download cheat_sheet.pdf from the directory"""
    return send_from_directory(directory='static',path='files/cheat_sheet.pdf', as_attachment=True,)



if __name__ == "__main__":
    app.run(debug=True)
