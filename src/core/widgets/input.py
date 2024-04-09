from tkinter import StringVar
from tkinter.ttk import Button, Frame, Label, Entry


class Input(Frame):
    def __init__(self, container: Frame, row: int, label_text: str, button_text: str, **kw):
        super().__init__(container, **kw)

        self._configure_input(row)
        self._set_label(label_text)
        self._set_entry()
        self._set_button(button_text)

    def _configure_input(self, row: int):
        for i in range(5):
            self.columnconfigure(i, weight=1)

        self.configure(style="Chrome.TFrame")
        self.grid(row=row, column=0, sticky='nesw')

    def _set_label(self, label_text: str):
        self.label = Label(self, text=label_text, width=10)
        self.label.grid(row=0, column=0, sticky='nesw', padx=5)
        self.label.configure(style="Chrome.TLabel")

    def _set_entry(self):
        self.var = StringVar()
        self.entry = Entry(self, textvariable=self.var)
        self.entry.grid(row=0, column=1, columnspan=4, sticky='nesw')
        self.entry.configure(style="Chrome.TEntry")

    def _set_button(self, button_text: str):
        self.button = Button(self, text=button_text)
        self.button.grid(row=0, column=5, sticky='nesw')
        self.button.configure(style="Chrome.TButton")
