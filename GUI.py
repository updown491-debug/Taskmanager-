import tkinter as tk
from tkinter import messagebox
import backend123pro as backend

class Tadow:
    def __init__(self):
        self.current_user = None  # stores logged-in user_id

        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.title("TADOW - Task Manager")

        self.message = tk.Label(self.window, text="")
        self.message.pack()

        self.menu = tk.Label(self.window, text="Welcome! Ready to destroy your tasks?")
        self.menu.pack(padx=20, pady=20)

        self.loginbutt = tk.Button(self.window, text="Login", command=self.login_screen)
        self.loginbutt.pack(pady=10)

        self.choice = tk.Label(self.window, text="OR")
        self.choice.pack()

        self.signupbutt = tk.Button(self.window, text="Sign Up", command=self.signup_screen)
        self.signupbutt.pack()

        self.window.mainloop()

    # ---------------- LOGIN ----------------
    def login_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Enter Username").pack()
        self.us_name = tk.Entry(self.window)
        self.us_name.pack()

        tk.Label(self.window, text="Enter Password").pack()
        self.password = tk.Entry(self.window, show="*")
        self.password.pack()

        tk.Button(self.window, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.us_name.get()
        password = self.password.get()
        user_id = backend.login_user(username, password)
        if user_id:
            self.current_user = user_id
            messagebox.showinfo("Login", "✅ Logged in successfully!")
            self.dashboard()
        else:
            messagebox.showerror("Login", "❌ Wrong username or password!")

    # ---------------- SIGNUP ----------------
    def signup_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Choose Username").pack()
        self.us_name = tk.Entry(self.window)
        self.us_name.pack()

        tk.Label(self.window, text="Choose Password").pack()
        self.password = tk.Entry(self.window, show="*")
        self.password.pack()

        tk.Button(self.window, text="Create Account", command=self.signup).pack(pady=10)

    def signup(self):
        username = self.us_name.get()
        password = self.password.get()
        backend.create_user(username, password)
        messagebox.showinfo("Signup", "✅ Account created successfully!")
        self.main_menu()

    # ---------------- DASHBOARD ----------------
    def dashboard(self):
        self.clear_window()
        tk.Label(self.window, text="Task Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self.window, text="➕ Add Task", command=self.add_task_screen).pack(pady=5)
        tk.Button(self.window, text="📋 Display Tasks", command=self.show_tasks).pack(pady=5)
        tk.Button(self.window, text="✅ Update Task", command=self.update_task_screen).pack(pady=5)
        tk.Button(self.window, text="🗑️ Delete Task", command=self.delete_task_screen).pack(pady=5)
        tk.Button(self.window, text="📊 Show Progress", command=self.show_progress).pack(pady=5)
        tk.Button(self.window, text="🚪 Logout", command=self.main_menu).pack(pady=20)

    # ---------------- ADD TASK ----------------
    def add_task_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Task Title").pack()
        self.task_title = tk.Entry(self.window)
        self.task_title.pack()

        tk.Label(self.window, text="Priority (High/Medium/Low)").pack()
        self.task_priority = tk.Entry(self.window)
        self.task_priority.pack()

        tk.Label(self.window, text="Deadline (YYYY-MM-DD)").pack()
        self.task_deadline = tk.Entry(self.window)
        self.task_deadline.pack()

        tk.Button(self.window, text="Add Task", command=self.add_task).pack(pady=10)

    def add_task(self):
        title = self.task_title.get()
        priority = self.task_priority.get()
        deadline = self.task_deadline.get()
        backend.add_task(self.current_user, title, priority, deadline)
        messagebox.showinfo("Task", "✅ Task added successfully!")
        self.dashboard()

    # ---------------- DISPLAY TASKS ----------------
    def show_tasks(self):
        tasks = backend.display_tasks(self.current_user)
        if not tasks:
            messagebox.showinfo("Tasks", "No tasks found.")
        else:
            text = ""
            for t in tasks:
                text += f"ID: {t[0]} | {t[1]} | {t[2]} | {t[3]} | {t[4]} | Coins: {t[5]}\n"
            messagebox.showinfo("Tasks", text)

    # ---------------- UPDATE TASK ----------------
    def update_task_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Enter Task ID to Update").pack()
        self.update_id = tk.Entry(self.window)
        self.update_id.pack()

        tk.Label(self.window, text="New Status (Pending/Completed)").pack()
        self.new_status = tk.Entry(self.window)
        self.new_status.pack()

        tk.Button(self.window, text="Update Task", command=self.update_task).pack(pady=10)

    def update_task(self):
        task_id = int(self.update_id.get())
        status = self.new_status.get()
        backend.update_task_status(task_id, status)
        messagebox.showinfo("Update", "✅ Task updated successfully!")
        self.dashboard()

    # ---------------- DELETE TASK ----------------
    def delete_task_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Enter Task ID to Delete").pack()
        self.delete_id = tk.Entry(self.window)
        self.delete_id.pack()

        tk.Button(self.window, text="Delete Task", command=self.delete_task).pack(pady=10)

    def delete_task(self):
        task_id = int(self.delete_id.get())
        backend.delete_task(task_id)
        messagebox.showinfo("Delete", "🗑️ Task deleted successfully!")
        self.dashboard()

    # ---------------- SHOW PROGRESS ----------------
    def show_progress(self):
        total, completed, coins = backend.show_progress(self.current_user)
        messagebox.showinfo("Progress", f"📊 Total Tasks: {total}\n✅ Completed: {completed}\n💰 Coins: {coins}")

    # ---------------- HELPERS ----------------
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.window.destroy()
        Tadow()


# Run the App
App = Tadow()
