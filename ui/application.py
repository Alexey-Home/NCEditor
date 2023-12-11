from tkinter import *
from tkinter import ttk
import ui.renishaw
import ui.bias
import ui.devlopprogram
import controller.subprograms as subp


class App:
    def __init__(self, parent):
        self.field = {}
        self.fields_center = {}
        self.sub_parameteres = None
        self.field_output = None
        self.window = Tk()
        self.created_field = {}
        self.main_parameteres = {}
        self.window.geometry(parent)
        self.window.title("NCEditor")
        self.create_notebook()
        self.create_notebook_renishaw()
        self.create_input_output_fileds()
        self.create_subbutton()
        self.create_info_field()
        self.create_bias()
        self.create_notebook_devprog()
        self.window.mainloop()

    def create_notebook(self):
        """
        Создается фрейм с перечнем вкладок.
        """
        # создаем набор вкладок
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)

        # создаем фреймы
        self.main_fr_bias = ttk.Frame(self.notebook)
        self.main_fr_bias.pack(fill=BOTH, expand=True)

        self.main_renishaw = ttk.Frame(self.notebook)
        self.main_renishaw.pack(fill=BOTH, expand=True)

        self.main_develop_program = ttk.Frame(self.notebook)
        self.main_develop_program.pack(fill=BOTH, expand=True)

        # добавляем фреймы в качестве вкладок
        self.notebook.add(self.main_renishaw, text="Renishaw")
        self.notebook.add(self.main_fr_bias, text="Смещение")
        self.notebook.add(self.main_develop_program, text="Создание программ")

    def create_bias(self):
        self.bias = ui.bias.Bias(self.main_fr_bias)
        self.bias.create(self.field)

    def create_notebook_renishaw(self):
        """
        Создает вкладки для измерений renishaw.
        """
        self.notebook_renishaw = ttk.Notebook(self.main_renishaw)
        self.notebook_renishaw.pack(expand=True, fill=BOTH)

        self.fr_sub_parameters_renishaw = ttk.Frame(self.main_renishaw)
        self.fr_sub_parameters_renishaw.pack(fill=BOTH, expand=True)
        self.sub = ui.renishaw.SubParameteres(self.fr_sub_parameters_renishaw)
        self.sub_parameteres = self.sub.create_sub_parameters()

        self.main_fr_single_surface = ttk.Frame(self.notebook_renishaw)
        self.main_fr_single_surface.pack(fill=BOTH, expand=True)

        self.main_fr_hole = ttk.Frame(self.notebook_renishaw)
        self.main_fr_hole.pack(fill=BOTH, expand=True)

        self.main_fr_cylinder = ttk.Frame(self.notebook_renishaw)
        self.main_fr_cylinder.pack(fill=BOTH, expand=True)

        self.main_fr_groove = ttk.Frame(self.notebook_renishaw)
        self.main_fr_groove.pack(fill=BOTH, expand=True)

        self.main_fr_ledge = ttk.Frame(self.notebook_renishaw)
        self.main_fr_ledge.pack(fill=BOTH, expand=True)

        self.notebook_renishaw.add(self.main_fr_single_surface, text="Одиночная поверхность")
        self.single_surface = ui.renishaw.SingleSurface(self.main_fr_single_surface)
        self.main_parameteres = self.single_surface.create(self.main_parameteres, self.sub_parameteres, self.field)

        self.notebook_renishaw.add(self.main_fr_cylinder, text="Цилиндр")
        self.cylinder = ui.renishaw.Cylinder(self.main_fr_cylinder)
        self.main_parameteres = self.cylinder.create(self.main_parameteres, self.sub_parameteres, self.field)

        self.notebook_renishaw.add(self.main_fr_hole, text="Отверстие")
        self.hole = ui.renishaw.Hole(self.main_fr_hole)
        self.main_parameteres = self.hole.create(self.main_parameteres, self.sub_parameteres, self.field)

        self.notebook_renishaw.add(self.main_fr_groove, text="Паз")
        self.groove = ui.renishaw.Groove(self.main_fr_groove)
        self.main_parameteres = self.groove.create(self.main_parameteres, self.sub_parameteres, self.field)

        self.notebook_renishaw.add(self.main_fr_ledge, text="Выступ")
        self.ledge = ui.renishaw.Ledge(self.main_fr_ledge)
        self.main_parameteres = self.ledge.create(self.main_parameteres, self.sub_parameteres, self.field)

    def create_notebook_devprog(self):
        self.notebook_devprog = ttk.Notebook(self.main_develop_program)
        self.notebook_devprog.pack(expand=True, fill=BOTH)

        self.main_fr_hole = Frame(self.notebook_devprog)
        self.main_fr_hole.pack(expand=True, fill=BOTH)

        self.notebook_devprog.add(self.main_fr_hole, text="Отверстие")
        self.program = ui.devlopprogram.Hole(self.main_fr_hole)

        self.centering_hole = Frame(self.main_fr_hole)
        self.centering_hole.pack(side=BOTTOM, fill=BOTH)

        self.centr_hole = ui.devlopprogram.HolesCenters(self.centering_hole)
        self.fields_center = self.centr_hole.create(self.field)

        self.main_paremeteres_hole = Frame(self.main_fr_hole)
        self.main_paremeteres_hole.pack(side=TOP, fill=BOTH)
        self.parameteres_hole = ui.devlopprogram.Hole(self.main_paremeteres_hole)
        self.parameteres_hole.create(self.field, self.fields_center)

    def create_input_output_fileds(self):
        """
        Создаются поля для вывода и ввода управляюще программы.
        """
        self.fr_input_output = Frame(self.window)
        self.fr_input_output.pack(side=TOP, fill=BOTH, expand=True)

        self.field['input'] = Text(self.fr_input_output, width=10)
        self.field['input'].pack(side=LEFT, fill=BOTH, expand=True)
        scroll = Scrollbar(self.fr_input_output, command=self.field['input'].yview)
        scroll.pack(side=LEFT, fill=Y)

        self.field["input"].config(yscrollcommand=scroll.set)

        self.field['output'] = Text(self.fr_input_output, width=10)
        self.field['output'].pack(side=LEFT, fill=BOTH, expand=True)
        scroll1 = Scrollbar(self.fr_input_output, command=self.field['output'].yview)
        scroll1.pack(side=LEFT, fill=Y)

        self.field["output"].config(yscrollcommand=scroll.set)

    def create_subbutton(self):
        """
        Создается поля и кнопки для полей ввода и выовда
        """
        self.main_fr_subbutton = Frame(self.window)
        self.main_fr_subbutton.pack(side=TOP, fill=BOTH, expand=True)

        self.fr_subbutton_input = Frame(self.main_fr_subbutton)
        self.fr_subbutton_input.pack(side=LEFT, fill=BOTH, expand=True)

        self.fr_subbutton_output = Frame(self.main_fr_subbutton)
        self.fr_subbutton_output.pack(side=LEFT, fill=BOTH, expand=True)

        self.clear_input = Button(self.fr_subbutton_input, text="Очистить",
                                  command=lambda: subp.clear_input_field(self.field))
        self.clear_input.pack(side=RIGHT)

        self.open_input = Button(self.fr_subbutton_input, text="Открыть",
                                 command=lambda: subp.open_file(self.field))
        self.open_input.pack(side=RIGHT)

        self.clear_output = Button(self.fr_subbutton_output, text="Очистить",
                                   command=lambda: subp.clear_output_field(self.field))
        self.clear_output.pack(side=RIGHT)

        self.save_output = Button(self.fr_subbutton_output, text="Сохранить",
                                 command=lambda: subp.save_file(self.field))
        self.save_output.pack(side=RIGHT)

    def create_info_field(self):
        """Создается фрейм и поля для вывода сообщений"""

        self.fr_info = Frame(self.window)
        self.fr_info.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.field['info'] = Text(self.fr_info)
        self.field['info'].config(state='disabled')
        self.field['info'].pack(side=LEFT, fill=BOTH, expand=True)


if __name__ == "__main__":
    app = App("800x600")
