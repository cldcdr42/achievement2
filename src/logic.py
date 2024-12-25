import psycopg2
import os
from datetime import datetime

# Specify Max number (N)
MAX_NUMBER = 100


def create_database_if_not_exists():
    """
    Check if the specified database exists, and create it if it does not.
    """
    db_host = os.getenv('DB_HOST', 'postgres_svc')  # Default to localhost
    db_user = os.getenv('POSTGRES_USER', 'root')  # Default to 'postgres'
    db_password = os.getenv('POSTGRES_PASSWORD', '123')  # Default to 'password'
    db_name = os.getenv('POSTGRES_DB', 'db')  # Default to 'mydatabase'
    db_port = int(os.getenv('DB_PORT', '5432'))  # Default to 5432

    print(f"DB Host: {db_host}")
    print(f"DB User: {db_user}")
    print(f"DB Password: {db_password}")
    print(f"DB Name: {db_name}")
    print(f"DB Port: {db_port}")

    # Connect to the default database ('postgres') to check for the existence of the target database
    conn = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database='postgres',
        port=db_port
    )
    conn.autocommit = True  # Enable autocommit for database creation
    cursor = conn.cursor()

    # Check if the database already exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cursor.fetchone()

    if not exists:
        # Create the database if it does not exist
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully.")
    else:
        print(f"Database '{db_name}' already exists.")

    cursor.close()
    conn.close()

def get_db_connection():
    """
    Create and return a PostgreSQL database connection using environment variables for configuration.
    """
    db_host = os.getenv('DB_HOST', 'postgres_svc')  # Default to localhost
    db_user = os.getenv('POSTGRES_USER', 'root')  # Default to 'postgres'
    db_password = os.getenv('POSTGRES_PASSWORD', '123')  # Default to 'password'
    db_name = os.getenv('POSTGRES_DB', 'db')  # Default to 'mydatabase'
    db_port = int(os.getenv('DB_PORT', '5432'))  # Default to 5432

    return psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        port=db_port
    )

def initialize_database():
    """
    Reinitialize the PostgreSQL database by dropping and recreating the numbers table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drop the table if it exists (clears the database)
    cursor.execute('DROP TABLE IF EXISTS numbers')

    # Recreate the table
    cursor.execute('''
        CREATE TABLE numbers (
            id SERIAL PRIMARY KEY,
            number INTEGER UNIQUE NOT NULL
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

def clear_logs():
    """
    Clear the logs.txt file by truncating its content.
    """
    with open("./logs.txt", "w") as log_file:
        log_file.write("")  # Overwrite the file with an empty string

def process_number(num):
    """
    Process the given number with the following rules:
    1. If the number is already in the database, return a message (case 1) and create a log.
    2. If number + 1 is already in the database, return a message (case 2) and create a log.
    3. If neither the number nor number + 1 is in the database, add the number and return a success message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the number or number + 1 exists in the database
    cursor.execute("SELECT number FROM numbers WHERE number = %s", (num,))
    is_num_in_db = cursor.fetchone()

    cursor.execute("SELECT number FROM numbers WHERE number = %s", (num + 1,))
    is_num_plus_one_in_db = cursor.fetchone()

    if is_num_in_db:
        # Case 1: Number already in the database
        log_message = f"Number {num} is already in the database (case 1)."
    elif is_num_plus_one_in_db:
        # Case 2: Number + 1 already in the database
        log_message = f"Number {num + 1} is already in the database (case 2)."
    else:
        # Case 3: Neither the number nor number + 1 is in the database
        cursor.execute("INSERT INTO numbers (number) VALUES (%s)", (num,))
        conn.commit()
        log_message = f"Response: {num + 1}. Number {num} has been added to the database."

    # Add timestamp to the log message
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {log_message}"

    # Write log to file
    with open("./logs.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

    cursor.close()
    conn.close()
    return log_message

def validate_number(input_number):
    """
    Validate the input number:
    1. Check if the input is a valid integer.
    2. Check if the input is within the allowed range (0 < number < N).
    """
    if not isinstance(input_number, int):
        return False, "The input must be a valid integer."

    if input_number <= 0 or input_number >= MAX_NUMBER:
        return False, f"The input must be between 1 and {MAX_NUMBER - 1}."

    return True, ""