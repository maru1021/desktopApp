import os
import tkinter as tk
from tkinter import ttk, messagebox
import re
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# データベースファイルのセットアップ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "organization.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, connect_args={"check_same_thread": False})

# SQLAlchemyセットアップ
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# モデル定義
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    department = relationship("Department", back_populates="employees")

    __table_args__ = (UniqueConstraint("email", name="unique_email_constraint"),)

# テーブル作成
Base.metadata.create_all(engine)

# バリデーション関数
def validate_inputs(name, email=None, parent=None):
    if not name:
        messagebox.showwarning("入力エラー", "名前を入力してください", parent=parent)
        return False
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showwarning("入力エラー", "有効なメールアドレスを入力してください", parent=parent)
        return False
    return True

# モーダル生成（共通）
def create_modal(title, fields, department_dropdown=False, on_confirm=None):
    modal = tk.Toplevel(root)
    modal.title(title)
    modal.geometry("300x300")
    modal.transient(root)
    modal.grab_set()

    entries = {}
    for field, default_value in fields.items():
        tk.Label(modal, text=f"{field}:").pack(pady=5)
        if department_dropdown and field == "部署":
            # 部署選択用ドロップダウンを作成
            departments = [d.name for d in session.query(Department).all()]
            combo = ttk.Combobox(modal, values=departments, state="readonly")
            combo.set(default_value)
            combo.pack(pady=5, fill="x", padx=10)
            entries[field] = combo
        else:
            entry = tk.Entry(modal)
            entry.insert(0, default_value)
            entry.pack(pady=5, fill="x", padx=10)
            entries[field] = entry

    def confirm_action():
        values = {field: entry.get() for field, entry in entries.items()}
        if all(validate_inputs(values.get("名前"), values.get("メールアドレス"), parent=modal) for field in fields):
            if on_confirm:
                on_confirm(values)
            modal.destroy()

    modal.bind("<Return>", lambda event: confirm_action())
    tk.Button(modal, text="保存", command=confirm_action).pack(pady=10)

# 通知を表示
def show_notification(message):
    notification = tk.Toplevel(root)
    notification.overrideredirect(True)
    notification.geometry(f"200x50+{root.winfo_screenwidth() - 220}+50")
    tk.Label(notification, text=message, bg="green", fg="white", font=("Arial", 12)).pack(expand=True, fill="both")
    root.after(2000, notification.destroy)

# 管理共通関数
def setup_page(title, columns, refresh_function, register_function, edit_function, delete_function):
    header_label.config(text=title)

    def show_context_menu(event):
        selected_item = tree.selection()
        if not selected_item:
            return

        def edit_item():
            edit_function(selected_item)

        def delete_item():
            item_id = tree.item(selected_item)["values"][0]
            delete_function(item_id)

        context_menu = tk.Menu(root, tearoff=0)
        context_menu.add_command(label="編集", command=edit_item)
        context_menu.add_command(label="削除", command=delete_item)
        context_menu.post(event.x_root, event.y_root)

    for widget in content_frame.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(content_frame, bg="#fff")
    top_frame.pack(side="top", fill="x", pady=5)

    search_entry = tk.Entry(top_frame)
    search_entry.pack(side="left", padx=10)
    search_entry.bind("<KeyRelease>", lambda event: refresh_function(search_entry.get(), tree))

    register_button = tk.Button(top_frame, text="登録", command=register_function)
    register_button.pack(side="right", padx=10)

    tree = ttk.Treeview(content_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150 if col != "ID" else 50)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    tree.update_idletasks()  # 即座に描画を反映

    tree.bind("<Button-3>", show_context_menu)
    refresh_function("", tree)

    return search_entry, tree

