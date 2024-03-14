from flask import Flask, render_template, redirect, request, session
from mysql.connector import connect, Error
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Get database configuration from config.py
db_config = DB_CONFIG


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    try:
        # Establish database connection
        connection = connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user[0]  # Store user ID in session
            session['username'] = username  # Store username in session
            return redirect('/dashboard')
        else:
            return "Invalid username or password"
    except Error as e:
        return f"An error occurred: {e}"
    finally:
        if connection:
            connection.close()


@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect('/')


@app.route('/new-user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Insert new user into the database
        try:
            connection = connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            connection.commit()
            cursor.close()
            return redirect('/')
        except Error as e:
            return f"An error occurred: {e}"
        finally:
            if connection:
                connection.close()

    return render_template('new_user.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Update user's password in the database
        if new_password == confirm_password:
            try:
                connection = connect(**db_config)
                cursor = connection.cursor()
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
                connection.commit()
                cursor.close()
                return redirect('/')
            except Error as e:
                return f"An error occurred: {e}"
            finally:
                if connection:
                    connection.close()
        else:
            return "Passwords do not match"

    return render_template('forgot_password.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        username = session.get('username')
        return render_template('dashboard.html', username=username)
    else:
        return redirect('/')


@app.route('/create-session')
def create_session():
    if 'user_id' in session:
        username = session.get('username')
        return render_template('create_session.html', username=username)
    else:
        return redirect('/')


@app.route('/process-session', methods=['POST'])
def process_session():
    if request.method == 'POST':
        username = session.get('username')
        lap_slips = int(request.form['lap_slips'])
        stroke_count = int(request.form['stroke_count'])
        heart_rate = int(request.form['heart_rate'])

        # Calculations for swolf score, total distance, and workout density
        swolf_score = lap_slips + stroke_count
        total_distance = lap_slips * stroke_count
        workout_density = total_distance / (lap_slips * heart_rate)

        try:
            # Establish database connection
            connection = connect(**db_config)
            cursor = connection.cursor()

            # Get user ID from session
            user_id = session.get('user_id')

            # Insert session data into the database
            cursor.execute(
                '''INSERT INTO sessions (user_id, lap_slips, stroke_count, heart_rate, swolf_score,
                 total_distance, workout_density) VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (user_id, lap_slips, stroke_count, heart_rate, swolf_score, total_distance, workout_density))
            connection.commit()

            cursor.close()

            return redirect('/dashboard')
        except Error as e:
            return f"An error occurred: {e}"
        finally:
            if connection:
                connection.close()


@app.route('/past-sessions')
def past_sessions():
    if 'user_id' in session:
        username = session.get('username')
        user_id = session.get('user_id')
        # Retrieve past sessions for the logged-in user from the database
        try:
            connection = connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM sessions WHERE user_id=%s", (user_id,))
            sessions = cursor.fetchall()
            cursor.close()
            return render_template('past_sessions.html', username=username, sessions=sessions)
        except Error as e:
            return f"An error occurred: {e}"
        finally:
            if connection:
                connection.close()
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
