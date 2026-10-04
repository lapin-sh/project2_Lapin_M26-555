"""Разбор аргументов команд: столбцы, значения и условия where и set."""


def convert_value(raw_value, type_name):
    """Приводит строковое значение к типу столбца."""
    if type_name == "int":
        try:
            return int(raw_value)
        except ValueError:
            raise TypeError(raw_value) from None
    if type_name == "bool":
        if raw_value == "true":
            return True
        if raw_value == "false":
            return False
        raise TypeError(raw_value)
    if len(raw_value) > 1 and raw_value[0] == raw_value[-1] and raw_value[0] in "\"'":
        return raw_value[1:-1]
    raise TypeError(raw_value)


def parse_columns(args):
    """Разбирает аргументы вида имя:тип в список пар."""
    columns = []
    for arg in args:
        name, _, type_name = arg.partition(":")
        if not name or not type_name:
            raise TypeError(arg)
        columns.append((name, type_name))
    return columns


def parse_values(raw):
    """Разбирает часть values: (значение1, значение2, ...) в список строк."""
    raw = raw.strip()
    if not (raw.startswith("(") and raw.endswith(")")):
        raise TypeError(raw)
    values = []
    for part in raw[1:-1].split(","):
        part = part.strip()
        if not part:
            raise TypeError(raw)
        values.append(part)
    return values


def parse_condition(raw, columns):
    """Разбирает условие вида столбец = значение в словарь."""
    column, sep, raw_value = raw.partition("=")
    column = column.strip()
    raw_value = raw_value.strip()
    if not sep or not column or not raw_value:
        raise TypeError(raw)
    schema = dict(columns)
    if column not in schema:
        raise KeyError(column)
    return {column: convert_value(raw_value, schema[column])}
