from tkinter import Toplevel, Label, Button, Entry, DISABLED, NORMAL, END
from tkinter import messagebox
from lib.provider import XmlProvider


class WinToSearch(object):

    def __init__(self, button, listbox):
        self._win = Toplevel()
        self._provider = XmlProvider('data.xml')

        self._logo = Label(self._win)
        self._label_name = Label(self._win)

        self._ent_name = Entry(self._win)

        self._search = Button(self._win)

        self._button = button
        self._result = None
        self._listbox = listbox

    def config(self):
        self._win.resizable(False, False)
        self._win.title('Поиск')
        self._logo.config(text='Поиск сотрудника')
        self._label_name.config(text='Name')
        self._search.config(text='Поиск', command=self.search)

    def layout(self):
        self._logo.grid(row=0, column=0, columnspan=2, pady=10)
        self._label_name.grid(row=1, column=0, padx=10, pady=5)
        self._ent_name.grid(row=1, column=1, padx=10, pady=5)
        self._search.grid(row=2, column=0, columnspan=2, pady=10)

    def search(self):
        name = self._ent_name.get()
        if name != '':
            self._result = self._provider.find_emp(name)
            self._ent_name.delete(0, END)
            if self._result is None:
                messagebox.showinfo('Инфо', f'Сотрудник "{name}" не найден!')
            else:
                self._listbox.delete(0, END)
                self._listbox.insert(END, name)
        else:
            messagebox.showerror('Ошибка', 'Данные не введены!')

    """Заблокировать кнопку входа"""
    def block(self):
        self._button.config(state=DISABLED)

    """Функция обработки закрытия окна"""
    def delete_window(self):
        def _delete_window():
            self._button.config(state=NORMAL)
            try:
                self._win.destroy()
            except:
                pass
        self._win.protocol('WM_DELETE_WINDOW', _delete_window)

    def run(self):
        self.config()
        self.layout()
        self.block()
        self.delete_window()
