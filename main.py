from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
import pandas as pd
from SendMail import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)


# Itinerary model
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


with app.app_context():
    db.create_all()

UNSPLASH_API_KEY = 'YOUR API KEY'

def read_places_from_excel(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)
    # Convert the DataFrame to a list of dictionaries
    places_list = df.to_dict(orient='records')
    return places_list

def get_random_unsplash_image(query):
    url = 'https://api.unsplash.com/photos/random'
    params = {
        'query': query,
        'client_id': UNSPLASH_API_KEY,
        'orientation': 'landscape',
        'count': 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['urls']['regular']
    return None


def is_strong_password(password):
    # Check length of password
    if len(password) < 8:
        return False

    # Check for each required character category
    has_upper = any(char in uppercase for char in password)
    has_lower = any(char in lowercase for char in password)
    has_digit = any(char in digits for char in password)
    has_symbol = any(char in symbols for char in password)

    # Return True if all categories are present, False otherwise
    return has_upper and has_lower and has_digit and has_symbol


uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
symbols = '!@#$%^&*(),.?":{}|<>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Homepage Route
@app.route('/itinerary')
@login_required
def index():
    itineraries = Itinerary.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', itineraries=itineraries)


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        passwrd = request.form['password']
        if not is_strong_password(passwrd):
            flash(
                'Password does not meet the required strength (minimum 8 characters, uppercase, lowercase, number, '
                'and special character).',
                'danger')
            return redirect('/register')
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')


# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Add itinerary route
@app.route('/add', methods=['POST'])
@login_required
def add_itinerary():
    title = request.form['title']
    date = request.form['date']
    location = request.form['location']
    details = request.form['details']

    itinerary = Itinerary(title=title, date=date, location=location, details=details, user_id=current_user.id)
    db.session.add(itinerary)
    db.session.commit()
    flash('Itinerary added successfully!', 'success')
    return redirect(url_for('index'))


# Delete itinerary route
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_itinerary(id):
    itinerary = Itinerary.query.get_or_404(id)
    db.session.delete(itinerary)
    db.session.commit()
    flash('Itinerary deleted successfully!', 'success')
    return redirect(url_for('index'))


# Route for places to visit
@app.route('/places')
def places():
    file_path = 'output.xlsx'  # Update this path to your Excel file
    places_list = read_places_from_excel(file_path)
    # Fetch images for each place using Unsplash
    # Set the number of places per page
    places_per_page = 9

    # Get the page number from the query parameters (default is page 1)
    page = request.args.get('page', 1, type=int)

    # Calculate the start and end index for the places to show on this page
    start = (page - 1) * places_per_page
    end = start + places_per_page

    # Fetch images for each place on the current page using Unsplash
    for place in places_list[start:end]:
        place['image_url'] = get_random_unsplash_image(query=place['name'])

    # Slice the list to get only the places for the current page
    paginated_places = places_list[start:end]

    # Calculate the total number of pages
    total_pages = (len(places_list) + places_per_page - 1) // places_per_page

    return render_template(
        'places.html',
        places=paginated_places,
        current_page=page,
        total_pages=total_pages
    )


@app.route('/')
def about():
    background_image_url = get_random_unsplash_image(query='Itinerary Planner')
    return render_template('about.html', background_image_url=background_image_url)


# Contact Us page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        # Send email
        if send_email(name, email, subject, message):
            return render_template('contact.html', success_message="Your message has been sent successfully!")
        else:
            return render_template('contact.html', error_message="Failed to send your message. Please try again later.")

    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
