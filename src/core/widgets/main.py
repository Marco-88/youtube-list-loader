import os
from tkinter import Tk, filedialog, IntVar
from tkinter.ttk import Frame, Button, Style, Checkbutton, Label
import threading

from .input import Input
from .progressbar import Progressbar
from .table import Table
from ..utils.table_manager import TableManager


class Main(Frame):
    def __init__(self, root: Tk, **kw):
        super().__init__(root, **kw)

        self._configure_frame()
        self._set_widgets()
        self._set_commands()

    def __repr__(self):
        return "Main"

    def _add(self):
        url = self.input_url.var.get()
        directory = self.input_directory.var.get()

        if url.startswith('https://www.youtube.'):
            self.manager.add(url, directory, self.progressbar, self.only_audio.get() > 0)
        else:
            self.show_info("Works only with valid youtube URLs (https://www.youtube.)", 2000, 0)

    def _choose(self):
        directory = filedialog.askdirectory()
        self.input_directory.var.set(directory)

    def _configure_frame(self):
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        style = Style()
        style.configure("Chrome.TFrame", foreground="#fff", background="#000")
        self.configure(style="Chrome.TFrame")

        self.grid(row=0, column=0, sticky='nesw', columnspan=5)

    def _set_widgets(self):
        self._set_inputs()
        self._set_download_btn()
        self._set_clear_btn()
        self._set_checkbox_only_audio()
        self._set_info_box()

        self.progressbar = Progressbar(self)

        self.table = Table(self)
        self.manager = TableManager(self.table)

    def _set_inputs(self):
        self.input_url = Input(self, 0, 'URL', 'Add')
        self.input_directory = Input(self, 1, 'Directory', 'Choose')
        self.input_directory.var.set(os.getcwd())  # 'C:/Users/User/Desktop/Media'

    def _set_download_btn(self):
        self.button_download = Button(self, text='Download')
        self.button_download.grid(row=3, column=0, columnspan=1, sticky='nesw')
        self.button_download.configure(style="Chrome.TButton")

    def _set_clear_btn(self):
        self.button_clear = Button(self, text='Clear')
        self.button_clear.grid(row=3, column=1, columnspan=1, sticky='nesw')
        self.button_clear.configure(style="Chrome.TButton")

    def _set_checkbox_only_audio(self):
        style = Style()
        style.configure("TCheckbutton", background="black", foreground="green")
        self.only_audio = IntVar()
        self.only_audio.set(1)
        self.checkbox_only_audio = Checkbutton(self, text="Only Audio", style="TCheckbutton", variable=self.only_audio)
        self.checkbox_only_audio.grid(row=0, column=1)

    def _set_info_box(self):
        style = Style()
        style.configure("TLabel", background="black", foreground="red")
        self.info_box_label = Label(self, style="TLabel")

    def show_info(self, text: str, ms: int, row: int = 4):
        self.info_box_label['text'] = text
        self.info_box_label.grid(row=row, column=0, columnspan=5)
        self.after(ms, self.info_box_label.grid_remove)

    def _set_commands(self):
        self.input_url.button['command'] = lambda: threading.Thread(target=self._add, daemon=True).start()
        self.input_directory.button['command'] = self._choose
        self.button_download['command'] = self.manager.download
        self.button_clear['command'] = self.manager.clear_table
