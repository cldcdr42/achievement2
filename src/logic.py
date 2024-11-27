import sqlite3
from datetime import datetime

# Specify the maximum allowed number (N)
MAX_NUMBER = 100  # Change this value to set the maximum number (N)

def initialize_database():
    """
    Reinitialize the SQLite database by dropping and recreating the numbers table.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Drop the table if it exists (clears the database)
    cursor.execute('DROP TABLE IF EXISTS numbers')
    
    # Recreate the table
    cursor.execute('''
        CREATE TABLE numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER UNIQUE NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def clear_logs():
    """
    Clear the logs.txt file by truncating its content.
    """
    with open("logs.txt", "w") as log_file:
        log_file.write("")  # Overwrite the file with an empty string

def process_number(num):
    """
    Process the given number with the following rules:
    1. If the number is already in the database, return a message.
    2. If number + 1 is already in the database, return a message.
    3. If neither the number nor number + 1 is in the database, add the number and return a success message.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the number or number + 1 exists in the database
    cursor.execute("SELECT number FROM numbers WHERE number = ?", (num,))
    is_num_in_db = cursor.fetchone()

    cursor.execute("SELECT number FROM numbers WHERE number = ?", (num + 1,))
    is_num_plus_one_in_db = cursor.fetchone()

    if is_num_in_db:
        # Case 1: Number already in the database
        log_message = f"Number {num} is already in the database."
    elif is_num_plus_one_in_db:
        # Case 2: Number + 1 already in the database
        log_message = f"Number {num + 1} is already in the database."
    else:
        # Case 3: Neither the number nor number + 1 is in the database
        cursor.execute("INSERT INTO numbers (number) VALUES (?)", (num,))
        conn.commit()
        log_message = f"Response: {num + 1}. Number {num} has been added to the database."

    # Add timestamp to the log message
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {log_message}"

    # Write log to file
    with open("logs.txt", "a") as log_file:
        log_file.write(log_entry + "\n")

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
