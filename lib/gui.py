from tkinter import Tk, Frame, Label, Listbox, Button, END
from lib.mui import WinOnePlus
from lib.provider import XmlProvider
from lib.search_win import WinToSearch


class Window(object):

    def __init__(self):
        self._root = Tk()
        self._provider = XmlProvider('data.xml')

        self._panel1 = Frame(self._root)
        self._panel2 = Frame(self._root)
        self._panel3 = Frame(self._root)
        self._panel4 = Frame(self._root)

        self._caption1 = Label(self._panel1)
        self._caption2 = Label(self._panel2)
        self._caption3 = Label(self._panel3)

        self._lbox1 = Listbox(self._panel1)
        self._lbox2 = Listbox(self._panel2)
        self._lbox3 = Listbox(self._panel3)

        self._admin_dep_but = Button(self._panel4)
        self._admin_emp_but = Button(self._panel4)
        self._search = Button(self._panel4)
        self._update = Button(self._panel4)

    def main_config(self):
        self._root.geometry('590x270')
        self._root.resizable(False, False)
        self._root.title('Отдел')

    def config(self):
        self._caption1.config(text='Департаменты')
        self._caption2.config(text='Сотрудники')
        self._caption3.config(text='Персональная информация')

        self._lbox1.config(width=25)
        self._lbox2.config(width=25)
        self._lbox3.config(width=25)

        self._admin_dep_but.config(text='Управление деп.', width=15)
        self._admin_emp_but.config(text='Управление сотр.', width=15)
        self._search.config(text='Поиск сотрудника', width=15)
        self._update.config(text='Обновить данные', width=15)

    def layout(self):
        self._panel1.grid(row=0, column=0)
        self._panel2.grid(row=0, column=1)
        self._panel3.grid(row=0, column=2)
        self._panel4.grid(row=1, column=0, columnspan=3)

        self._caption1.pack(padx=30, pady=15)
        self._caption2.pack(pady=15)
        self._caption3.pack(padx=30, pady=15)

        self._lbox1.pack(padx=30)
        self._lbox2.pack()
        self._lbox3.pack(padx=30)

        self._admin_dep_but.grid(row=0, column=1, pady=15)
        self._admin_emp_but.grid(row=0, column=2, pady=15, padx=16)
        self._search.grid(row=0, column=3, pady=15, padx=16)
        self._update.grid(row=0, column=4, pady=15)

    """Получение списка департаментов и вывод в listbox"""
    def department_management(self):
        # dep_list = self._provider.get_dep_list()
        # for i in dep_list:
        #     self._lbox1.insert(END, i)
        self._lbox1.delete(0, END)
        self._lbox2.delete(0, END)
        self._lbox3.delete(0, END)
        [self._lbox1.insert(END, i) for i in self._provider.get_dep_list()]

    """Получение списка сотрудников и вывод в listbox"""
    def employee_management(self, event):
        w = event.widget
        select = w.curselection()
        if len(select) != 0:
            self._lbox2.delete(0, END)
            self._lbox3.delete(0, END)

            # dep = self._lbox1.get(select[0])
            # emp_list = self._provider.get_emp_list(dep)
            # for i in emp_list:
            #     self._lbox2.insert(END, i)

            [self._lbox2.insert(END, i) for i in self._provider.get_emp_list(self._lbox1.get(select[0]))]

    """Получение персональной информации и вывод в listbox"""
    def personal_info(self, event):
        w = event.widget
        select = w.curselection()
        if len(select) != 0:
            self._lbox3.delete(0, END)

            # emp = self._lbox2.get(select[0])
            # emp_dict = self._provider.get_emp_info(emp)
            # for key, item in emp_dict.items():
            #     self._lbox3.insert(END, f'{key}: {item}')

            [self._lbox3.insert(END, f'{key}: {item}')
             for key, item in self._provider.get_info(f"dep/emp[@name='{self._lbox2.get(select[0])}']").items()]

    """Вызов окна редактироавния"""
    def admin_win(self, text: str):
        if text == 'Департаменты':
            win = WinOnePlus(self._admin_dep_but)
            win.department_management()
            win.run(text)
        elif text == 'Сотрудники':
            win = WinOnePlus(self._admin_emp_but)
            win.emp_management()
            win.run(text)

    """Админ окно департамента"""
    def admin_dep(self):
        self.admin_win('Департаменты')

    """Админ окно сотрудников"""
    def admin_emp(self):
        self.admin_win('Сотрудники')

    """Поиск сотрудника"""
    def search_emp(self):
        win = WinToSearch(self._search, self._lbox2)
        win.run()

    """Обновить данные"""
    def update_func(self):
        self._provider = XmlProvider('data.xml')
        self.department_management()

    def binding(self):
        self._lbox1.bind('<Button-1>', self.employee_management)
        self._lbox2.bind('<Button-1>', self.personal_info)

        self._admin_dep_but.config(command=self.admin_dep)
        self._admin_emp_but.config(command=self.admin_emp)
        self._search.config(command=self.search_emp)
        self._update.config(command=self.update_func)

    def run(self):
        self.main_config()
        self.config()
        self.layout()
        self.binding()
        self.department_management()
        self._root.mainloop()
