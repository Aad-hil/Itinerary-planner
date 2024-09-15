Flask Itinerary Planner
A web application built with Flask that allows users to manage itineraries, explore places to visit with images from Unsplash, and contact the site administrators. This application supports user registration, login, and itinerary management, as well as reading place data from Excel and displaying it with dynamic images.

Features
User Authentication: Secure registration and login functionality with password hashing.
Itinerary Management: Add, view, and delete itineraries.
Places to Visit: Display a paginated list of places fetched from an Excel file with images from Unsplash.
Contact Form: Send messages to site administrators via email.
Responsive Design: Optimized for various devices with a user-friendly interface.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/yourusername/itinerary-planner.git
cd itinerary-planner
Set Up a Virtual Environment (recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Create the Database:

bash
Copy code
python main.py
This will create the SQLite database file (database.db) and the necessary tables.

Configure Environment Variables:

Create a .env file in the root directory and add your environment variables:

plaintext
Copy code
SECRET_KEY=your_secret_key
UNSPLASH_API_KEY=your_unsplash_api_key
SMTP_USER=your_email
SMTP_PASSWORD=your_password
Ensure these keys and credentials are kept secure and not exposed publicly.

Usage
Run the Flask Application:

bash
Copy code
python main.py
The application will start and be accessible at http://127.0.0.1:5000.

Navigate to the Application:

Homepage: Displays background information and a random image.
Register: Create a new user account.
Login: Access the application with your credentials.
Itinerary: View and manage your itineraries.
Places: Explore places with images from Unsplash.
Contact: Send a message to the administrators.
File Descriptions
main.py: Contains the main application logic, including routes, user models, itinerary management, and integration with the Unsplash API.
SendMail.py: Handles sending emails using SMTP for the contact form.
Contributing
Feel free to fork the repository, make changes, and submit pull requests. Contributions are welcome!

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Flask: The web framework used for this application.
SQLAlchemy: ORM used for database interactions.
Flask-Bcrypt: For password hashing.
Unsplash API: Provides images for the places.
pandas: Used for reading Excel files.
