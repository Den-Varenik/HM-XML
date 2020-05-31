from tkinter import Toplevel, Label, Button, Entry, DISABLED, NORMAL, END
from tkinter import messagebox
from lib.provider import XmlProvider


class WinToAdd(object):

    def __init__(self, button):
        self._win_add = Toplevel()
        self._provider = XmlProvider('data.xml')

        self._label_dep = Label(self._win_add)
        self._label_emp = Label(self._win_add)
        self._name = Label(self._win_add)
        self._name_dep = Label(self._win_add)
        self._age = Label(self._win_add)
        self._position = Label(self._win_add)
        self._salary = Label(self._win_add)

        self._ent_name_dep = Entry(self._win_add)
        self._ent_name = Entry(self._win_add)
        self._ent_age = Entry(self._win_add)
        self._ent_position = Entry(self._win_add)
        self._ent_salary = Entry(self._win_add)

        self._save = Button(self._win_add)
        self._button = button

    def main_config(self):
        self._win_add.resizable(False, False)
        self._win_add.title('Окно управления')

    def dep_config_layout(self):
        """Config"""
        self._label_dep.config(text='Добавление департамента')
        self._name.config(text='Name')
        self._save.config(text='Сохранить', command=self.add_dep)

        """Layout"""
        self._label_dep.grid(row=0, column=0, columnspan=2, pady=10)
        self._name.grid(row=1, column=0, padx=10, pady=5)
        self._save.grid(row=3, column=0, columnspan=2, pady=10)

        self._ent_name.grid(row=1, column=1, padx=10, pady=5)

    def emp_config_layout(self):
        """Config"""
        self._label_emp.config(text='Добавление сотрудника')
        self._name_dep.config(text='Name Dep')
        self._name.config(text='Name')
        self._age.config(text='Age')
        self._position.config(text='Position')
        self._salary.config(text='Salary')
        self._save.config(text='Сохранить', command=self.add_emp)

        """Layout"""
        self._label_emp.grid(row=0, column=0, columnspan=2, pady=10)
        self._name_dep.grid(row=1, column=0, padx=10, pady=5)
        self._name.grid(row=2, column=0, padx=10, pady=5)
        self._age.grid(row=3, column=0, padx=10, pady=5)
        self._position.grid(row=4, column=0, padx=10, pady=5)
        self._salary.grid(row=5, column=0, padx=10, pady=5)
        self._save.grid(row=6, column=0, columnspan=2, pady=10)

        self._ent_name_dep.grid(row=1, column=1, padx=10, pady=5)
        self._ent_name.grid(row=2, column=1, padx=10, pady=5)
        self._ent_age.grid(row=3, column=1, padx=10, pady=5)
        self._ent_position.grid(row=4, column=1, padx=10, pady=5)
        self._ent_salary.grid(row=5, column=1, padx=10, pady=5)

    """Заблокировать кнопку входа"""
    def block(self):
        self._button.config(state=DISABLED)

    """Функция обработки закрытия окна"""
    def delete_window(self):
        def _delete_window():
            self._button.config(state=NORMAL)
            try:
                self._win_add.destroy()
            except:
                pass
        self._win_add.protocol('WM_DELETE_WINDOW', _delete_window)

    """Функция добавления департамента"""
    def add_dep(self):
        dep = self._ent_name.get()
        if dep != '':
            self._provider.add_dep(dep)
            self._ent_name.delete(0, END)
            messagebox.showinfo('Инфо', 'Департамент успешно добавлен')
        else:
            messagebox.showerror('Ошибка', 'Данные не введены!')

    """Функция добавления сотрудника"""
    def add_emp(self):
        dep = self._ent_name_dep.get()
        emp = self._ent_name.get()
        age = self._ent_age.get()
        position = self._ent_position.get()
        salary = self._ent_salary.get()
        if dep in self._provider.get_dep_list():
            if emp != '' and age != '' and position != '' and salary != '':
                try:
                    age = int(age)
                    salary = float(salary)
                except ValueError:
                    messagebox.showerror('Ошибка', 'Возраст и зарплата должны\nиметь только числовые значения!')
                self._provider.add_emp(dep, emp, age, position, salary)
                self._ent_name_dep.delete(0, END)
                self._ent_name.delete(0, END)
                self._ent_age.delete(0, END)
                self._ent_position.delete(0, END)
                self._ent_salary.delete(0, END)
                messagebox.showinfo('Инфо', 'Сотрудник успешно добавлен!')
            else:
                messagebox.showerror('Ошибка', 'Введите все данные!')
        else:
            messagebox.showerror('Ошибка', 'Введите существующий департамент!')

    def run_dep(self):
        self.main_config()
        self.block()
        self.delete_window()
        self.dep_config_layout()

    def run_emp(self):
        self.main_config()
        self.block()
        self.delete_window()
        self.emp_config_layout()
