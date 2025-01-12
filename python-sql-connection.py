import os
import oracledb
from flask import Flask, jsonify, request

app = Flask(_name_)

# Database configuration
dsn = os.getenv('DB_DSN', oracledb.makedsn("localhost", 1521, service_name="XE"))
db_user = os.getenv('DB_USER', 'system')
db_password = os.getenv('DB_PASSWORD', 'dazai')

# Create database connection
def create_connection():
    try:
        connection = oracledb.connect(user=db_user, password=db_password, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        print(f"Error connecting to Oracle DB: {error_obj.message}")
        return None

# API to fetch newsfeed for a user
@app.route('/api/newsfeed/<int:user_id>', methods=['GET'])
def get_newsfeed(user_id):
    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500
        
        cursor = connection.cursor()
        cursor.callproc("display_newsfeed", [user_id])

        # Collect DBMS_OUTPUT content
        output = []
        while True:
            line = cursor.getimplicitresults()
            if not line:
                break
            output.append(line[0])
        
        cursor.close()
        connection.close()

        return jsonify({"newsfeed": output}), 200
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500

# API to add a post
@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    user_id = data.get('user_id')
    content = data.get('content')

    if not user_id or not content:
        return jsonify({"error": "User ID and content are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.callproc("add_post", [user_id, content])
        connection.commit()

        return jsonify({"message": "Post added successfully"}), 201
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# API to send a friend request
@app.route('/api/friend-request', methods=['POST'])
def send_friend_request():
    data = request.get_json()
    user_id1 = data.get('user_id1')
    user_id2 = data.get('user_id2')

    if not user_id1 or not user_id2:
        return jsonify({"error": "Both user IDs are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.callproc("send_friend_request", [user_id1, user_id2])
        connection.commit()

        return jsonify({"message": "Friend request sent successfully"}), 201
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# API to accept a friend request
@app.route('/api/accept-friend-request', methods=['POST'])
def accept_friend_request():
    data = request.get_json()
    user_id1 = data.get('user_id1')
    user_id2 = data.get('user_id2')

    if not user_id1 or not user_id2:
        return jsonify({"error": "Both user IDs are required"}), 400

    try:
        connection = create_connection()
        if connection is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = connection.cursor()
        cursor.callproc("accept_friend_request", [user_id1, user_id2])
        connection.commit()

        return jsonify({"message": "Friend request accepted successfully"}), 200
    except oracledb.DatabaseError as e:
        error_obj, = e.args
        return jsonify({"error": error_obj.message}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if _name_ == '_main_':
    app.run(debug=True)