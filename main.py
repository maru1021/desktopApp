import tkinter as tk
from db_access import Base, engine
from components.create_modal import create_modal
from views.PageManager import PageManager
from views.employee import EmployeeManager
from views.department import DepartmentManager
from components.sidebar import Sidebar

# テーブル作成
Base.metadata.create_all(engine)

# メインウィンドウ
root = tk.Tk()
root.title("管理システム")
root.geometry("900x600")

# メインの表示領域
content_frame = tk.Frame(root, bg="#fff")
content_frame.pack(side="right", fill="both", expand=True)

header_label = tk.Label(content_frame, text="", bg="#fff", font=("Arial", 16), anchor="w")
header_label.pack(side="top", fill="x", padx=10, pady=5)

# 共通の初期設定を行う
PageManager.initialize(root, content_frame, header_label)

# サイドバーを作成
employee_manager = EmployeeManager()
department_manager = DepartmentManager()

sidebar = Sidebar(root, [department_manager, employee_manager])

# 初期画面
employee_manager.setup_page()

root.mainloop()
