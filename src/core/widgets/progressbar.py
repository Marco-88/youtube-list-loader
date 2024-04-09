from tkinter import StringVar, HORIZONTAL
from tkinter.ttk import Label, Progressbar as PBar, Frame, Style


class Progressbar():
    def __init__(self, container: Frame):
        self._setup_label(container)
        self._setup_progressbar(container)
        self.max_value = 100
        self.type = "Audios"

    def _setup_label(self, container: Frame):
        self.label = Label(container, text="Analyzing", width=5)
        self.label.configure(style="Chrome.TLabel", anchor="center")

    def _setup_progressbar(self, container: Frame):
        style = Style()
        style.configure("green.Horizontal.TProgressbar", foreground='gray17', background='green')
        self.progressbar = PBar(container, orient=HORIZONTAL, style="green.Horizontal.TProgressbar")

    def set_value(self, value: int):
        self.progressbar['value'] = value
        self.label['text'] = "{}  {} / {}".format(self.type, value, self.max_value)

    def hide(self):
        self.label.grid_remove()
        self.progressbar.grid_remove()

    def show(self, max_value: int, only_audio: bool):
        self.label.grid(row=0, column=1, sticky='nesw', padx=5)
        self.progressbar.grid(row=0, column=0, sticky='nesw', padx=5)
        self._set_max_value(max_value)
        self.type = "Audios" if only_audio else "Videos"

    def _set_max_value(self, max_value: int):
        self.progressbar['maximum'] = max_value
        self.max_value = max_value
