import re
from tkinter import ttk, messagebox
import tkinter as tk
from db_access import session
from models.department import Department

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
def create_modal(root, title, fields, department_dropdown=False, on_confirm=None):
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