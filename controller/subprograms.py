from tkinter import *
from tkinter import ttk
import fileinput
from tkinter.filedialog import *
import sqlite3 as sq


def show_picture(field):
    """Показывает картинки подсказок."""

    keys_db = {
        "Направление измерения": 1,
        "Положение поверхности": 2,
        "Диаметр отверстия": 3,
        "Диаметр цилиндра": 4,
        "Относительное расстояние по Z цилиндра": 5,
        "Ось паза": 6,
        "Ширина паза": 7,
        "Ось выступа": 8,
        "Ширина выступа": 9,
        "Относительное расстояние по Z выступа": 10
    }

    con = sq.connect("C:\\python3.7\\NCEditor\\model\\model.db")
    cur = con.cursor()
    tmp = f"""SELECT path FROM pictures WHERE id == {keys_db[field["name"]]}"""
    cur.execute(tmp)
    path = cur.fetchone()[0]

    root = Tk()
    root.geometry("400x320")
    root.title(field["text"])
    canvas = Canvas(root, bg="white", height=320, width=400)
    canvas.pack()
    photo = PhotoImage(master=root, file=path)
    prhotIMG = canvas.create_image(200, 160, image=photo)
    root.mainloop()


def check_exists_parameters(param, title, kind):
    "Проверяет наличие параметров в полях ввода"
    for p in param:
        if p not in kind:
            print(f"Не введен параметр '{p}' в {title}")


def get_parameters(parameters, fields):
    """Получает и возвращает основные значения вводимые пользователем."""
    value_parameters = {}
    exception = ["value_number_programm"]

    for name, p in parameters.items():
        try:
            value_parameters[name] = p.get()
            try:
                if isinstance(p, Entry) and not isinstance(p, ttk.Combobox) and name not in exception:
                    value_parameters[name] = float(value_parameters[name])
            except ValueError:
                view_info(f"Параметр должен быть числом, введено - '{value_parameters[name]}'", fields)
                return False
        except AttributeError:
            continue
        except ValueError:
            continue
    return value_parameters


def view_info(message, fields):
    """
    Вывод сообщений в поле инфо-поле
    """
    old_info = fields["info"].get(1., END)
    info = old_info + message
    info_clear(fields)
    fields["info"].config(state='normal')
    fields["info"].insert(1., info)
    fields["info"].config(state='disabled')


def info_clear(fields):
    """Очистка инфо поля"""
    fields["info"].config(state="normal")
    fields["info"].delete(1.0, END)
    fields["info"].config(state="disabled")


def output_clear(fields):
    """Очистка поле вывода"""
    fields["output"].delete(1.0, END)


def get_input_text(fields):
    """Возвращает вводимый пользоветелем текст"""
    result = fields["input"].get(1.0, END)
    if result == "\n":
        view_info("Поле для ввода пустое...", fields)
        return False
    return fields["input"].get(1.0, END)


def clear_input_field(field):
    """Очистить поля ввода."""
    field["input"].delete(0., END)


def clear_output_field(field):
    """Очистить поле вывода."""
    field["output"].delete(0., END)


def open_file(fields):
    """Открывает файл для обработки."""
    open_a = askopenfilename()
    if open_a:
        fields["input"].delete(1., END)
        for i in fileinput.input(open_a):
            fields["input"].insert(END, i)


def save_file(fields):
    """Сохраняет полученный файл."""
    save = asksaveasfilename()
    if save:
        file = fields["output"].get(1.0, END)
        f = open(save, "w")
        f.write(file)
        f.close()
