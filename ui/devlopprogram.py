from tkinter import *
from tkinter import ttk
import controller.subprograms as subp
import controller.devprogram as dp


class Program:
    def __init__(self, frame):
        self.frame = frame
        self.operation = ["Центрование", "Сверление", "Фрезерование", "Резьбофрезерование"]
        self.main_parameteres = {}
        self.count = Count(6)
        self.work_offset = ["Нет", "G54", "G55", "G56", "G57", "G58", "G59"] + [f"G54.1P{i}" for i in range(1, 99)]
        self.tool = ["без инструмента"] + [f"{i:02d}" for i in range(1, 41)]
        self.corrector_for_radius = ["Нет", "Левая", "Правая"]
        self.value_dimesion = ["попутное", "встречное"]


    def create_parameteres(self, parameteres):
        created_parameteres = {}
        for title, kind in parameteres.items():
            if kind["type"] == "label":
                name_param = ["frame", "text"]
                subp.check_exists_parameters(name_param, title, kind)
                created_parameteres[title] = Label(kind["frame"], text=kind["text"])
                created_parameteres[title].grid(row=self.count.srow(), column=self.count.scolumn())
            elif kind["type"] == "entry":
                name_param = ["frame"]
                subp.check_exists_parameters(name_param, title, kind)
                created_parameteres[title] = Entry(kind["frame"])
                created_parameteres[title].grid(row=self.count.srow(), column=self.count.scolumn())
                created_parameteres[title].config(justify=RIGHT)
                created_parameteres[title].insert(1, kind["default"])
            elif kind["type"] == "combobox":
                name_param = ["frame", "values", "width", "current"]
                subp.check_exists_parameters(name_param, title, kind)

                created_parameteres[title] = ttk.Combobox(kind["frame"],
                                                          values=kind["values"],
                                                          width=kind["width"],
                                                          justify=RIGHT)
                created_parameteres[title].current(kind["current"])
                created_parameteres[title].grid(row=self.count.srow(), column=self.count.scolumn())
            elif kind["type"] == "button":
                name_param = ["frame", "text", "command"]
                subp.check_exists_parameters(name_param, title, kind)
                created_parameteres[title] = Button(kind['frame'],
                                                    text=kind["text"],
                                                    command=kind["command"])
                created_parameteres[title].grid(row=self.count.srow(), column=self.count.scolumn())
            elif kind["type"] == "checkbutton":
                var = BooleanVar()
                created_parameteres[title] = Checkbutton(kind["frame"], variable=var, onvalue=1, offvalue=0)
                created_parameteres[title].grid(row=self.count.srow(), column=self.count.scolumn())
                created_parameteres[title] = var
        return created_parameteres

    def generate_program(self, name_op, *args):
        main_parameteres, fields, fields_center = args

        subp.info_clear(fields)
        subp.output_clear(fields)

        main_parameteres[name_op] = {**main_parameteres[name_op], **fields_center}
        parameteres = subp.get_parameters(main_parameteres[name_op], fields)

        if parameteres:
            text = dp.create(parameteres, fields, name_op)
            fields['output'].insert(1.0, "".join(text))


