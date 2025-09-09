# backend.py
import mysql.connector

# Function to connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="YOUR_PASSWORD_HERE",   
        database="tadow"
    )

# Function to initialize database & tables
def init_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Nikhil@123890"
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS tadow")
    cursor.execute("USE tadow")

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(50)
    )
    """)

    # Create tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        title VARCHAR(100),
        status VARCHAR(20) DEFAULT 'Pending',
        priority VARCHAR(10),
        deadline DATE,
        coins INT DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    db.commit()
    db.close()
    print("✅ Database and tables initialized successfully!")



# backend.py (continued)

# Signup
def create_user(username, password):
    db = get_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        print("✅ Account created successfully!")
    except mysql.connector.IntegrityError:
        print("⚠️ Username already exists!")
    db.close()

# Login
def login_user(username, password):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    db.close()
    if user:
        print("✅ Login successful!")
        return user[0]   # return user_id
    else:
        print("❌ Invalid username or password")
        return None






# backend.py (continued)

# Add Task
def add_task(user_id, title, priority, deadline):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tasks (user_id, title, priority, deadline) VALUES (%s, %s, %s, %s)",
                   (user_id, title, priority, deadline))
    db.commit()
    db.close()
    print("✅ Task added successfully!")

# Display Tasks
def display_tasks(user_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, status, priority, deadline, coins FROM tasks WHERE user_id=%s", (user_id,))
    rows = cursor.fetchall()
    db.close()
    return rows

# Update Task Status (mark completed & reward coins)
def update_task_status(task_id, new_status):
    db = get_connection()
    cursor = db.cursor()
    if new_status.lower() == "completed":
        cursor.execute("UPDATE tasks SET status=%s, coins=coins+5 WHERE id=%s", (new_status, task_id))
    else:
        cursor.execute("UPDATE tasks SET status=%s WHERE id=%s", (new_status, task_id))
    db.commit()
    db.close()
    print("✅ Task updated successfully!")

# Delete Task
def delete_task(task_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    db.commit()
    db.close()
    print("🗑️ Task deleted successfully!")

# Show Progress
def show_progress(user_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*), SUM(CASE WHEN status='Completed' THEN 1 ELSE 0 END), SUM(coins) FROM tasks WHERE user_id=%s", (user_id,))
    total, completed, coins = cursor.fetchone()
    db.close()
    return total, completed or 0, coins or 0
