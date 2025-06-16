import gspread
from oauth2client.service_account import ServiceAccountCredentials
from plyer import notification
import tkinter as tk
from tkinter import messagebox
import os
import sys

def get_json_key_path():
    key_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not key_path or not os.path.exists(key_path):
        raise FileNotFoundError(
            "Environment variable 'GOOGLE_SERVICE_ACCOUNT_JSON' is not set "
            "or points to a non-existent file."
        )
    return key_path

google_api_scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

credentials_path = get_json_key_path()
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, google_api_scope)
google_client = gspread.authorize(credentials)
task_sheet = google_client.open("Tester").worksheet("Muzammil")

previous_task_list = []

app_window = tk.Tk()
app_window.title("My Task List")
app_window.geometry("450x350")
app_window.resizable(False, False)

task_display = tk.Listbox(app_window, width=60, height=15, font=("Segoe UI", 10))
task_display.pack(pady=10)

def update_task_display(tasks):
    task_display.delete(0, tk.END)
    for task_row in tasks:
        task_text = " | ".join(task_row)
        task_display.insert(tk.END, task_text)

def fetch_and_notify_tasks():
    global previous_task_list
    try:
        current_tasks = task_sheet.get_all_values()
        new_tasks = [task for task in current_tasks if task not in previous_task_list]

        if new_tasks:
            for task in new_tasks:
                notification.notify(
                    title="New Task",
                    message=" | ".join(task),
                    timeout=5
                )
        else:
            messagebox.showinfo("No New Tasks", "No new tasks found.")

        previous_task_list = current_tasks
        update_task_display(current_tasks)
    except Exception as error:
        messagebox.showerror("Error", f"Could not fetch tasks:\n{error}")

refresh_button = tk.Button(
    app_window,
    text="Refresh Tasks",
    command=fetch_and_notify_tasks,
    font=("Segoe UI", 10, "bold")
)
refresh_button.pack(pady=10)

fetch_and_notify_tasks()
app_window.mainloop()
