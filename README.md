# Lawn Service Manager

A desktop-based store and service management system built with Python, SQLite, and PySide6.

Designed for service businesses to manage stores, recurring services, service history, pricing, and image records through a graphical interface.

---

# Features:

* Store management system
* Add/edit/remove stores
* Track active and inactive locations
* Service scheduling and records
* Service history logging
* Attach and preview images for completed work
* SQLite database backend
* Data export system
* Database backup and restore support
* Standalone Windows executable support
* Dark themed UI built with PySide6

---

# Preview:

**Main Window**

**Expanded Store View**

**Image Viewer**

---

# Technology Used:

* Python 3
* PySide6
* SQLite3
* Object-Oriented Programming
* Custom UI component system

---

# Project Structure

    Store-Management-System/
    ├── scripts/
    │   ├── database.py
    │   ├── utils.py
    │   ├── in_out_put.py
    │   └── installer.py
    │
    ├── ui/
    │   ├── engine.py
    │   ├── main_window.py
    │   ├── store_object.py
    │   ├── service_object.py
    │   ├── service_record_object.py
    │   ├── service_history_object.py
    │   ├── export_prompt.py
    │   ├── image_prompt.py
    │   └── image_object.py
    │
    ├── main.py
    ├── requirements.txt
    └── README.md

---

# Database:

The application uses SQLite with relational table structures for:

* Stores
* Services
* Service Records
* Service History
* Image Storage

> Foreign key relationships and cascading deletes are supported.

---

# Safety features:

The application supports:

* Full database backups
* Database restoration
* Exporting data tables
* Importing existing databases

---

# Installation Steps:

**Method 1: (Python)**
1) Clone Repository
```bash
git clone https://github.com/srh05624/Store-Management-System.git
cd Store-Management-System
```

2) Install Dependencies (Generated via pipreqs)

```bash
pip install requirements.txt
```

3) Run Application

```bash
python main.py
```

**Method 2: (Standalone Executable)**
The project is packaged into a standalone Windows executable using: pyinstaller

To run the project, use the executable found in the dist folder.

> Current packaged size is approximately: 50MB

---

# Project Goals:

This project was created to:

* Improve workflow management for businesses with many services across stores
* Practice GUI application development
* Learn database architecture and management
* Build a real-world desktop application with Python

---

# Planned improvements:

* Calendar/scheduling system
* Better responsive layouts
* Automatic recurring service generation
* Multi-user support
* Cloud backup support
* Advanced filtering/search
* PDF/Excel export support

---

# Author:

> *Samuel Rodriguez*
