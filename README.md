# event-management
# ⚡ EventHub — Full-Stack Event Management Website

A simple, beginner-friendly event management web app built with **Python + Flask**. No database required — all data is stored in a `data.json` file.

---

## 📁 Project Structure

```
event_manager/
│
├── app.py                  # Flask backend (all routes & logic)
├── data.json               # JSON file used as the data store
└── templates/
    ├── base.html           # Shared layout (navbar, styles, flash messages)
    ├── index.html          # Homepage — lists all events
    ├── create.html         # Form to create a new event
    ├── register.html       # Form to register for an event
    ├── search.html         # Search/filter events by name
    ├── login.html          # Admin login page
    └── admin.html          # Admin dashboard with registration summary
```

---

## 🚀 Getting Started

### 1. Install Flask

```bash
pip install flask
```

### 2. Run the App

```bash
python app.py
```

### 3. Open in Browser

```
http://127.0.0.1:5000
```

---

## 🔐 Login Credentials

The login system uses hardcoded credentials (no database needed):

| Username | Password    |
|----------|-------------|
| `admin`  | `password123` |

You must be logged in to **create events** or access the **admin panel**.

---

## ✨ Features

| Member | Feature | Route |
|--------|---------|-------|
| **Member 1** | Homepage — view all upcoming events | `/` |
| **Member 2** | Create Event — add name, date, description | `/create` |
| **Member 3** | Register — add your name to an event | `/register/<id>` |
| **Member 4** | Search — filter events by name | `/search` |
| **Member 5** | Login/Logout — session-based auth | `/login`, `/logout` |
| **Member 6** | Admin View — event & registration summary | `/admin` |

---

## 🗃️ How Data is Stored

All events are stored in `data.json` as a list of objects. No SQL or database setup needed.

**Example entry:**
```json
{
  "id": 1,
  "name": "Tech Fest 2025",
  "date": "2025-08-15",
  "description": "Annual technology festival with workshops and talks.",
  "registrations": ["Alice", "Bob"]
}
```

The file is read and written automatically by the app. Three sample events are included to get you started.

---

## 🧱 Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** Plain HTML + CSS (no frameworks)
- **Data Storage:** JSON file (`data.json`)
- **Auth:** Flask sessions with hardcoded credentials

---

## 📝 Notes

- All pages share a common layout defined in `base.html` using Flask's Jinja2 template inheritance (`{% extends "base.html" %}`).
- Flash messages (success, error, warning) are handled globally in `base.html` and triggered from any route in `app.py`.
- The `secret_key` in `app.py` is required for sessions to work. Change it to something random before deploying.
