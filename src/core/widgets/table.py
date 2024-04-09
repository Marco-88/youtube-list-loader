from tkinter import NO, CENTER, Event
from tkinter.ttk import Treeview, Frame

from ..utils.table_videos import open_directory


class Table(Treeview):
    keys = ('id', 'title', 'author', 'length', 'size', 'download')
    widths = {'id': 20, 'title': 140, 'author': 80, 'length': 20, 'size': 20, 'download': 20}

    def __init__(self, container: Frame, **kw):
        super().__init__(container, **kw)

        self._configure_layout()
        self._setup_columns()
        self.set_row_behaviour()
        self.directory = ''

    def _configure_layout(self) -> None:
        self.grid(row=2, column=0, columnspan=5, sticky='news')
        self.configure(style='Chrome.Treeview')

    def _setup_columns(self) -> None:
        self['columns'] = Table.keys
        self.column("#0", width=0, stretch=NO)
        self.heading("#0", text="", anchor=CENTER)

        for _id in self['columns']:
            self.column(_id, anchor=CENTER, width=Table.widths[_id])
            self.heading(_id, text=_id.capitalize(), anchor=CENTER)

    def set_row_behaviour(self) -> None:
        self.tag_configure("done", foreground='#00aa00')
        self.bind("<Double-1>", self.on_double_click)
        self.bind("<Key>", self.on_key_press)

    def on_double_click(self, event: Event) -> None:
        item = self.selection()[0]
        path = f'{self.directory}/{self.item(item, "values")[1]}'

        open_directory(path)

    def on_key_press(self, event: Event) -> None:
        if event.keysym == 'Delete':
            for item in self.selection():
                print(f'Remove selected entry: {self.item(item, "values")[1]}')
                self.delete(item)
