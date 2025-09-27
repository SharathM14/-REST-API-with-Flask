from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage: A dictionary where keys are user IDs.
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}
next_id = 3 # ID for the next new user

# --- READ: Get ALL Users (GET /users) ---
@app.route('/users', methods=['GET'])
def get_all_users():
    # Converts the users dictionary into a list of objects for JSON response.
    user_list = [{"id": uid, **data} for uid, data in users.items()]
    return jsonify(user_list)

# --- READ: Get One User (GET /users/<id>) ---
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user_data = users.get(user_id)
    if user_data:
        # Return the user data with their ID
        return jsonify({"id": user_id, **user_data})
    return jsonify({"message": "User not found"}), 404

# --- CREATE: Add New User (POST /users) ---
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    
    # Get the user data sent as JSON
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"message": "Name is required"}), 400

    new_user = {"name": data['name'], "email": data.get('email', 'N/A')}

    # Assign and increment the ID
    users[next_id] = new_user
    new_id = next_id
    next_id += 1 

    # Respond with the new user and a 201 status (Created)
    return jsonify({"id": new_id, **new_user}), 201

# --- UPDATE: Change Existing User (PUT /users/<id>) ---
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = users.get(user_id)
    if not user_data:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    
    # Update name and email only if they are provided in the request body
    if 'name' in data:
        user_data['name'] = data['name']
    if 'email' in data:
        user_data['email'] = data['email']

    return jsonify({"id": user_id, **user_data})

# --- DELETE: Remove User (DELETE /users/<id>) ---
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        # 204 No Content is the standard response for successful deletion
        return '', 204
    return jsonify({"message": "User not found"}), 404


if __name__ == '__main__':
    # Runs the app on http://127.0.0.1:5000/
    app.run(debug=True)