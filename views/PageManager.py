import tkinter as tk
from tkinter import ttk

class PageManager:
    # 継承先クラス共通の初期設定
    @classmethod
    def initialize(cls, root, content_frame, header_label):
        cls.root = root
        cls.content_frame = content_frame
        cls.header_label = header_label

    def __init__(self):
        # サブクラスで定義するクラス変数
        self.title = getattr(self, "title", "管理画面")
        self.columns = getattr(self, "columns", ())

        self.tree = None
        self.search_entry = None
        self.register_button = None
        self.validation_rules = {}

    # ページのセットアップ
    def setup_page(self):
        self.header_label.config(text=self.title)

        # サイドバーで選択しているもの以外の要素を削除する
        for widget in self.content_frame.winfo_children():
            if widget != self.header_label:
                widget.destroy()

        top_frame = tk.Frame(self.content_frame, bg="#fff")
        top_frame.pack(side="top", fill="x", pady=5)

        # テーブル見出しの定義
        self.tree = ttk.Treeview(self.content_frame, columns=self.columns, show="headings")

        # 検索フォーム
        self.search_entry = tk.Entry(top_frame)
        self.search_entry.pack(side="left", padx=10)
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh(self.search_entry.get(), self.tree))

        # 登録ボタン
        self.register_button = tk.Button(top_frame, text="登録", command=self.show_register_modal)
        self.register_button.pack(side="right", padx=10)

        # テーブルの幅などの設定
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "ID" else 50)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # テーブルで右クリック時にコンテキストメニューを表示させる
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.refresh("", self.tree)

    # 右クリックメニューを表示
    def show_context_menu(self, event):
        # 右クリックされた行の識別子を取得
        selected_item = self.tree.selection()
        if not selected_item:
            return

        def edit_item():
            self.show_edit_modal(selected_item)

        def delete_item():
            item_id = self.tree.item(selected_item)["values"][0]
            self.delete(item_id)

        context_menu = tk.Menu(self.root)
        context_menu.add_command(label="編集", command=edit_item)
        context_menu.add_command(label="削除", command=delete_item)
        context_menu.post(event.x_root, event.y_root)

    # テーブルのデータの更新（サブクラスで実装）
    def refresh(self, search_text, tree):
        raise NotImplementedError

    # データの登録（サブクラスで実装）
    def register(self, values):
        raise NotImplementedError

    # データの編集（サブクラスで実装）
    def edit(self, selected_item):
        raise NotImplementedError

    # データの削除（サブクラスで実装）
    def delete(self, item_id):
        raise NotImplementedError

    # 登録用モーダルを表示（サブクラスで実装）
    def show_register_modal(self):
        raise NotImplementedError

    # 編集用モーダルを表示（サブクラスで実装）
    def show_edit_modal(self, selected_item):
        raise NotImplementedError