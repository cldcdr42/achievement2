from flask import Flask, request, jsonify
from logic import initialize_database, clear_logs, process_number, validate_number
from datetime import datetime
import os

app = Flask(__name__)

# Set base directory for logs and database
BASE_DIR = os.getenv("APP_BASE_DIR", os.path.dirname(os.path.abspath(__file__)))
REQUEST_LOGS_PATH = os.path.join(BASE_DIR, "request_logs.txt")

# Reinitialize database and clear logs
initialize_database()
clear_logs(REQUEST_LOGS_PATH)

@app.route('/process', methods=['POST'])
def process():
    """
    Handle POST requests to process a number.
    """
    data = request.get_json()

    # Check if the input is empty or missing
    if not data or 'number' not in data:
        error_message = "Invalid input. Please send a number."
        # Log the error
        with open(REQUEST_LOGS_PATH, "a") as log_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{timestamp} - {error_message}\n")
        return jsonify({"error": error_message}), 400

    input_number = data.get('number')

    # Validate the input number
    is_valid, error_message = validate_number(input_number)
    if not is_valid:
        # Log validation errors
        with open(REQUEST_LOGS_PATH, "a") as log_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{timestamp} - {error_message}\n")
        return jsonify({"error": error_message}), 400

    # Process the number and log the result
    result = process_number(input_number, REQUEST_LOGS_PATH)
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
