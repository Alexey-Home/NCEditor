import re


samples_bias = {
    "X": r"X[0-9+-.]+",
    "Y": r"Y[0-9+-.]+",
    "Z": r"Z[0-9+-.]+"
}


def generate_bias(text: str, parameters: dict) -> str:
    """
    Генерация смещения по x,y,z.
    :param text: текст управляющей прогаммы.
    :param parameters: величины смещения по координатам .
    :return: текст с подменными координатами.
    """
    text = text.split("\n")
    text_out = []
    for strng in text:
        for coord, sample in samples_bias.items():
            if re.compile(r"G28|G30|G29").findall(strng):
                continue
            if re.compile(sample).findall(strng):
                coordinate = re.compile(sample).findall(strng)[0]
                digit_coordinate = float(re.compile(r'[0-9+-.]+').findall(coordinate)[0])
                result_bias = "".join([coord, str(round(parameters[coord] + digit_coordinate, 3))])
                strng = re.compile(sample).sub(result_bias, strng)
        text_out.append(strng)
    return "\n".join(text_out)


samples_cor = {
    "line_interpoliacia": r"(G[0]?[0-3])",
    "X": r"(?<!\(.)X([0-9+-.]+)",
    "Y": r"(?<!\(.)Y([0-9+-.]+)",
    "Z": r"(?<!\(. )Z([0-9+-.]+)",
    "I": r"(?<!\(.)I([0-9+-.]+)",
    "J": r"(?<!\(.)J([0-9+-.]+)",
    "R": r"(?<!\(.)R([0-9+-.]+)",

}


def generate_correction(text: str, parameters: dict) -> str:
    """
    Генерация коррекции на радиус.
    :param text: текст управляющей прогаммы.
    :param parameters: величины и параметры коррекции на радиус.
    :return: текст с подменными координатами.
    """
    text = text.split("\n")
    dict_line = get_dict_line(text)

    points = get_point_trajectory(dict_line)


    for number_line, line in dict_line.items():
        print(f"Номер: {number_line}, Линия: {line}")
        

    return "\n".join(text)


def get_dict_line(text):
    """Получить словарь из координат и параметров"""
    dict_line = {}
    current = {
        "line_interpoliacia": "G01",
        "X": 0.,
        "Y": 0.,
        "Z": 350.,
        "I": 0.,
        "J": 0.,
        "R": 0.,
    }

    for line_number, strng in enumerate(text):
        trigger = False
        for command, sample in samples_cor.items():
            result = re.compile(sample).findall(strng)
            if result:
                current = get_current_command(command, current, result)
                trigger = True if command != "line_interpoliacia" else False
        if trigger:
            dict_line = update_dict_line(line_number, dict_line, current)
    return dict_line


def get_current_command(command, current, result):
    """Получает актуальные параметры."""
    current[command] = result[0]
    return current


def update_dict_line(line_number, dict_line, current):
    """
    Добавляет строчку в словарь с координатами.
    :param line_number: Номер сроки.
    :param dict_line: Словарь с траекториями.
    :param current: Актуальные параметры и координаты.
    :return: Словрь с координатами и параметрами.
    """
    parametrs = current.copy()
    dict_line[line_number] = parametrs
    return dict_line


def get_merge(lst):
    result = []
    for i in lst:
        for j in i:
            result.append(j)
    return result


