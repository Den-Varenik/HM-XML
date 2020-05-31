import xml.etree.ElementTree as et


class XmlProvider(object):
    
    def __init__(self, file: str):
        self._file = file
        self._tree = et.parse(self._file)
        self._root = self._tree.getroot()

    def get_dep_list(self) -> list:
        # dep_names = list()
        # departments = self._root.findall('dep')
        # for d in departments:
        #     dep_names.append(f'{d.get("id")} -> {d.get("name")}')
        # return dep_names
        return [f'{i.get("name")}' for i in self._root.findall('dep')]

    def get_emp_list(self, dep_name: str) -> list:
        # id_dep = int(dep_name.split('-')[1]) * 100
        return [f'{i.get("name")}' for i in self._tree.findall(f"dep[@id='{int(dep_name.split('-')[-1]) * 100}']/emp")]

    def get_info(self, emp_name: str) -> dict:
        # emp = self._tree.find(f"dep/emp[@name='{emp_name}']")
        return self._tree.find(emp_name).attrib

    def add_dep(self, dep_name: str) -> None:
        num = int(self._root.findall('dep')[-1].attrib['id'])//100+1
        dep = et.SubElement(self._root, 'dep')
        dep.set('id', f'{num*100}')
        dep.set('name', f'{dep_name}-{num}')
        self._tree.write(self._file, encoding='utf-8')

    def add_emp(self, dep_name: str, name: str, age: int, position: str, salary: float) -> None:
        dep = self._root.find(f"dep[@name='{dep_name}']")
        emp = et.SubElement(dep, 'emp')
        employers_name = self.get_emp_list(dep_name)
        if employers_name[0] == 'None':
            emp.set('id', f'{int(dep_name.split("-")[-1])*100+1}')
            print('ok')
        else:
            employers = self._root.find(f"dep[@name='{dep_name}']/emp[@name='{employers_name[-2]}']")
            emp.set('id', f'{int(employers.attrib["id"])+1}')
        emp.set('name', name)
        emp.set('age', f'{age}')
        emp.set('position', position)
        emp.set('salary', f'{salary}')
        self._tree.write(self._file, encoding='utf-8')

    def change_data(self, parent, key: str, item: str, bol: bool) -> None:
        if bol:
            self._root.find(f"dep[@name='{parent}']").attrib[key] = item
        else:
            self._root.find(f"dep/emp[@name='{parent}']").attrib[key] = item
        self._tree.write(self._file, encoding='utf-8')

    def del_dep(self, dep_name: str) -> None:
        self._root.remove(self._tree.find(f"dep[@name='{dep_name}']"))
        self._tree.write(self._file, encoding='utf-8')

    def del_emp(self, emp_name: str):
        emp = self._tree.find(f"dep/emp[@name='{emp_name}']")
        emp_id = int(emp.attrib['id'])
        dep = self._tree.find(f"dep[@id='{emp_id//100*100}']")
        dep.remove(emp)
        for employers_name in self.get_emp_list(dep.attrib['name']):
            employers = self._tree.find(f"dep/emp[@name='{employers_name}']")
            employers_id = int(employers.attrib['id'])
            if employers_id > emp_id:
                employers.set('id', f'{employers_id-1}')
        self._tree.write(self._file, encoding='utf-8')

    def del_param(self, element: str, atr: str, bol: bool) -> bool:
        if element != atr.split(': ')[1] and atr.split(': ')[0] != 'id':
            if bol:
                self._tree.find(f"dep[@name='{element}']").attrib.pop(atr.split(': ')[0])
            else:
                self._tree.find(f"dep/emp[@name='{element}']").attrib.pop(atr.split(': ')[0])
            self._tree.write(self._file, encoding='utf-8')
        else:
            return True
        return False

    def find_emp(self, emp_name: str):
        return self._root.find(f"dep/emp[@name='{emp_name}']")
