import controller.subprograms as subp
import controller.renishaw as ren
from tkinter import *
from tkinter import ttk


class Renishaw:
    def __init__(self, frame):
        self.frame = frame
        self.created_field = {}
        self.work_offset = ["Нет", "G54", "G55", "G56", "G57", "G58", "G59"] + [f"G54.1P{i}" for i in range(1, 99)]

    def generate_program(self, name_op, args):
        main_parameteres, sub_parameteres, fields = args

        subp.info_clear(fields)
        subp.output_clear(fields)

        main_param = subp.get_parameters(main_parameteres[name_op], fields)
        sub_param = subp.get_parameters(sub_parameteres, fields)

        if main_param and sub_param:
            parameters = {**main_param, **sub_param}
            text = ren.create(parameters, name_op)
            fields['output'].insert(1.0, "".join(text))


    def create_main_parameters(self, kinds_param):
        created_parameteres = {}
        for title, kind in kinds_param.items():
            if kind["type"] == "button":
                name_param = ["frame", "text", "command", ]
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


class Ledge(Renishaw):
    def __init__(self, frame):
        super().__init__(frame)
        self.axis = ["X", "Y"]

    def create(self, *args):
        main_parameteres = args[0]
        ledge = {
            "axis": dict(type="button",
                         text="Ось:",
                         name="Ось выступа",
                         frame=self.frame,
                         command=lambda: subp.show_picture(ledge["axis"])
                         ),
            "value_axis": dict(type="combobox",
                               name="Значение оси",
                               frame=self.frame,
                               values=self.axis,
                               width=5,
                               current=0
                               ),
            "width": dict(type="button",
                          text="Ширина:",
                          name="Ширина выступа",
                          frame=self.frame,
                          command=lambda: subp.show_picture(ledge["width"])),
            "value_width": dict(type="entry",
                                frame=self.frame,
                                name="Значение ширины"),
            "relative_distance": dict(type="button",
                                      text="Отн.расстояние по Z:",
                                      name="Относительное расстояние по Z выступа",
                                      frame=self.frame,
                                      command=lambda: subp.show_picture(ledge["relative_distance"])),
            "value_relative_distance": dict(type="entry",
                                            name="Значение отн.расстояния по Z",
                                            frame=self.frame),
            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=self.frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=7,
                                   name="Рабочее смещение",
                                   frame=self.frame,
                                   values=self.work_offset,
                                   current=1),
            "generate_groove": dict(type="button",
                                    text="Сгенерировать",
                                    name="Генерация",
                                    frame=self.frame,
                                    command=lambda: self.generate_program("ledge", args)),

        }
        main_parameteres["ledge"] = self.create_main_parameters(ledge)
        return main_parameteres


class Groove(Renishaw):
    def __init__(self, frame):
        super().__init__(frame)
        self.axis = ["X", "Y"]

    def create(self, *args):
        main_parameteres = args[0]
        groove = {
            "axis": dict(type="button",
                         text="Ось:",
                         name="Ось паза",
                         frame=self.frame,
                         command=lambda: subp.show_picture(groove["axis"])
                         ),
            "value_axis": dict(type="combobox",
                               name="Значение оси",
                               frame=self.frame,
                               values=self.axis,
                               width=5,
                               current=0
                               ),
            "width": dict(type="button",
                          text="Ширина:",
                          name="Ширина паза",
                          frame=self.frame,
                          command=lambda: subp.show_picture(groove["width"])),
            "value_width": dict(type="entry",
                                frame=self.frame,
                                name="Значение ширины"),
            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=self.frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=self.frame,
                                   values=self.work_offset,
                                   current=1),
            "generate_groove": dict(type="button",
                                    text="Сгенерировать",
                                    name="Генерация",
                                    frame=self.frame,
                                    command=lambda: self.generate_program("groove", args))

        }

        main_parameteres["groove"] = self.create_main_parameters(groove)
        return main_parameteres


class SingleSurface(Renishaw):
    def __init__(self, frame):
        super().__init__(frame)
        self.coordinate_dimension = ["X плюс", "X минус", "Y плюс", "Y минус", "Z минус"]


    def create(self, *args):
        """
        Создает параметры для renishaw - одиночная поверхность.
        """

        main_parameteres = args[0]

        single_surface = {
            "direct_measure": dict(type="button",
                                   text="Направление измерения:",
                                   name="Направление измерения",
                                   frame=self.frame,
                                   command=lambda: subp.show_picture(single_surface["direct_measure"])),
            "move_dimension": dict(type="combobox",
                                   name="Направление движения",
                                   frame=self.frame,
                                   values=self.coordinate_dimension,
                                   width=5,
                                   current=1),

            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=self.frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=self.frame,
                                   values=self.work_offset,
                                   current=1),
            "surface_position": dict(type="button",
                                     text="Положение поверхности:",
                                     name="Положение поверхности",
                                     frame=self.frame,
                                     command=lambda: subp.show_picture(single_surface["surface_position"])),
            "value_coordinate": dict(type="entry",
                                     name="Значение положение поверхности",
                                     frame=self.frame),
            "generate_hole": dict(type="button",
                                  text="Сгенерировать",
                                  name="Генерация",
                                  frame=self.frame,
                                  command=lambda: self.generate_program("single_surface", args)),

        }

        main_parameteres["single_surface"] = self.create_main_parameters(single_surface)
        return main_parameteres


