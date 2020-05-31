from tkinter import Toplevel, Label, Button, Entry, DISABLED, NORMAL, END
from tkinter import messagebox
from lib.provider import XmlProvider


class WinToChange(object):

    def __init__(self, button, bol, select, key=None):
        self._win = Toplevel()
        self._provider = XmlProvider('data.xml')

        self._logo = Label(self._win)
        self._attrib = Label(self._win)
        self._item = Label(self._win)

        self._ent_key = Entry(self._win)
        self._ent_item = Entry(self._win)

        self._save = Button(self._win)

        self._select = select
        self._key = key
        self._button = button
        self._bool = bol

    def main_config(self):
        self._win.resizable(False, False)
        self._win.title('Управление базой')

    def change_data_config_layout(self):
        """Config"""
        self._logo.config(text='Изменение данных')
        self._attrib.config(text=self._key)
        self._save.config(text='Сохранить', command=self.change_data)

        """Layout"""
        self._logo.grid(row=0, column=0, columnspan=2, pady=10)
        self._attrib.grid(row=1, column=0, padx=10, pady=5)
        self._ent_item.grid(row=1, column=1, padx=10, pady=5)
        self._save.grid(row=2, column=0, columnspan=2, pady=10)

    def add_data_config_layout(self):
        """Config"""
        self._logo.config(text='Добавление данных')
        self._attrib.config(text='Атрибут')
        self._item.config(text='Значение')
        self._save.config(text='Сохранить', command=self.add_data)

        """Layout"""
        self._logo.grid(row=0, column=0, columnspan=2, pady=10)
        self._attrib.grid(row=1, column=0, padx=10, pady=5)
        self._item.grid(row=1, column=1, padx=10, pady=5)
        self._ent_key.grid(row=2, column=0, padx=10, pady=5)
        self._ent_item.grid(row=2, column=1, padx=10, pady=5)
        self._save.grid(row=3, column=0, columnspan=2, pady=10)

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

    """Функция изменения данных"""
    def change_data(self):
        item = self._ent_item.get()
        if item != '':
            self._provider.change_data(self._select, self._key, item, self._bool)
            self._ent_item.delete(0, END)
            messagebox.showinfo('Инфо', 'Изменения внесены!')
        else:
            messagebox.showerror('Ошибка', 'Данные не введены!')

    """Функция добавления данных"""
    def add_data(self):
        key = self._ent_key.get()
        item = self._ent_item.get()
        if item != '' and key != '':
            self._provider.change_data(self._select, key, item, self._bool)
            self._ent_key.delete(0, END)
            self._ent_item.delete(0, END)
            messagebox.showinfo('Инфо', 'Изменения внесены!')
        else:
            messagebox.showerror('Ошибка', 'Все поля должны быть заполнены!')

    def run_change(self):
        self.main_config()
        self.change_data_config_layout()
        self.block()
        self.delete_window()

    def run_add(self):
        self.main_config()
        self.add_data_config_layout()
        self.block()
        self.delete_window()
