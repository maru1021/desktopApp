import tkinter as tk
from tkinter import ttk

def create_modal(root, title, fields, validation_rules=None, on_confirm=None):
    modal = tk.Toplevel(root)
    modal.title(title)
    modal.geometry("300x300")
    modal.transient(root)
    modal.grab_set()

    entries = {}

    for field, default_value in fields.items():
        tk.Label(modal, text=f"{field}:").pack(pady=5)

        # セレクトボックス（リストの場合）
        if isinstance(default_value, list):
            combo = ttk.Combobox(modal, values=default_value, state="readonly")
            combo.set(default_value[0] if default_value else "")
            combo.pack(pady=5, fill="x", padx=10)
            entries[field] = combo
        else:
            entry = tk.Entry(modal)
            entry.insert(0, default_value)
            entry.pack(pady=5, fill="x", padx=10)
            entries[field] = entry

    # バリデーション、クリック時のメソッドの実行
    def confirm_action():
        values = {field: entry.get() for field, entry in entries.items()}

        if validation_rules:
            for field, rules in validation_rules.items():
                for rule in rules:
                    if not rule(values.get(field), parent=modal):
                        return

        if on_confirm:
            on_confirm(values)
        modal.destroy()

    modal.bind("<Return>", lambda event: confirm_action())
    tk.Button(modal, text="保存", command=confirm_action).pack(pady=10)
