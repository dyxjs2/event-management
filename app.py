from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for sessions

DATA_FILE = "data.json"

# ---------- Hardcoded credentials (Member 5) ----------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"


# ---------- Helper functions ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(events):
    with open(DATA_FILE, "w") as f:
        json.dump(events, f, indent=2)


def get_next_id(events):
    if not events:
        return 1
    return max(e["id"] for e in events) + 1


# ---------- Member 1: Homepage & Listing ----------
@app.route("/")
def index():
    events = load_data()
    # Sort by date ascending
    events_sorted = sorted(events, key=lambda e: e.get("date", ""))
    return render_template("index.html", events=events_sorted)


# ---------- Member 2: Event Creation ----------
@app.route("/create", methods=["GET", "POST"])
def create():
    if not session.get("logged_in"):
        flash("You must be logged in to create events.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        date = request.form.get("date", "").strip()
        description = request.form.get("description", "").strip()

        if not name or not date or not description:
            flash("All fields are required.", "error")
            return render_template("create.html")

        events = load_data()
        new_event = {
            "id": get_next_id(events),
            "name": name,
            "date": date,
            "description": description,
            "registrations": []
        }
        events.append(new_event)
        save_data(events)
        flash(f'Event "{name}" created successfully!', "success")
        return redirect(url_for("index"))

    return render_template("create.html")


# ---------- Member 3: Event Registration ----------
@app.route("/register/<int:event_id>", methods=["GET", "POST"])
def register(event_id):
    events = load_data()
    event = next((e for e in events if e["id"] == event_id), None)

    if not event:
        flash("Event not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        user_name = request.form.get("user_name", "").strip()
        if not user_name:
            flash("Please enter your name.", "error")
            return render_template("register.html", event=event)

        if user_name in event["registrations"]:
            flash(f'"{user_name}" is already registered for this event.', "warning")
        else:
            event["registrations"].append(user_name)
            save_data(events)
            flash(f'"{user_name}" successfully registered for "{event["name"]}"!', "success")
        return redirect(url_for("index"))

    return render_template("register.html", event=event)


# ---------- Member 4: Search / Filter ----------
@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    events = load_data()

    if query:
        results = [e for e in events if query in e["name"].lower()]
    else:
        results = events

    return render_template("search.html", events=results, query=query)


# ---------- Member 5: User Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


# ---------- Member 6: Admin View ----------
@app.route("/admin")
def admin():
    if not session.get("logged_in"):
        flash("Admin access requires login.", "warning")
        return redirect(url_for("login"))

    events = load_data()
    total_events = len(events)
    total_registrations = sum(len(e["registrations"]) for e in events)
    return render_template("admin.html", events=events,
                           total_events=total_events,
                           total_registrations=total_registrations)


if __name__ == "__main__":
    app.run(debug=True)