# Itinerary Planner Flask App

This project is a web application built using Flask, which helps users manage their itineraries, view places to visit with images, and send contact messages via email. It also includes user authentication features and integration with the Unsplash API.

## Features

- **User Authentication**: Register, login, and logout functionality.
- **Itinerary Management**: Add, view, and delete itineraries.
- **Places to Visit**: Display a paginated list of places with images fetched from Unsplash.
- **Contact Form**: Send messages via email.

## Getting Started

To get started with this project, follow these instructions:

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Aad-hil/Itinerary-planner.git
   cd itinerary-planner
   ```
2. Set Up a Virtual Environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Create the Database
   ```bash
   python main.py
   ```
   This will create the SQLite database file (database.db) and the necessary tables.
5. Configure Environment Variables
   Create a .env file in the root directory and add your environment variables:
   ```plaintext
   SECRET_KEY=your_secret_key
   UNSPLASH_API_KEY=your_unsplash_api_key
   SMTP_USER=your_email
   SMTP_PASSWORD=your_password
   ```
   Ensure these keys and credentials are kept secure and not exposed publicly.
# Usage
## Run the Flask Application
```bash
python main.py
```
The application will start and be accessible at http://127.0.0.1:5000.

## Navigate to the Application
- **Homepage**: Displays background information and a random image.
- **Register**: Create a new user account.
- **Login**: Access the application with your credentials.
- **Itinerary**: View and manage your itineraries.
- **Places**: Explore places with images from Unsplash.
- **Contact**: Send a message to the administrators.
# File Descriptions
- ***main.py***: Contains the main application logic, including routes, user models, itinerary management, and integration with the Unsplash API.
-***SendMail.py***: Handles sending emails using SMTP for the contact form.
# Contributing
Feel free to fork the repository, make changes, and submit pull requests. Contributions are welcome!

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments
- **Flask**: The web framework used for this application.
- **SQLAlchemy**: ORM used for database interactions.
- **Flask-Bcrypt**: For password hashing.
- **Unsplash API**: Provides images for the places.
- **pandas**: Used for reading Excel files.
