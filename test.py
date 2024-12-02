import tkinter as tk
from db_access import Base, engine
from components.create_modal import create_modal
from views.PageManager import PageManager
from views.employee import EmployeeManager
from views.department import DepartmentManager

# テーブル作成
Base.metadata.create_all(engine)

# メインウィンドウ
root = tk.Tk()
root.title("管理システム")
root.geometry("900x600")

sidebar = tk.Frame(root, bg="#eee", width=200)
sidebar.pack(side="left", fill="y")

content_frame = tk.Frame(root, bg="#fff")
content_frame.pack(side="right", fill="both", expand=True)

header_label = tk.Label(content_frame, text="", bg="#fff", font=("Arial", 16), anchor="w")
header_label.pack(side="top", fill="x", padx=10, pady=5)

# 共通の初期設定を行う
PageManager.initialize(root, content_frame, header_label)

# サイドバーにマスター項目を追加
master_label = tk.Label(sidebar, text="マスター", bg="#ddd", font=("Arial", 14, "bold"), anchor="w", cursor="hand2")
master_label.pack(fill="x", pady=5)

sub_menu_frame = tk.Frame(sidebar, bg="#eee")

employee_label = tk.Label(sub_menu_frame, text="従業員", bg="#eee", font=("Arial", 12), anchor="w", cursor="hand2")
employee_label.pack(fill="x", pady=5)
employee_manager = EmployeeManager()
employee_label.bind("<Button-1>", lambda event: employee_manager.setup_page())

department_label = tk.Label(sub_menu_frame, text="部署", bg="#eee", font=("Arial", 12), anchor="w", cursor="hand2")
department_label.pack(fill="x", pady=5)
department_manager = DepartmentManager()
department_label.bind("<Button-1>", lambda event: department_manager.setup_page())

def toggle_sub_menu():
    if sub_menu_frame.winfo_viewable():
        sub_menu_frame.pack_forget()
    else:
        sub_menu_frame.pack(fill="x")

master_label.bind("<Button-1>", lambda event: toggle_sub_menu())

# 初期画面
employee_manager.setup_page()

root.mainloop()
