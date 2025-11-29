from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# ---------------- APP SETUP ----------------
app = Flask(__name__)

# ---------------- DATABASE SETUP ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hostel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- MODEL (TABLE STRUCTURE) ----------------
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    adhar = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10))
    family = db.Column(db.String(50))
    fee = db.Column(db.String(20))
    room = db.Column(db.String(50))
    checkin = db.Column(db.String(50))
    duration = db.Column(db.String(20))
    requests = db.Column(db.String(200))

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template("index.html")

# ---------------- BOOKING PAGE ----------------
@app.route("/booking", methods=["GET", "POST"])
def booking():
    success_message = None
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        adhar = request.form["adhar"]
        gender = request.form["gender"]
        family = request.form["family"]
        fee = request.form["fee"]
        room = request.form["room"]
        checkin = request.form["checkin"]
        duration = request.form["duration"]
        requests_text = request.form["requests"]

        # --- Save to SQLite (direct) ---
        conn = sqlite3.connect("hostel.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                adhar TEXT,
                gender TEXT,
                family TEXT,
                fee TEXT,
                room TEXT,
                checkin TEXT,
                duration TEXT,
                requests TEXT
            )
        """)
        cursor.execute("""
            INSERT INTO bookings (name, email, phone, adhar, gender, family, fee, room, checkin, duration, requests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, adhar, gender, family, fee, room, checkin, duration, requests_text))
        conn.commit()
        conn.close()

        success_message = f"✅ Thank you {name}! Your {room} booking has been submitted successfully."

    # Pass success_message to template for popup
    return render_template("booking.html", success_message=success_message)

# ---------------- OTHER PAGES ----------------
@app.route("/facilities")
def facilities():
    return render_template("facilities.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login")
def login():
    return render_template("login.html")

# ---------------- ADMIN PAGE ----------------
@app.route("/admin")
def admin():
    bookings = Booking.query.all()
    return render_template("admin.html", bookings=bookings)

# ---------------- AVAILABILITY CHECK ----------------
@app.route("/availability")
def availability():
    return render_template("availability.html")

@app.route("/check_availability", methods=["POST"])
def check_availability():
    room_type = request.form["room_type"]
    date = request.form["date"]

    conn = sqlite3.connect("hostel.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bookings WHERE room=? AND checkin=?", (room_type, date))
    booked = cursor.fetchone()[0]
    conn.clos
# ---------------- CREATE DATABASE ----------------
with app.app_context():
    db.create_all()

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user for testing
USER = {
    "email": "varshaseenu0426@gmail.com",
    "password": "12345"
}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == USER['email'] and password == USER['password']:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid email or password")
    return render_template('login.html')

@app.route('/home')
def home():
    return "<h1>Welcome, Student!</h1><p>Login Successful 🎉</p>"

if __name__ == '__main__':
    app.run(debug=True)
