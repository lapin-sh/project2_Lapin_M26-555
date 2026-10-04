"""Основная логика работы с таблицами и данными."""

from primitive_db.constants import VALID_TYPES
from primitive_db.parser import convert_value


def create_table(metadata, table_name, columns):
    """Создает таблицу со столбцом ID и возвращает обновленные метаданные."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None
    for name, type_name in columns:
        if type_name not in VALID_TYPES:
            print(f"Некорректное значение: {name}:{type_name}. Попробуйте снова.")
            return None
    if not any(name == "ID" for name, _ in columns):
        columns = [("ID", "int")] + list(columns)
    metadata[table_name] = columns
    columns_line = ", ".join(f"{name}:{type_name}" for name, type_name in columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_line}')
    return metadata


def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных и возвращает их."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def get_table_columns(metadata, table_name):
    """Возвращает схему таблицы, если она существует."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None
    return metadata[table_name]


def generate_id(table_data):
    """Вычисляет ID для новой записи."""
    if not table_data:
        return 1
    return max(row["ID"] for row in table_data) + 1


def matches(row, where_clause):
    """Проверяет, подходит ли запись под условие."""
    for column, value in where_clause.items():
        if row[column] != value:
            return False
    return True


def insert(metadata, table_name, table_data, raw_values):
    """Добавляет запись в таблицу и возвращает обновленные данные."""
    columns = get_table_columns(metadata, table_name)
    if columns is None:
        return None
    if len(raw_values) != len(columns) - 1:
        print(f"Некорректное значение: {', '.join(raw_values)}. Попробуйте снова.")
        return None
    record = {"ID": generate_id(table_data)}
    index = 0
    for name, type_name in columns:
        if name == "ID":
            continue
        value = convert_value(raw_values[index], type_name)
        if value is None:
            return None
        record[name] = value
        index += 1
    table_data.append(record)
    print(f'Запись с ID={record["ID"]} успешно добавлена в таблицу "{table_name}".')
    return table_data


def select(table_data, where_clause=None):
    """Возвращает записи таблицы по условию."""
    if where_clause is None:
        return table_data
    rows = []
    for row in table_data:
        if matches(row, where_clause):
            rows.append(row)
    return rows


def update(table_name, table_data, set_clause, where_clause):
    """Обновляет записи по условию и возвращает измененные данные."""
    for row in table_data:
        if matches(row, where_clause):
            for column, value in set_clause.items():
                row[column] = value
            record_id = row["ID"]
            print(f"Запись с ID={record_id} в таблице "
                  f'"{table_name}" успешно обновлена.')
    return table_data


def delete(table_name, table_data, where_clause):
    """Удаляет записи по условию и возвращает обновленные данные."""
    remaining = []
    for row in table_data:
        if matches(row, where_clause):
            print(f'Запись с ID={row["ID"]} успешно удалена из таблицы "{table_name}".')
        else:
            remaining.append(row)
    return remaining
