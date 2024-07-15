from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Login'  # Replace 'Login' with your database name
mongo = PyMongo(app)

# Route for user signup
@app.route('/signup', methods=['POST'])
def signup():
    users = mongo.db.users
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username or password missing'}), 400

    existing_user = users.find_one({'username': username})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    # Insert user into MongoDB
    result = users.insert_one({'username': username, 'password': password})

    return jsonify({'message': 'User created successfully', 'username': username}), 201

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username or password missing'}), 400

    user = users.find_one({'username': username, 'password': password})
    if user:
        return jsonify({'message': 'Login successful', 'username': username}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
