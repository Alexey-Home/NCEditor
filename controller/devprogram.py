import sqlite3 as sq
import controller.subprograms as subp
import re
from controller.renishaw import get_work_offset


def create(parameteres, fields, name):
    operations = {
        "hole": {
            "Центрование": 1,
            "Сверление": 2,
            "Фрезерование": 3,
            "Резьбофрезерование": 4}
    }
    text = []
    sample = get_sample(operations[name][parameteres["value_operation"]], name)

    parameteres["z"] = parameteres["value_surface_coordinate"] - abs(parameteres["value_depth"])
    parameteres["r"] = parameteres["value_surface_coordinate"] + abs(parameteres["value_second_supply"])
    parameteres["z1"] = parameteres["value_surface_coordinate"] + abs(parameteres["value_first_supply"])
    parameteres["radius"] = abs(parameteres["value_diameter"]/2)
    parameteres = get_corrector(parameteres)
    parameteres = get_level(parameteres)
    parameteres = get_begin_level(parameteres, fields)
    parameteres = get_dimension(parameteres)

    center_holes = subp.get_input_text(fields)
    center_holes = update_center_hole(center_holes)
    if parameteres["value_programm_on"]:
        text.append(get_begin_program(parameteres))
    text.append(calling_the_tool(parameteres))
    text.append(get_work_offset(parameteres))
    text.append(get_rmp(parameteres))

    if center_holes:
        text.append(get_tool_supply(parameteres, center_holes))
        text.append(get_lines_cycle(parameteres, sample, center_holes))
    else:
        text.append(get_tool_supply(parameteres, [(parameteres["X"], parameteres["Y"])]))
        text.append(get_lines_cycle(parameteres, sample, [(parameteres["X"], parameteres["Y"])]))
    if parameteres["value_programm_on"]:
        text.append(get_end_programm())
    return text


def get_begin_level(parameteres, fields):
    """Возвращает начальное положение режущего инструмента, при резьбофрезеровании."""
    z = parameteres["z"]
    surface = parameteres["value_surface_coordinate"]
    step = parameteres["value_step"]

    if z <= surface:
        while z <= surface:
            z += step
    else:
        subp.view_info("Конечная точка 'Z' больше чем начальная 'Координата поверхности'", fields)
        return False
    parameteres["value_begin_level"] = round(z, 2)
    return parameteres


def get_dimension(parameteres):
    """Возвращает команду - направления движения режущего инструмента."""

    if parameteres["value_dimension"] == "попутное":
        parameteres["value_dimension"] = "G03"
    else:
        parameteres["value_dimension"] = "G02"
    return parameteres


def get_rmp(parameteres):
    """Возвращает команду включения вращаения шпинделя"""
    return f"S{parameteres['value_rmp']}M3\n"


def get_lines_cycle(parameteres, sample, center_holes):
    """Возвращает цикл для обработки отверстий."""
    text = []
    for coordinate in center_holes:
        text.append(get_line(sample, parameteres, coordinate))
    else:
        if parameteres["value_operation"] in ["Центрование", "Сверление"]:
            text.append("G80\n")
    return "".join(text)


def update_center_hole(center_hole):
    """Возращает параметры центра отверстий, полученных из поля input."""
    if center_hole:
        coordinate = []
        reg_shaple = re.compile(r"X([0-9.+-]+)\s*Y([0-9.+-]+)")
        center_hole = center_hole.split("\n")
        for c in center_hole:
            if reg_shaple.findall(c):
                coordinate.append([float(i) for i in list(reg_shaple.findall(c)[0])])
        return coordinate
    else:
        return False


def get_corrector(parameteres):
    """Возвращает параметры коррекции на радиус."""
    if parameteres["value_corrector"] == "Левая":
        parameteres["value_corrector"] = f"G41D{parameteres['value_toolnum']}"
    elif parameteres["value_corrector"] == "Правая":
        parameteres["value_corrector"] = f"G42D{parameteres['value_toolnum']}"
    else:
        parameteres["value_corrector"] = ""
    return parameteres


def get_level(parameteres):
    """Возвращает параметры выводы режущего инструмента или нет."""
    if parameteres["value_level"]:
        parameteres["value_level"] = "G00Z#4\nEND1"
    else:
        parameteres["value_level"] = "#6=0\nEND1\nG00Z#4\n"
    return parameteres


def get_begin_program(parameteres):
    """Возвращает начало программы"""
    return f'%O{parameteres["value_number_programm"]}\nG91G30Z0.\n'


def get_tool_supply(parametrs, center_hole):
    """Вовзращает подвод режущего инструмента."""
    temp = ""
    if parametrs["value_toolnum"] != "без инструмента":
        temp = f"G43H{parametrs['value_toolnum']}"

    return f"G00X{center_hole[0][0]}Y{center_hole[0][1]}\n" \
           f"{temp}Z{parametrs['z1']}M8\n"


def calling_the_tool(parameteres):
    """Возвращает строку вызова инструмента."""
    if parameteres["value_toolnum"] == "без инструмента":
        return ""
    return f"M01\nG00G80G90G40G49G94\nT{parameteres['value_toolnum']}M6\n"


def get_line(sample, parameteres, coordinate):
    """Возвращает шаблон с подставленными параметрами..."""

    result = sample.format(coordinate[0],
                           coordinate[1],
                           parameteres["z"],
                           parameteres["value_second_supply"],
                           parameteres["value_feed"],
                           parameteres["value_step"],
                           parameteres["z1"],
                           parameteres["value_surface_coordinate"],
                           coordinate[0] + parameteres["radius"],
                           parameteres["radius"],
                           parameteres["value_corrector"],
                           parameteres["value_level"],
                           parameteres["value_begin_level"],
                           parameteres["value_dimension"])
    return result


def get_end_programm():
    """Возвращает конец программы."""
    return "M9\nM5\nG91G30Z0.\nM30\n%"


def get_sample(num, name):
    """Возращает шаблон, полученный с базы данных."""
    con = sq.connect("C:\\python3.7\\NCEditor\\model\\model.db")
    cur = con.cursor()
    tmp = f"""SELECT sample FROM {name} WHERE id == {num}"""
    cur.execute(tmp)
    sample = cur.fetchone()[0]
    return sample
