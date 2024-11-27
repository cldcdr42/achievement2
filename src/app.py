from flask import Flask, request, jsonify
from logic import initialize_database, clear_logs, process_number

app = Flask(__name__)

# Initialise and clear the database before each start of the application
initialize_database()
clear_logs()

@app.route('/process', methods=['POST'])
def process():
    """
    Handle HTPP POST number requests
    """
    data = request.get_json()
    number = data.get('number')

    # Validate input
    if not isinstance(number, int) or number < 0:
        return jsonify({"error": "Invalid input. Please send a natural number."}), 400

    # Process the number and return the result
    result = process_number(number)
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(debug=True)
