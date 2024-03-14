import mysql.connector

# Function to connect to the database
def connect():
    return mysql.connector.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        database='your_database'
    )

# Function to execute a query
def execute_query(query, data=None):
    connection = connect()
    cursor = connection.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    connection.commit()
    connection.close()
