# Tour De Restaurant - Inventory & Ordering System

**Course:** Fall 2026 - SDEV265 - System Software Analysis

## Team Members
- Marko Gvero
- Ashley Lawrence
- Cesar Vasquez
- Marvin Lamothe

## Summary & Technologies
Tour De Restaurant is a web application built to manage daily restaurant operations including ingredient inventory tracking and customer ordering. Customers can view the menu and place their orders, while kitchen and restaurant staff can track ingredient stock levels and manage inventory in real time.

This project is built using:
- **Python** & **Django** - backend logic
- **SQLite** - database for data storage
- **HTML5 & CSS3** - user interface
- **GitHub** - version control

## Features

### Staff & Management
- Log in as staff to view/add ingredient inventory levels.
- Track stock quantities to know when ingredients need to be restocked.
- Access staff-only views restricted by user permissions.

### Customers
- Browse menu items and place restaurant orders.
- Simple, straightforward interface for selecting items and checking out.

## Setup & How to Run

### To go to live website visit: https://markogvero.pythonanywhere.com/

### To run program locally:

1. **Clone the repository:**
```bash
git clone <repository-url>
cd SDEV265-Group-Project---Team-Tour-De-Restaurant
```

2. **Set up a virtual environment:**
```bash
python -m venv .venv
```

3. **Activate the virtual environment:**
    - **Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
    - **Mac/Linux:**
    ```bash
    source venv/bin/activate
    ```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Apply database migrations:**
```bash
python manage.py migrate
```

6. **Log in or Register:**
    - **Staff/Admin Login:** Username: "admin", Password: "Password1234"
    - **Customer:** Click **Register** on the navigation bar to create a new account, then log in.

7. **Start the development server:**
```bash
python manage.py runserver
```

8. Open your web browser and go to `http://127.0.0.1:8000/`.