class Hole(Program):
    def __init__(self, frame):
        super().__init__(frame)

    def create(self, fields, fields_center):
        hole = {
            "diameter": dict(
                type="label",
                frame=self.frame,
                text="Диаметр:"),
            "value_diameter": dict(
                type="entry",
                default="10",
                frame=self.frame),
            "surface_coordinate": dict(
                type="label",
                frame=self.frame,
                text="Координата поверхности:"),
            "value_surface_coordinate": dict(
                type="entry",
                default="20",
                frame=self.frame),
            "depth": dict(
                type="label",
                frame=self.frame,
                text="Глубина:"),
            "value_depth": dict(
                type="entry",
                default="10",
                frame=self.frame, ),
            "step": dict(
                type="label",
                frame=self.frame,
                text="Шаг:"),
            "value_step": dict(
                type="entry",
                default="1",
                frame=self.frame),
            "operation": dict(
                type="label",
                frame=self.frame,
                text="Операция:"),
            "value_operation": dict(
                type="combobox",
                frame=self.frame,
                values=self.operation,
                width=17,
                current=0),
            "first_supply": dict(
                type="label",
                frame=self.frame,
                text="1ая координата подвода:"),
            "value_first_supply": dict(
                type="entry",
                default="25",
                frame=self.frame),
            "second_supply": dict(
                type="label",
                frame=self.frame,
                text="2ая координата подвода(R):"),
            "value_second_supply": dict(
                type="entry",
                default="2",
                frame=self.frame),
            "feed": dict(
                type="label",
                frame=self.frame,
                text="Подача:"),
            "value_feed": dict(
                type="entry",
                default="100",
                frame=self.frame),
            "rpm": dict(
                type="label",
                frame=self.frame,
                text="Обороты:"),
            "value_rmp": dict(
                type="entry",
                default="1000",
                frame=self.frame),
            "toolnum": dict(
                type="label",
                frame=self.frame,
                text="Номер инструмента:"),
            "value_toolnum": dict(
                type="combobox",
                frame=self.frame,
                values=self.tool,
                width=17,
                current=1),
            "name_field": dict(
                type="label",
                name="Рабочее смещение",
                frame=self.frame,
                text="Рабочее смещение"),
            "working_offset": dict(
                type="combobox",
                width=8,
                name="Рабочее смещение",
                frame=self.frame,
                values=self.work_offset,
                current=1),
            "corrector": dict(
                type="label",
                frame=self.frame,
                text="Коррекция на радиус:"),
            "value_corrector": dict(
                type="combobox",
                width=8,
                frame=self.frame,
                values=self.corrector_for_radius,
                current=0),
            "dimension": dict(
                type="label",
                frame=self.frame,
                text="Направление",),
            "value_dimension": dict(
                type="combobox",
                width=9,
                frame=self.frame,
                values=self.value_dimesion,
                current=0),
            "level": dict(
                type="label",
                frame=self.frame,
                text="С выходом на уровень:"),
            "value_level": dict(
                type="checkbutton",
                frame=self.frame),
            "programm": dict(
                type="label",
                frame=self.frame,
                text="Программа:"),
            "value_programm_on": dict(
                type="checkbutton",
                frame=self.frame,
                text="Программа"),
            "number_programm": dict(
                type="label",
                frame=self.frame,
                text="Номер программы:"),
            "value_number_programm": dict(
                type="entry",
                frame=self.frame,
                default="5001"),
            "generate": dict(
                type="label",
                frame=self.frame,
                text=""),
            "generate_hole": dict(
                type="button",
                frame=self.frame,
                text="Генерация",
                command=lambda: self.generate_program("hole", self.main_parameteres, fields, fields_center)),
        }

        self.main_parameteres["hole"] = self.create_parameteres(hole, )


class HolesCenters:
    def __init__(self, frame):
        self.frame = frame
        self.coordinates = {}

    def create(self, field):
        self.label_coordinate_x = Label(self.frame, text="Координата X:")
        self.label_coordinate_x.pack(side=LEFT, fill=BOTH, expand=True)

        self.coordinates["X"] = Entry(self.frame)
        self.coordinates["X"].pack(side=LEFT, fill=BOTH, expand=True, )
        self.coordinates["X"].config(justify=RIGHT)
        self.coordinates["X"].insert(1, "0")

        self.label_coordinate_y = Label(self.frame, text="Координата Y:")
        self.label_coordinate_y.pack(side=LEFT, fill=BOTH, expand=True)

        self.coordinates["Y"] = Entry(self.frame)
        self.coordinates["Y"].pack(side=LEFT, fill=BOTH, expand=True)
        self.coordinates["Y"].config(justify=RIGHT)
        self.coordinates["Y"].insert(1, "0")

        self.button_delete_one = Button(self.frame, text="Удалить",
                                        command=lambda: self.delete_hole(field))
        self.button_delete_one.pack(side=RIGHT)

        self.button_add_hole = Button(self.frame, text="Добавить",
                                      command=lambda: self.add_hole(self.coordinates, field))
        self.button_add_hole.pack(side=RIGHT)

        return self.coordinates

    def delete_hole(self, field):
        text = field["input"].get(0.0, END).split("\n")
        text = [i for i in text if i != ""]
        if len(text) != 0:
            text.pop(-1)
            field["input"].delete(1., END)
            field["input"].insert(1., "\n".join(text))

    def add_hole(self, parameteres, fields):

        parameteres = subp.get_parameters(parameteres, fields)

        if parameteres:
            old = fields["input"].get(0.0, END).split("\n")
            old.append(f'X{parameteres["X"]} Y{parameteres["Y"]}\n')
            old = [i for i in old if i != ""]
            fields["input"].delete(1., END)
            fields["input"].insert(1., "\n".join(old))


class Count:
    def __init__(self, max_row):
        self.multy = 1
        self.row = -1
        self.column = 1
        self.max_row = max_row

    def srow(self):
        if self.multy == 1:
            self.row += 1
        if self.row == self.max_row:
            self.row = 0
            self.column += 2
        return self.row

    def scolumn(self):
        self.multy *= -1
        self.column = self.column + self.multy
        return self.column