# 従業員管理
def manage_employees():
    def refresh_employees(search_text, tree):
        for row in tree.get_children():
            tree.delete(row)
        query = session.query(Employee).join(Department).filter(
            (Employee.name.like(f"%{search_text}%")) |
            (Employee.email.like(f"%{search_text}%")) |
            (Department.name.like(f"%{search_text}%"))
        )
        for emp in query.all():
            tree.insert("", "end", values=(emp.id, emp.name, emp.email, emp.department.name if emp.department else ""))

    def register_employee(values):
        department_name = values.get("部署")
        department = session.query(Department).filter_by(name=department_name).first()
        try:
            new_employee = Employee(name=values["名前"], email=values["メールアドレス"], department=department)
            session.add(new_employee)
            session.commit()
            refresh_employees("", tree)
            show_notification("登録されました")
        except Exception as e:
            session.rollback()  # セッションをリセット
            messagebox.showwarning("エラー", "メールアドレスが重複しています", parent=root)


    def edit_employee(selected_item):
        employee_id, name, email, department_name = tree.item(selected_item)["values"]

        def update_employee(values):
            try:
                emp = session.query(Employee).filter_by(id=employee_id).first()
                emp.name = values["名前"]
                emp.email = values["メールアドレス"]
                emp.department = session.query(Department).filter_by(name=values.get("部署")).first()
                session.commit()
                refresh_employees("", tree)
                show_notification("更新されました")
            except Exception as e:
                session.rollback()  # セッションをリセット
                messagebox.showwarning("エラー", "メールアドレスが重複しています", parent=root)

        create_modal("従業員編集", fields={"名前": name, "メールアドレス": email, "部署": department_name}, 
                    department_dropdown=True, on_confirm=update_employee)

    def delete_employee(employee_id):
        if messagebox.askyesno("確認", "この従業員を削除しますか？", parent=root):
            session.query(Employee).filter_by(id=employee_id).delete()
            session.commit()
            refresh_employees("", tree)
            show_notification("削除されました")

    employee_columns = ("ID", "名前", "メールアドレス", "部署")
    _, tree = setup_page("従業員管理", employee_columns, refresh_employees, 
                         lambda: create_modal("従業員登録", {"名前": "", "メールアドレス": "", "部署": ""}, 
                                              department_dropdown=True, on_confirm=register_employee), 
                         edit_employee, delete_employee)

# 部署管理
def manage_departments():
    def refresh_departments(search_text, tree):
        for row in tree.get_children():
            tree.delete(row)
        query = session.query(Department).filter(Department.name.like(f"%{search_text}%"))
        for dept in query.all():
            tree.insert("", "end", values=(dept.id, dept.name))

    def register_department(values):
        try:
            new_department = Department(name=values["名前"])
            session.add(new_department)
            session.commit()
            refresh_departments("", tree)
            show_notification("登録されました")
        except Exception:
            messagebox.showwarning("エラー", "部署名が重複しています", parent=root)

    def edit_department(selected_item):
        department_id, name = tree.item(selected_item)["values"]

        def update_department(values):
            try:
                dept = session.query(Department).filter_by(id=department_id).first()
                dept.name = values["名前"]
                session.commit()
                refresh_departments("", tree)
                show_notification("更新されました")
            except Exception:
                messagebox.showwarning("エラー", "更新に失敗しました", parent=root)

        create_modal("部署編集", fields={"名前": name}, on_confirm=update_department)

    def delete_department(department_id):
        # 紐づいている従業員がいるかをチェック
        linked_employees = session.query(Employee).filter_by(department_id=department_id).count()
        if linked_employees > 0:
            # メッセージを表示して削除をキャンセル
            messagebox.showwarning("削除エラー", "この部署には従業員が紐づいているため削除できません", parent=root)
            return

        if messagebox.askyesno("確認", "この部署を削除しますか？", parent=root):
            session.query(Department).filter_by(id=department_id).delete()
            session.commit()
            refresh_departments("", tree)
            show_notification("部署が削除されました")


    department_columns = ("ID", "名前")
    _, tree = setup_page("部署管理", department_columns, refresh_departments, 
                         lambda: create_modal("部署登録", {"名前": ""}, on_confirm=register_department), 
                         edit_department, delete_department)

# メインウィンドウ
root = tk.Tk()
root.title("管理システム")
root.geometry("900x600")

# サイドバー
sidebar = tk.Frame(root, bg="#eee", width=150)
sidebar.pack(side="left", fill="y")

header_label = tk.Label(root, text="", bg="#fff", font=("Arial", 16), anchor="e")
header_label.pack(side="top", fill="x", padx=10, pady=5)

content_frame = tk.Frame(root, bg="#fff")
content_frame.pack(side="right", fill="both", expand=True)

employee_btn = tk.Button(sidebar, text="従業員", command=manage_employees)
employee_btn.pack(fill="x", pady=5)

department_btn = tk.Button(sidebar, text="部署", command=manage_departments)
department_btn.pack(fill="x", pady=5)

# 初期画面
manage_employees()

root.mainloop()
