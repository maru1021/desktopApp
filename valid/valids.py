import re
from tkinter import messagebox

def validate_required(value, parent=None):
    # 必須項目のバリデーション
    if not value.strip():
        messagebox.showwarning("入力エラー", "このフィールドは必須です", parent=parent)
        return False
    return True

def validate_email(value, parent=None):
    # メールアドレス形式のバリデーション
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        messagebox.showwarning("入力エラー", "有効なメールアドレスを入力してください", parent=parent)
        return False
    return True

def validate_length(value, max_length, parent=None):
    # 文字数制限のバリデーション
    if len(value.strip()) > max_length:
        messagebox.showwarning("入力エラー", f"最大{max_length}文字までです", parent=parent)
        return False
    return True

def validate_custom(value, custom_rule, error_message, parent=None):
    # カスタムルールのバリデーション
    if not custom_rule(value):
        messagebox.showwarning("入力エラー", error_message, parent=parent)
        return False
    return True
