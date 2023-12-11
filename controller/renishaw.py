import re
import sqlite3 as sq



def create(parameters: dict, name_op):
    """
    Создание программы renishaw для привязки.
    :param paramateres: Вводимые параметры.
    :param name_op: Название операции.
    :return:
    """
    text = []
    number_operation = {
        "single_surface": 1,
        "hole": 2,
        "cylinder": 3,
        "groove": 4,
        "ledge": 5
    }
    function_operation = {

        "single_surface": [get_direction_of_measure,
                           get_surface_position,
                           get_working_offset],
        "hole": [get_diametr_hole,
                 get_working_offset],
        "cylinder": [get_diametr_hole,
                     get_height_measure,
                     get_working_offset],
        "groove": [get_axis_measure,
                   get_width,
                   get_working_offset],
        "ledge": [get_axis_measure,
                  get_width,
                  get_height_measure,
                  get_working_offset]
    }

    sample = get_sample(number_operation[name_op], parameters)
    text.append(calling_the_tool(parameters))
    text.append(get_work_offset(parameters))
    text.append(get_tool_supply(parameters))
    text.append(get_measure_on(parameters))
    text.append(get_measur_position(parameters))

    text.append(sample.format(*get_collection_argument(function_operation[name_op], parameters)))

    text.append(get_measur_position(parameters))
    text.append(get_end_programm())
    return text


def get_measure_on(parameters):
    measure_on = "M117"
    return f"{measure_on}\n"


def get_axis_measure(parameters):
    """Возвращает ось измерения."""
    if parameters["version"] == "новая":
        measure_axis = parameters["value_axis"]
        axis = {
            "X": "A1.",
            "Y": "A2.",
        }
        return f"{axis[measure_axis]}"
    else:
        return f"{parameters['value_axis']}"


def get_width(parameters):
    """Возвращает ширину."""
    if parameters["version"] == "новая":
        return f"D{abs(parameters['value_width'])}"
    else:
        return parameters["value_width"]


def get_height_measure(parameters):
    """Получить высоту измерения"""
    if parameters["version"] == "новая":
        return f"W-{abs(parameters['value_relative_distance'])}"
    else:
        hieght = abs(parameters['pos_h']) - abs(parameters['value_relative_distance'])
    return f"Z{hieght}"


def get_collection_argument(functions, parameters):
    """Собирает все значение аргументов"""
    collections = []
    for f in functions:
        collections.append(f(parameters))

    return collections


def get_work_offset(parametrs):
    """Возвращает "рабочее смещение координат". """
    if parametrs["working_offset"] == "Нет":
        return "G90\n"
    return f"G90{parametrs['working_offset']}\n"


def get_tool_supply(parametrs):
    """Вовзращает подвод режущего инструмента."""
    temp = ""
    if parametrs["toolnum"] != "без инструмента":
        temp = f"G43H{parametrs['toolnum']}"
    return f"G00X{parametrs['pos_x']}Y{parametrs['pos_y']}\n" \
           f"{temp}Z{parametrs['pos_z']}\n"


def calling_the_tool(parametrs):
    """Возвращает строку вызова инструмента."""
    if parametrs["toolnum"] == "без инструмента":
        return ""
    return f"M01\nG00G80G90G40G49G94\nT{parametrs['toolnum']}M6(RENISHAW)\n"


def get_measur_position(parameters):
    """Возвращает высоту измерения."""
    if "first_move" in parameters:
        return f"G65P9810Z{parameters['pos_z']}F500\n"
    parameters["first_move"] = True
    return f"G65P9810Z{parameters['pos_h']}F500\n"


def get_diametr_hole(parameters):
    """Возвращает диаметр измеряемого отверстия."""
    return f"D{parameters['value_diametr']}"


def get_end_programm():
    return "G91G30Z0.\n"


def get_surface_position(parameters):
    """
    Возвращает положение поверхности при одиночной поверхности.
    :param position: значенеи положение поверхности.
    :return:
    """
    position = parameters["value_coordinate"]
    if parameters["version"] == "новая":
        if position == 0:
            return ""
        return f"K{position}"
    else:
        return f"{parameters['move_dimension'][0]}{position}"


def get_direction_of_measure(parameters):
    """
    Возвращает значение "A" для 'направления измерения'.
    :param measure: Направление измерения выбраное пользователем.
    :return:
    """
    if parameters["version"] == "новая":
        measure = parameters["move_dimension"]

        direction_measure = {
            "X плюс": "A1.",
            "X минус": "A-1.",
            "Y плюс": "A2.",
            "Y минус": "A-2.",
            "Z минус": "A-3.",
        }

        return direction_measure[measure]
    else:
        return ""


def get_working_offset(paramaters):
    """
    Преобразование рабочего смещения.
    :param offset: рабочее смещение.
    :return:
    """
    offset = paramaters["working_offset"]
    if offset in ["G54", "G55", "G56", "G57", "G58", "G59"]:
        return f"S{offset[1:]}"
    elif offset == "Нет":
        return ""
    else:
        p = int(re.compile("P([0-9]+)").findall(offset)[0])
        return f"S1{p:02}"


def get_sample(num: int, parameters) -> str:
    """
    Получение шаблона Renishaw из базы данных
    :param num: id шаблона
    :return:
    """

    if parameters["version"] == "новая":
        table_v = "new_sample"
    else:
        table_v = "old_sample"

    con = sq.connect("C:\\python3.7\\NCEditor\\model\\model.db")
    cur = con.cursor()
    tmp = f"""SELECT {table_v} FROM GoProbe WHERE id == {num}"""
    cur.execute(tmp)
    sample = cur.fetchone()[0]
    return sample
