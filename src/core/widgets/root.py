from tkinter import Tk
from tkinter.ttk import Style

from main import Main


class Root(Tk):
    def __init__(self, title: str):
        super().__init__()

        self._configure_root(title)
        self._setup_theme()

        self.main = Main(self)

    def __repr__(self):
        return "Root"

    def _configure_root(self, title: str):
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self._delete_window)
        self.geometry("800x800")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _delete_window(self):
        self.quit()
        self.destroy()

    def _setup_theme(self):
        self.theme = Style()
        self.theme.theme_use("alt")

        self._setup_theme_base_colors()
        self._setup_theme_button()
        self._setup_theme_heading()

    def _setup_theme_base_colors(self):
        self.theme.configure("Chrome.TFrame", foreground="#fff", background="#000")
        self.theme.configure("Chrome.TLabel", foreground="#fff", background="#000")
        self.theme.configure("Chrome.TEntry", foreground="#fff", fieldbackground="#222", insertcolor='#fff')
        self.theme.configure("Chrome.Treeview", foreground="#fff", background="#000", fieldbackground="#000")

    def _setup_theme_button(self):
        btn_fg = [('!active', '#fff'), ('pressed', '#bbb'), ('active', '#ddd')]
        btn_bg = [('!active', '#000'), ('pressed', '#444'), ('active', '#222')]
        self.theme.map("Chrome.TButton", foreground=btn_fg, background=btn_bg)

    def _setup_theme_heading(self):
        tree_head_fg = [('!active', '#ddd'), ('pressed', '#bbb'), ('active', '#fff')]
        tree_head_bg = [('!active', '#222'), ('pressed', '#444'), ('active', '#000')]
        self.theme.map("Chrome.Treeview.Heading", foreground=tree_head_fg, background=tree_head_bg)
