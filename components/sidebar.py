import tkinter as tk

class Sidebar:
    def __init__(self, root, managers):
        self.root = root
        self.managers = managers
        self.sidebar_frame = tk.Frame(root, bg="#eee", width=200)
        self.sidebar_frame.pack(side="left", fill="y")

        self._create_master_menu()

    def _create_master_menu(self):
        master_label = tk.Label(
            self.sidebar_frame, text="マスター", bg="#ddd",
            font=("Arial", 14, "bold"), anchor="w"
        )
        master_label.pack(fill="x", pady=5)

        self.sub_menu_frame = tk.Frame(self.sidebar_frame, bg="#eee")

        for manager in self.managers:
            label = tk.Label(
                self.sub_menu_frame, text=manager.title,
                bg="#eee", font=("Arial", 12), anchor="w"
            )
            label.pack(fill="x", pady=5)
            label.bind("<Button-1>", lambda event, m=manager: m.setup_page())

        master_label.bind("<Button-1>", lambda event: self.toggle_sub_menu())

    # サブメニューの表示/非表示を切り替え
    def toggle_sub_menu(self):
        if self.sub_menu_frame.winfo_viewable():
            self.sub_menu_frame.pack_forget()
        else:
            self.sub_menu_frame.pack(fill="x")
