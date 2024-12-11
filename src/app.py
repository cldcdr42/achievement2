from flask import Flask, request, jsonify
from logic import initialize_database, clear_logs, process_number, validate_number
from datetime import datetime

app = Flask(__name__)

# Reinitialize database (clear it) and logs at the start of the app
initialize_database()
clear_logs()

@app.route('/process', methods=['POST'])
def process():
    """
    Handle POST requests to process a number.
    """
    data = request.get_json()

    # Check if the input is empty or missing
    if not data or 'number' not in data:
        return jsonify({"error": "Invalid input. Please send a number."}), 400

    input_number = data.get('number')

    # Validate if the input is a number and within the allowed range
    is_valid, error_message = validate_number(input_number)
    if not is_valid:
        # Log the invalid request
        with open("logs.txt", "a") as log_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_file.write(f"{timestamp} - {error_message}\n")
        return jsonify({"error": error_message}), 400

    # Process the valid number and return the result
    result = process_number(input_number)
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
