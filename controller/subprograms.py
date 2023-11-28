from tkinter import *
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

    con = sq.connect("model/model.db")
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


def get_main_parameters(parameters):
    """Получает и возвращает основные значения вводимые пользователем."""
    value_parameters = {}
    for name, p in parameters.items():
        try:
            value_parameters[name] = p.get()
        except AttributeError:
            continue
    return value_parameters
