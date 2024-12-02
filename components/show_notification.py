import tkinter as tk

# 通知を表示
def show_notification(root, message):
    notification = tk.Toplevel(root)
    notification.overrideredirect(True)
    notification.geometry(f"200x50+{root.winfo_screenwidth() - 220}+50")
    tk.Label(notification, text=message, bg="green", fg="white", font=("Arial", 12)).pack(expand=True, fill="both")
    root.after(2000, notification.destroy)