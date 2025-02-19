import logging
import sqlite3
from flask import Flask, request, jsonify

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

print("✅ Flask app is starting...")  

app = Flask(__name__)

# ✅ Log every incoming request
@app.before_request
def log_request_info():
    print(f"📥 Incoming Request: {request.method} {request.path}")


# ✅ Health Check Route (To Test if Flask is Running)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# ✅ Initialize database
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT,
                address TEXT,
                travel_time TEXT,
                roster TEXT
            )
        """)
    conn.close()

# ✅ Route to check available routes (Debugging)
@app.route("/debug-routes", methods=["GET"])
def debug_routes():
    return jsonify({"routes": [str(rule) for rule in app.url_map.iter_rules()]}), 200

# ✅ Signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, password, address, travel_time, roster)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data['name'], data['email'], data['password'], data['address'], data['travel_time'], data['roster']))
            conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered."}), 400

# ✅ Roster Matching Route
@app.route('/match', methods=['GET'])
def match_users():
    roster = request.args.get('roster')
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, email, address, roster
            FROM users
            WHERE roster = ?
        """, (roster,))
        matches = cursor.fetchall()
    return jsonify({"matches": matches}), 200

# ✅ Ensure Flask is properly bound for production
if __name__ == "__main__":
    print("✅ Flask is now running on port 5000 and listening for requests.")
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(f"🚨 Flask failed to start: {e}")
