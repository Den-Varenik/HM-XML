from tkinter import Toplevel, Frame, Label, Listbox, Button,  DISABLED, NORMAL, END
from tkinter import messagebox
from lib.provider import XmlProvider
from lib.win_add import WinToAdd
from lib.win_manage_data import WinToChange


class WinOnePlus(object):

    def __init__(self, button):
        self._win = Toplevel()
        self._provider = XmlProvider('data.xml')

        self._panel1 = Frame(self._win)
        self._panel2 = Frame(self._win)
        self._panel2_1 = Frame(self._panel2)

        self._caption1 = Label(self._panel1)
        self._caption2 = Label(self._panel2)

        self._lbox1 = Listbox(self._panel1)
        self._lbox2 = Listbox(self._panel2)

        self._but_add_frame1 = Button(self._panel1)
        self._but_del_frame1 = Button(self._panel1)

        self._but_add_frame2 = Button(self._panel2_1)
        self._but_del_frame2 = Button(self._panel2_1)
        self._but_change_frame2 = Button(self._panel2_1)
        self._but_upd_frame2 = Button(self._panel2_1)

        self._select = None
        self._select_param = None
        self._button = button
        self._bool = None

    def config(self, text):
        self._win.resizable(False, False)
        self._win.title('Управление')
        self._caption1.config(text=text)
        self._caption2.config(text=f'Управление данными')

        self._lbox1.config(width=25)
        self._lbox2.config(width=25)

        self._but_add_frame1.config(text='Добавить', width=9)
        self._but_del_frame1.config(text='Удалить', width=9)

        self._but_add_frame2.config(text='Добавить', width=9)
        self._but_del_frame2.config(text='Удалить', width=9)
        self._but_change_frame2.config(text='Изменить', width=9)
        self._but_upd_frame2.config(text='Обновить', width=9)

    def layout(self):
        self._panel1.grid(row=0, column=0)
        self._panel2.grid(row=0, column=1)
        self._panel2_1.pack(side='bottom')

        self._caption1.pack(padx=30, pady=15)
        self._caption2.pack(pady=15)

        self._lbox1.pack(padx=30)
        self._lbox2.pack(padx=30)

        self._but_add_frame1.pack(pady=5, padx=5)
        self._but_del_frame1.pack(padx=5)

        self._but_add_frame2.grid(row=0, column=0, pady=5, padx=5)
        self._but_del_frame2.grid(row=1, column=0, padx=5)
        self._but_change_frame2.grid(row=0, column=1, pady=5, padx=5)
        self._but_upd_frame2.grid(row=1, column=1, padx=5)

    """Создание списка департаментов"""
    def department_management(self):
        self._lbox1.delete(0, END)
        self._lbox2.delete(0, END)
        [self._lbox1.insert(END, i) for i in self._provider.get_dep_list()]
        self._button.config(state=DISABLED)
        self.delete_window()
        self._bool = True

    """Создание списка сотрудников"""
    def emp_management(self):
        self._lbox1.delete(0, END)
        self._lbox2.delete(0, END)
        [[self._lbox1.insert(END, i) for i in self._provider.get_emp_list(i)] for i in self._provider.get_dep_list()]
        self._button.config(state=DISABLED)
        self.delete_window()
        self._bool = False

    """Информация по депортаменту"""
    def department_info(self, event):
        w = event.widget
        select = w.curselection()
        if len(select) != 0:
            self._select = self._lbox1.get(select[0])
            self._lbox2.delete(0, END)
            [self._lbox2.insert(END, f'{key}: {item}')
             for key, item in self._provider.get_info(f"dep[@name='{self._select}']").items()]

    """Информация по сотрудникам"""
    def employer_info(self, event):
        w = event.widget
        select = w.curselection()
        if len(select) != 0:
            self._select = self._lbox1.get(select[0])
            self._lbox2.delete(0, END)
            [self._lbox2.insert(END, f'{key}: {item}')
             for key, item in self._provider.get_info(f"dep/emp[@name='{self._select}']").items()]

    """Функция обработки закрытия окна"""
    def delete_window(self):
        def _delete_window():
            self._button.config(state=NORMAL)
            try:
                self._win.destroy()
            except:
                pass
        self._win.protocol('WM_DELETE_WINDOW', _delete_window)

    """Функция вызова окна Add Department"""
    def add_dep(self):
        win = WinToAdd(self._but_add_frame1)
        win.run_dep()

    """Функция вызова окна Add Employer"""
    def add_emp(self):
        win = WinToAdd(self._but_add_frame1)
        win.run_emp()

    """Функция добавления параметров"""
    def add_param(self):
        pass

    """Функция удаления департамента"""
    def delete_dep(self):
        if self._select is not None:
            self._provider.del_dep(self._select)
            self.department_management()
            self._select = None

    """Функция удаления сотрудника"""
    def delete_emp(self):
        if self._select is not None:
            self._provider.del_emp(self._select)
            self.emp_management()
            self._select = None

    """Функция получения параметра"""
    def get_param(self, event):
        w = event.widget
        select = w.curselection()
        if len(select) != 0:
            self._select_param = self._lbox2.get(select[0])

    """Функция удаления параметра"""
    def delete_param(self):
        if self._select_param is not None:
            if self._provider.del_param(self._select, self._select_param, self._bool):
                messagebox.showwarning('Ошибка', 'Параметр не удаляем!')
            else:
                self._select_param = None
                self._lbox2.delete(0, END)
                if self._bool:
                    [self._lbox2.insert(END, f'{key}: {item}')
                     for key, item in self._provider.get_info(f"dep[@name='{self._select}']").items()]
                else:
                    [self._lbox2.insert(END, f'{key}: {item}')
                     for key, item in self._provider.get_info(f"dep/emp[@name='{self._select}']").items()]

    """Функция обновления данных"""
    def updating(self):
        self._provider = XmlProvider('data.xml')
        if self._bool:
            self.department_management()
            self._select = None
            self._select_param = None
        else:
            self.emp_management()
            self._select = None
            self._select_param = None

    """Вызов окна добавления"""
    def add_win(self):
        win = WinToChange(self._but_add_frame2, self._bool, self._select)
        win.run_add()

    """Вызов окна изменения"""
    def change_win(self):
        if self._select_param is not None:
            win = WinToChange(self._but_change_frame2, self._bool, self._select, self._select_param.split(': ')[0])
            win.run_change()
        else:
            messagebox.showinfo('Ошибка', 'Не выделен параметр!')

    def binding(self):
        self._lbox2.bind('<Button-1>', self.get_param)
        self._but_del_frame2.config(command=self.delete_param)
        self._but_upd_frame2.config(command=self.updating)
        self._but_add_frame2.config(command=self.add_win)
        self._but_change_frame2.config(command=self.change_win)

        if self._bool:
            """Binding to Department"""
            self._lbox1.bind('<Button-1>', self.department_info)
            self._but_add_frame1.config(command=self.add_dep)
            self._but_del_frame1.config(command=self.delete_dep)
        else:
            """Binding to employers"""
            self._lbox1.bind('<Button-1>', self.employer_info)
            self._but_add_frame1.config(command=self.add_emp)
            self._but_del_frame1.config(command=self.delete_emp)

    def run(self, text):
        self.config(text)
        self.layout()
        self.binding()
