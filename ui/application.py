from tkinter import *
from tkinter import ttk
import controller.function as fun
import controller.renishaw as ren
import controller.subprograms as subp
import sqlite3 as sq


class App:
    def __init__(self, parent):
        self.window = Tk()
        self.work_offset = ["Нет", "G54", "G55", "G56", "G57", "G58", "G59"] + [f"G54.1P{i}" for i in range(1, 99)]
        self.created_field = {}
        self.window.geometry(parent)
        self.window.title("NCEditor")
        self.create_notebook()
        self.create_parameters_bias()
        # self.create_parameters_correction()
        self.create_notebook_renishaw()
        self.create_input_output_fileds()
        self.create_info_field()
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

        self.main_fr_correction = ttk.Frame(self.notebook)
        self.main_fr_correction.pack(fill=BOTH, expand=True)

        self.main_renishaw = ttk.Frame(self.notebook)
        self.main_renishaw.pack(fill=BOTH, expand=True)

        # добавляем фреймы в качестве вкладок
        self.notebook.add(self.main_renishaw, text="Renishaw")
        self.notebook.add(self.main_fr_bias, text="Смещение")
        self.notebook.add(self.main_fr_correction, text="Коррекция на радиус")

    def create_notebook_renishaw(self):
        """
        Создает вкладки для измерений renishaw.
        """
        self.notebook_renishaw = ttk.Notebook(self.main_renishaw)
        self.notebook_renishaw.pack(expand=True, fill=BOTH)

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
        self.create_single_surface()

        self.notebook_renishaw.add(self.main_fr_cylinder, text="Цилиндр")
        self.create_cylinder()

        self.notebook_renishaw.add(self.main_fr_hole, text="Отверстие")
        self.create_hole()

        self.notebook_renishaw.add(self.main_fr_groove, text="Паз")
        self.create_groove()

        self.notebook_renishaw.add(self.main_fr_ledge, text="Выступ")
        self.create_ledge()

        self.fr_sub_parameters_renishaw = ttk.Frame(self.main_renishaw)
        self.fr_sub_parameters_renishaw.pack(fill=BOTH, expand=True)
        self.create_sub_parameters()

    def create_sub_parameters(self):
        """
        Создает дополнительные параметры для renishaw.
        """

        tool_number = ["без инструмента"] + [f"{i:02d}" for i in range(1, 41)]
        devices = ["fanuc"]
        version_pogramm = ["новая", "старая"]

        self.frame_param_1 = Frame(self.fr_sub_parameters_renishaw)
        self.frame_param_1.pack(side=LEFT, fill=BOTH, expand=True)

        self.frame_param_2 = Frame(self.fr_sub_parameters_renishaw)
        self.frame_param_2.pack(side=LEFT, fill=BOTH, expand=True)

        self.label_position_x = Label(self.frame_param_1, text="Нач. положение X:", justify=LEFT)
        self.label_position_x.grid(row=0, column=0)
        self.position_x = Entry(self.frame_param_1)
        self.position_x.config(justify=RIGHT)
        self.position_x.insert(1, "0")
        self.position_x.grid(row=0, column=1)

        self.label_position_y = Label(self.frame_param_1, text="Нач. положение Y:")
        self.label_position_y.grid(row=1, column=0)
        self.position_y = Entry(self.frame_param_1)
        self.position_y.config(justify=RIGHT)
        self.position_y.insert(1, "0")
        self.position_y.grid(row=1, column=1)

        self.label_position_z = Label(self.frame_param_1, text="Нач. положение Z:")
        self.label_position_z.grid(row=2, column=0)
        self.position_z = Entry(self.frame_param_1)
        self.position_z.config(justify=RIGHT)
        self.position_z.insert(1, "150")
        self.position_z.grid(row=2, column=1)

        self.label_position_h = Label(self.frame_param_1, text="Высота измерения:")
        self.label_position_h.grid(row=3, column=0)
        self.position_h = Entry(self.frame_param_1)
        self.position_h.config(justify=RIGHT)
        self.position_h.insert(1, "100")
        self.position_h.grid(row=3, column=1)

        self.label_device = Label(self.frame_param_2, text="Устройство ЧПУ:")
        self.label_device.grid(row=0, column=0)
        self.field_device = ttk.Combobox(self.frame_param_2, values=devices, justify=RIGHT)
        self.field_device.current(0)
        self.field_device.grid(row=0, column=1)

        self.label_tool = Label(self.frame_param_2, text="Номер инструмента:")
        self.label_tool.grid(row=1, column=0)
        self.field_tool_number = ttk.Combobox(self.frame_param_2, values=tool_number, justify=RIGHT)
        self.field_tool_number.current(40)
        self.field_tool_number.grid(row=1, column=1)

        self.label_version_shample = Label(self.frame_param_2, text="Версия программы:")
        self.label_version_shample.grid(row=2, column=0)
        self.version_shample = ttk.Combobox(self.frame_param_2, values=version_pogramm, justify=RIGHT)
        self.version_shample.current(0)
        self.version_shample.grid(row=2, column=1)

    def create_ledge(self):
        frame = self.main_fr_ledge
        axis = ["X", "Y"]

        ledge = {
            "axis": dict(type="button",
                         text="Ось:",
                         name="Ось выступа",
                         frame=frame,
                         command=lambda: subp.show_picture(ledge["axis"])
                         ),
            "value_axis": dict(type="combobox",
                               name="Значение оси",
                               frame=frame,
                               values=axis,
                               width=5,
                               current=0
                               ),
            "width": dict(type="button",
                          text="Ширина:",
                          name="Ширина выступа",
                          frame=frame,
                          command=lambda: subp.show_picture(ledge["width"])),
            "value_width": dict(type="entry",
                                frame=frame,
                                name="Значение ширины"),
            "relative_distance": dict(type="button",
                                      text="Отн.расстояние по Z:",
                                      name="Относительное расстояние по Z выступа",
                                      frame=frame,
                                      command=lambda: subp.show_picture(ledge["relative_distance"])),
            "value_relative_distance": dict(type="entry",
                                            name="Значение отн.расстояния по Z",
                                            frame=frame),
            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=frame,
                                   values=self.work_offset,
                                   current=1),
            "generate_groove": dict(type="button",
                                    text="Сгенерировать",
                                    name="Генерация",
                                    frame=frame,
                                    command=lambda: self.generate_program("ledge")),

        }
        self.created_field["ledge"] = self.create_main_parameters(ledge)


    def create_groove(self):
        frame = self.main_fr_groove
        axis = ["X", "Y"]

        groove = {
            "axis": dict(type="button",
                         text="Ось:",
                         name="Ось паза",
                         frame=frame,
                         command=lambda: subp.show_picture(groove["axis"])
                         ),
            "value_axis": dict(type="combobox",
                               name="Значение оси",
                               frame=frame,
                               values=axis,
                               width=5,
                               current=0
                               ),
            "width": dict(type="button",
                          text="Ширина:",
                          name="Ширина паза",
                          frame=frame,
                          command=lambda: subp.show_picture(groove["width"])),
            "value_width": dict(type="entry",
                                frame=frame,
                                name="Значение ширины"),
            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=frame,
                                   values=self.work_offset,
                                   current=1),
            "generate_groove": dict(type="button",
                                    text="Сгенерировать",
                                    name="Генерация",
                                    frame=frame,
                                    command=lambda: self.generate_program("groove")),

        }
        self.created_field["groove"] = self.create_main_parameters(groove)

    def create_single_surface(self):
        """
        Создает параметры для renishaw - одиночная поверхность.
        """

        coordinate_dimension = ["X плюс", "X минус", "Y плюс", "Y минус", "Z минус"]
        frame = self.main_fr_single_surface

        single_surface = {
            "direct_measure": dict(type="button",
                                   text="Направление измерения:",
                                   name="Направление измерения",
                                   frame=frame,
                                   command=lambda: subp.show_picture(single_surface["direct_measure"])),
            "move_dimension": dict(type="combobox",
                                   name="Направление движения",
                                   frame=self.main_fr_single_surface,
                                   values=coordinate_dimension,
                                   width=5,
                                   current=1),

            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=frame,
                                   values=self.work_offset,
                                   current=1),
            "surface_position": dict(type="button",
                                     text="Положение поверхности:",
                                     name="Положение поверхности",
                                     frame=frame,
                                     command=lambda: subp.show_picture(single_surface["surface_position"])),
            "value_coordinate": dict(type="entry",
                                     name="Значение положение поверхности",
                                     frame=frame),
            "generate_hole": dict(type="button",
                                  text="Сгенерировать",
                                  name="Генерация",
                                  frame=frame,
                                  command=lambda: self.generate_program("single_surface")),

        }

        self.created_field["single_surface"] = self.create_main_parameters(single_surface)

    def create_hole(self):
        frame = self.main_fr_hole

        hole = {
            "diametr_hole": dict(type="button",
                                 text="Диаметр:",
                                 name="Диаметр отверстия",
                                 frame=frame,
                                 command=lambda: subp.show_picture(hole["diametr_hole"])),
            "value_diametr": dict(type="entry",
                                  name="Значение диаметра",
                                  frame=frame),
            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=frame,
                                   values=self.work_offset,
                                   current=1),
            "generate_surface": dict(type="button",
                                     text="Сгенерировать",
                                     name="Генерация",
                                     frame=frame,
                                     command=lambda: self.generate_program("hole")),
        }

        self.created_field["hole"] = self.create_main_parameters(hole)

    def create_cylinder(self):
        frame = self.main_fr_cylinder

        cylinder = {
            "diametr_cylinder": dict(type="button",
                                     text="Диаметр:",
                                     name="Диаметр цилиндра",
                                     frame=frame,
                                     command=lambda: subp.show_picture(cylinder["diametr_cylinder"])),
            "value_diametr": dict(type="entry",
                                  name="Значение диаметра",
                                  frame=frame),
            "relative_distance": dict(type="button",
                                      text="Отн.расстояние по Z:",
                                      name="Относительное расстояние по Z цилиндра",
                                      frame=frame,
                                      command=lambda: subp.show_picture(cylinder["relative_distance"])),
            "value_relative_distance": dict(type="entry",
                                            name="Значение отн.расстояния по Z",
                                            frame=frame),
            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=frame,
                                   values=self.work_offset,
                                   current=1),
            "generate_surface": dict(type="button",
                                     text="Сгенерировать",
                                     name="Генерация",
                                     frame=frame,
                                     command=lambda: self.generate_program("cylinder")),
        }

        self.created_field["cylinder"] = self.create_main_parameters(cylinder)

    def generate_program(self, name_op):

        main_param = subp.get_main_parameters(self.created_field[name_op])
        sub_param = self.get_sub_parameters()

        parameters_hole = {**main_param, **sub_param}

        input_text = self.get_input_text()
        if self.check_parameter(parameters_hole):
            text = ren.create(parameters_hole, name_op)
            self.field_output.insert(1.0, "".join(text))
        else:
            return

    def get_sub_parameters(self):
        """
        Получает и возращает дополнительные параметры для renishaw.
        """
        sub_parameters = {
            "device": self.field_device.get(),
            "toolnum": self.field_tool_number.get(),
            "pos_x": self.position_x.get(),
            "pos_y": self.position_y.get(),
            "pos_z": self.position_z.get(),
            "pos_h": self.position_h.get(),
            "version": self.version_shample.get(),
        }
        return sub_parameters

    def create_parameters_correction(self):
        """
        Создается фрейм с параметрами для вкладки "Коррекция на радиус".
        """

        self.parameters_fr_correction = Frame(self.main_fr_correction)
        self.parameters_fr_correction.pack(side=TOP, fill=BOTH, expand=True)

        self.label_value = Label(self.parameters_fr_correction, text="Значение")
        self.label_value.pack(side=LEFT)
        self.field_entry_value = Entry(self.parameters_fr_correction)
        self.field_entry_value.config(justify=RIGHT)
        self.field_entry_value.pack(side=LEFT)
        self.field_entry_value.insert(1, "0")

        self.label_direction = Label(self.parameters_fr_correction, text="Направление")
        self.label_direction.pack(side=LEFT)
        self.field_choice_direction = ttk.Combobox(self.parameters_fr_correction, values=["Внутрь", "Наружу"],
                                                   justify=RIGHT)
        self.field_choice_direction.current(0)
        self.field_choice_direction.pack(side=LEFT)

        self.button_correction = Button(self.parameters_fr_correction, text="Сгенерировать",
                                        command=self.generate_correction)
        self.button_correction.pack(side=RIGHT)

    def generate_correction(self):
        """
        Функция отвечающая за кнопку 'Сгенерировать' параметров 'Коррекция на радиус'
        """

        parameters = {
            "value": self.field_entry_value.get(),
            "direction": self.field_choice_direction.get(),
        }

        input_text = self.get_input_text()
        if self.check_parameter(parameters):
            text = fun.generate_correction(input_text, parameters)
            self.field_output.insert(1.0, text)
        else:
            return

    def create_parameters_bias(self):
        """
        Создается фрейм с параметрами для вкладки "смещения".
        """
        self.parametrs_fr_bias = Frame(self.main_fr_bias)
        self.parametrs_fr_bias.pack(side=TOP, fill=BOTH, expand=True)

        # создаются X, Y, Z параметрами для смещения
        self.label_x = Label(self.parametrs_fr_bias, text="X")
        self.label_x.pack(side=LEFT)
        self.field_entry_x = Entry(self.parametrs_fr_bias)
        self.field_entry_x.config(justify=RIGHT)
        self.field_entry_x.pack(side=LEFT)
        self.field_entry_x.insert(1, "0")

        self.label_y = Label(self.parametrs_fr_bias, text="Y")
        self.label_y.pack(side=LEFT)
        self.field_entry_y = Entry(self.parametrs_fr_bias)
        self.field_entry_y.config(justify=RIGHT)
        self.field_entry_y.pack(side=LEFT)
        self.field_entry_y.insert(1, "0")

        self.label_z = Label(self.parametrs_fr_bias, text="Z")
        self.label_z.pack(side=LEFT)
        self.field_entry_z = Entry(self.parametrs_fr_bias)
        self.field_entry_z.config(justify=RIGHT)
        self.field_entry_z.pack(side=LEFT)
        self.field_entry_z.insert(1, "0")

        self.button_bias = Button(self.parametrs_fr_bias, text="Сгенерировать", command=self.generate_bias)
        self.button_bias.pack(side=RIGHT)

    def get_input_text(self):
        """Возвращает вводимый пользоветелм текст"""
        self.info_clear()
        self.field_output.delete(0.0, END)
        return self.field_input.get(1.0, END)

    def generate_bias(self):
        """
        Функция отвечающая за кнопку 'Сгенерировать' параметров 'Смещение'
        """

        parameters = {
            "X": self.field_entry_x.get(),
            "Y": self.field_entry_y.get(),
            "Z": self.field_entry_z.get(),
        }

        input_text = self.get_input_text()
        if self.check_parameter(parameters):
            text = fun.generate_bias(input_text, parameters)
            self.field_output.insert(1.0, text)
        else:
            return

    def info_clear(self):
        """Очистка инфо поля"""
        self.field_info.config(state="normal")
        self.field_info.delete(1.0, END)
        self.field_info.config(state="disabled")

    def check_parameter(self, parameters):
        """
        Проверка на валидность параметров.
        """
        # исключения
        exempt = [
            "direction",
            "device",
            "toolnum",
            "move_dimension",
            "working_offset",
            "version",
            "value_axis"
        ]

        for key, value in parameters.items():
            if key in exempt:
                continue
            if len(value) == 0:
                parameters[key] = 0
            try:
                parameters[key] = float(value)
            except ValueError:
                self.view_info(f"Параметр: {key} должен быть числом, введено - '{value}'")
                return False
        return True

    def create_input_output_fileds(self):
        """
        Создаются поля для вывода и ввода управляюще программы.
        """
        self.fr_input_output = Frame(self.window)
        self.fr_input_output.pack(side=TOP, fill=BOTH, expand=True)

        self.field_input = Text(self.fr_input_output, width=10)
        self.field_input.pack(side=LEFT, fill=BOTH, expand=True)

        self.field_output = Text(self.fr_input_output, width=10)
        self.field_output.pack(side=RIGHT, fill=BOTH, expand=True)

    def create_info_field(self):
        """Создается фрейм и поля для вывода сообщений"""

        self.fr_info = Frame(self.window)
        self.fr_info.pack(side=TOP, fill=BOTH, expand=True)

        self.field_info = Text(self.fr_info)
        self.field_info.config(state='disabled')
        self.field_info.pack(side=LEFT, fill=BOTH, expand=True)

    def view_info(self, message):
        """
        Вывод сообщений в поле инфо-поле
        """
        old_info = self.field_info.get(1., END)
        info = old_info + message
        self.field_info.config(state='normal')
        self.field_info.insert(1., info)
        self.field_info.config(state='disabled')

    def create_main_parameters(self, kinds_param):
        created_parameteres = {}
        for title, kind in kinds_param.items():
            if kind["type"] == "button":
                name_param = ["frame", "text", "command",]
                subp.check_exists_parameters(name_param, title, kind)

                created_parameteres[title] = Button(kind['frame'],
                                                    text=kind["text"],
                                                    command=kind["command"])
                created_parameteres[title].pack(side=LEFT, fill=BOTH, expand=True)
            elif kind["type"] == "entry":
                name_param = ["frame"]
                subp.check_exists_parameters(name_param, title, kind)
                created_parameteres[title] = Entry(kind["frame"])
                created_parameteres[title].pack(side=LEFT, fill=BOTH, expand=True)
                created_parameteres[title].config(justify=RIGHT)
                created_parameteres[title].insert(1, "0")
            elif kind["type"] == "combobox":
                name_param = ["frame", "values", "width", "current"]
                subp.check_exists_parameters(name_param, title, kind)

                created_parameteres[title] = ttk.Combobox(kind["frame"],
                                                          values=kind["values"],
                                                          width=kind["width"],
                                                          justify=RIGHT)
                created_parameteres[title].current(kind["current"])
                created_parameteres[title].pack(side=LEFT, fill=BOTH, expand=True)

            elif kind["type"] == "label":
                name_param = ["frame", "text"]
                subp.check_exists_parameters(name_param, title, kind)
                created_parameteres[title] = Label(kind["frame"], text=kind["text"])
                created_parameteres[title].pack(side=LEFT)
            else:
                print("Неизвестный тип поля")
        return created_parameteres






if __name__ == "__main__":
    app = App("800x600")
