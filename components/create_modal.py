import tkinter as tk
from tkinter import ttk

def create_modal(root, title, fields, validation_rules=None, on_confirm=None):
    """
    モーダルウィンドウを作成

    :param root: モーダルの親ウィンドウ
    :param title: モーダルのタイトル
    :param fields: フィールドとデフォルト値の辞書
    :param validation_rules: バリデーションルールの辞書
    :param on_confirm: 確定ボタンが押された際のコールバック関数
    """
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

    def confirm_action():
        """入力データをバリデーションし、成功時にコールバックを実行"""
        values = {field: entry.get() for field, entry in entries.items()}

        # バリデーションを適用
        if validation_rules:
            for field, rules in validation_rules.items():
                for rule in rules:
                    if not rule(values.get(field), parent=modal):
                        return  # バリデーションエラー時は処理を中断

        if on_confirm:
            on_confirm(values)
        modal.destroy()

    modal.bind("<Return>", lambda event: confirm_action())
    tk.Button(modal, text="保存", command=confirm_action).pack(pady=10)
