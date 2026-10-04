"""Разбор сложных частей команд: значения и условия where и set."""


def convert_value(raw_value, type_name):
    """Приводит строковое значение к типу столбца."""
    if type_name == "int":
        try:
            return int(raw_value)
        except ValueError:
            print(f"Некорректное значение: {raw_value}. Попробуйте снова.")
            return None
    if type_name == "bool":
        if raw_value == "true":
            return True
        if raw_value == "false":
            return False
        print(f"Некорректное значение: {raw_value}. Попробуйте снова.")
        return None
    if len(raw_value) > 1 and raw_value[0] == raw_value[-1] and raw_value[0] in "\"'":
        return raw_value[1:-1]
    print(f"Некорректное значение: {raw_value}. Попробуйте снова.")
    return None


def parse_values(raw):
    """Разбирает часть values: (значение1, значение2, ...) в список строк."""
    raw = raw.strip()
    if not (raw.startswith("(") and raw.endswith(")")):
        print(f"Некорректное значение: {raw}. Попробуйте снова.")
        return None
    values = []
    for part in raw[1:-1].split(","):
        part = part.strip()
        if not part:
            print(f"Некорректное значение: {raw}. Попробуйте снова.")
            return None
        values.append(part)
    return values


def parse_condition(raw, columns):
    """Разбирает условие вида столбец = значение в словарь."""
    column, sep, raw_value = raw.partition("=")
    column = column.strip()
    raw_value = raw_value.strip()
    if not sep or not column or not raw_value:
        print(f"Некорректное значение: {raw}. Попробуйте снова.")
        return None
    schema = dict(columns)
    if column not in schema:
        print(f"Ошибка: Таблица или столбец {column} не найден.")
        return None
    value = convert_value(raw_value, schema[column])
    if value is None:
        return None
    return {column: value}
