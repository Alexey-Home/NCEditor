from tkinter import *
import controller.function as fun
import controller.subprograms as subp


class Bias:
    def __init__(self, frame):
        self.frame = frame
        self.parameteres = {}

    def create(self, fields):
        """
        Создается фрейм с параметрами для вкладки "смещения".
        """
        self.parametrs_fr_bias = Frame(self.frame)
        self.parametrs_fr_bias.pack(side=TOP, fill=BOTH, expand=True)

        # создаются X, Y, Z параметрами для смещения
        self.label_x = Label(self.parametrs_fr_bias, text="X")
        self.label_x.pack(side=LEFT)
        self.parameteres["X"] = Entry(self.parametrs_fr_bias)
        self.parameteres["X"].config(justify=RIGHT)
        self.parameteres["X"].pack(side=LEFT)
        self.parameteres["X"].insert(1, "0")

        self.label_y = Label(self.parametrs_fr_bias, text="Y")
        self.label_y.pack(side=LEFT)
        self.parameteres["Y"] = Entry(self.parametrs_fr_bias)
        self.parameteres["Y"].config(justify=RIGHT)
        self.parameteres["Y"].pack(side=LEFT)
        self.parameteres["Y"].insert(1, "0")

        self.label_z = Label(self.parametrs_fr_bias, text="Z")
        self.label_z.pack(side=LEFT)
        self.parameteres["Z"] = Entry(self.parametrs_fr_bias)
        self.parameteres["Z"].config(justify=RIGHT)
        self.parameteres["Z"].pack(side=LEFT)
        self.parameteres["Z"].insert(1, "0")

        self.button_bias = Button(self.parametrs_fr_bias, text="Сгенерировать",
                                  command=lambda: self.generate_bias(fields))
        self.button_bias.pack(side=RIGHT)

    def generate_bias(self, fields):
        """
        Функция отвечающая за кнопку 'Сгенерировать' параметров 'Смещение'
        """
        subp.info_clear(fields)
        subp.output_clear(fields)

        parameteres = subp.get_parameters(self.parameteres, fields)
        input_text = subp.get_input_text(fields)

        if parameteres and input_text:
            text = fun.generate_bias(input_text, parameteres)
            fields["output"].insert(1.0, text)