class Hole(Renishaw):
    def __init__(self, frame):
        super().__init__(frame)

    def create(self, *args):
        main_parameteres = args[0]
        hole = {
            "diametr_hole": dict(type="button",
                                 text="Диаметр:",
                                 name="Диаметр отверстия",
                                 frame=self.frame,
                                 command=lambda: subp.show_picture(hole["diametr_hole"])),
            "value_diametr": dict(type="entry",
                                  name="Значение диаметра",
                                  frame=self.frame),
            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=self.frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=self.frame,
                                   values=self.work_offset,
                                   current=1),
            "generate_surface": dict(type="button",
                                     text="Сгенерировать",
                                     name="Генерация",
                                     frame=self.frame,
                                     command=lambda: self.generate_program("hole", args)),
        }

        main_parameteres["hole"] = self.create_main_parameters(hole)
        return main_parameteres


class Cylinder(Renishaw):
    def __init__(self, frame):
        super().__init__(frame)

    def create(self, *args):
        main_parameteres = args[0]
        cylinder = {
            "diametr_cylinder": dict(type="button",
                                     text="Диаметр:",
                                     name="Диаметр цилиндра",
                                     frame=self.frame,
                                     command=lambda: subp.show_picture(cylinder["diametr_cylinder"])),
            "value_diametr": dict(type="entry",
                                  name="Значение диаметра",
                                  frame=self.frame),
            "relative_distance": dict(type="button",
                                      text="Отн.расстояние по Z:",
                                      name="Относительное расстояние по Z цилиндра",
                                      frame=self.frame,
                                      command=lambda: subp.show_picture(cylinder["relative_distance"])),
            "value_relative_distance": dict(type="entry",
                                            name="Значение отн.расстояния по Z",
                                            frame=self.frame),
            "name_field": dict(type="label",
                               name="Рабочее смещение",
                               frame=self.frame,
                               text="Рабочее смещение"),
            "working_offset": dict(type="combobox",
                                   width=5,
                                   name="Рабочее смещение",
                                   frame=self.frame,
                                   values=self.work_offset,
                                   current=1),
            "generate_surface": dict(type="button",
                                     text="Сгенерировать",
                                     name="Генерация",
                                     frame=self.frame,
                                     command=lambda: self.generate_program("cylinder", args)),
        }

        main_parameteres["cylinder"] = self.create_main_parameters(cylinder)
        return main_parameteres


class SubParameteres():
    def __init__(self, frame):
        self.frame_sub_parameters = frame
        self.sub_parameteres = {}

    def create_sub_parameters(self):
        """
        Создает дополнительные параметры для renishaw.
        """

        tool_number = ["без инструмента"] + [f"{i:02d}" for i in range(1, 41)]
        devices = ["fanuc"]
        version_pogramm = ["новая", "старая"]

        self.frame_param_1 = Frame(self.frame_sub_parameters)
        self.frame_param_1.pack(side=LEFT, fill=BOTH, expand=True)

        self.frame_param_2 = Frame(self.frame_sub_parameters)
        self.frame_param_2.pack(side=LEFT, fill=BOTH, expand=True)

        self.label_position_x = Label(self.frame_param_1, text="Нач. положение X:", justify=LEFT)
        self.label_position_x.grid(row=0, column=0)

        self.sub_parameteres["pos_x"] = Entry(self.frame_param_1)
        self.sub_parameteres["pos_x"].config(justify=RIGHT)
        self.sub_parameteres["pos_x"].insert(1, "0")
        self.sub_parameteres["pos_x"].grid(row=0, column=1)

        self.label_position_y = Label(self.frame_param_1, text="Нач. положение Y:")
        self.label_position_y.grid(row=1, column=0)
        self.sub_parameteres["pos_y"] = Entry(self.frame_param_1)
        self.sub_parameteres["pos_y"].config(justify=RIGHT)
        self.sub_parameteres["pos_y"].insert(1, "0")
        self.sub_parameteres["pos_y"].grid(row=1, column=1)

        self.label_position_z = Label(self.frame_param_1, text="Нач. положение Z:")
        self.label_position_z.grid(row=2, column=0)
        self.sub_parameteres["pos_z"] = Entry(self.frame_param_1)
        self.sub_parameteres["pos_z"].config(justify=RIGHT)
        self.sub_parameteres["pos_z"].insert(1, "150")
        self.sub_parameteres["pos_z"].grid(row=2, column=1)

        self.label_position_h = Label(self.frame_param_1, text="Высота измерения:")
        self.label_position_h.grid(row=3, column=0)
        self.sub_parameteres["pos_h"] = Entry(self.frame_param_1)
        self.sub_parameteres["pos_h"].config(justify=RIGHT)
        self.sub_parameteres["pos_h"].insert(1, "100")
        self.sub_parameteres["pos_h"].grid(row=3, column=1)

        self.label_device = Label(self.frame_param_2, text="Устройство ЧПУ:")
        self.label_device.grid(row=0, column=0)
        self.sub_parameteres["device"] = ttk.Combobox(self.frame_param_2, values=devices, justify=RIGHT)
        self.sub_parameteres["device"].current(0)
        self.sub_parameteres["device"].grid(row=0, column=1)

        self.label_tool = Label(self.frame_param_2, text="Номер инструмента:")
        self.label_tool.grid(row=1, column=0)
        self.sub_parameteres["toolnum"] = ttk.Combobox(self.frame_param_2, values=tool_number, justify=RIGHT)
        self.sub_parameteres["toolnum"].current(40)
        self.sub_parameteres["toolnum"].grid(row=1, column=1)

        self.label_version_shample = Label(self.frame_param_2, text="Версия программы:")
        self.label_version_shample.grid(row=2, column=0)
        self.sub_parameteres["version"] = ttk.Combobox(self.frame_param_2, values=version_pogramm, justify=RIGHT)
        self.sub_parameteres["version"].current(0)
        self.sub_parameteres["version"].grid(row=2, column=1)

        return self.sub_parameteres
