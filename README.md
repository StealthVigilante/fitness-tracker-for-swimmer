# Fitness Tracker for Swimmers

This is a web application built with Flask and AngularJS that serves as a fitness tracker for swimmers.
It allows users to log in, create new sessions, view past sessions, and calculate various metrics related to swimming workouts.

## Features

- **User Authentication**: Users can create an account and log in securely.
- **Session Creation**: Users can log their swimming sessions by entering lap slips, stroke count, and heart rate.
The application calculates metrics such as Swolf score, total distance, and workout density.
- **View Past Sessions**: Users can view their past swimming sessions along with calculated metrics.
- **New User Registration**: New users can register by providing a username and password.
- **Forgot Password**: Users can reset their password by entering their username and a new password.
- **Responsive Design**: The application is designed to work well on desktop and mobile devices.

## Installation

1. Clone the repository:
git clone https://github.com/StealthVigilante/fitness-tracker-for-swimmer.git

2. Install dependencies:
pip install -r requirements.txt

3. Set up the database:
- Create a MySQL database and configure the connection details in `config.py`.
- Run the database initialization script provided in `fitness_tracker.sql`.

4. Run the application:
python app.py

5. Access the application in your web browser at `http://localhost:5000`.

## Usage
- Visit the login page and log in with your username and password.
- Once logged in, you can create new sessions, view past sessions, or log out using the navigation buttons.
- To create a new session, enter the details in the provided form and click "Create Session".
- To view past sessions, click on the "Past Sessions" button.
- To register as a new user, click on the "New User" button on the login page and follow the instructions.
- If you forgot your password, click on the "Forgot Password" button on the login page and follow the instructions.
