from tkinter import *
from tkinter import ttk
import controller.function as fun

class App:
    def __init__(self, parent):
        self.window = Tk()
        self.window.geometry(parent)
        self.window.title("NCEditor")
        self.create_notebook()
        self.create_parametrs_bias()
        self.create_input_output_fileds()
        self.create_info_field()
        self.window.mainloop()


    def create_notebook(self):
        """
        Создается фрейм с перечнем вкладок.
        """
        #создаем набор вкладок
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)

        # создаем фреймы
        self.main_fr_bias = ttk.Frame(self.notebook)
        self.main_fr_bias.pack(fill=BOTH, expand=True)

        # добавляем фреймы в качестве вкладок
        self.notebook.add(self.main_fr_bias, text="Смещение")

    def create_parametrs_bias(self):
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

        self.button = Button(self.parametrs_fr_bias, text="Сгенерировать", command=self.generate_bias)
        self.button.pack(side=RIGHT)


    def generate_bias(self):
        """
        Функция отвечающая за кнопку 'Сгенерировать' параметров 'Смещение'
        """
        input_text = self.field_input.get(1.0, END)
        self.info_clear()
        self.field_output.delete(0.0, END)

        parameters = {
            "X": self.field_entry_x.get(),
            "Y": self.field_entry_y.get(),
            "Z": self.field_entry_z.get(),
        }

        if self.check_parameter(parameters):
            text = fun.generate_bias(input_text, parameters)
            self.field_output.insert(1.0, input_text)
        else:
            return

    def info_clear(self):
        """Очистка инфо поля"""
        self.field_info.config(state="normal")
        self.field_info.delete(1.0, END)
        self.field_info.config(state="disabled")


    def check_parameter(self, parameters):
        """
        Проверка на валидность параметров
        """
        for key, value in parameters.items():
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
        self.fr_input_output = Frame(self.main_fr_bias)
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


if __name__ == "__main__":
    app = App("800x600")

