"""Основная логика работы с таблицами и данными."""

from primitive_db.constants import VALID_TYPES
from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.parser import convert_value


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает таблицу со столбцом ID и возвращает обновленные метаданные."""
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')
    for name, type_name in columns:
        if type_name not in VALID_TYPES:
            raise TypeError(f"{name}:{type_name}")
    if not any(name == "ID" for name, _ in columns):
        columns = [("ID", "int")] + list(columns)
    metadata[table_name] = columns
    columns_line = ", ".join(f"{name}:{type_name}" for name, type_name in columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_line}')
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных и возвращает их."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def get_table_columns(metadata, table_name):
    """Возвращает схему таблицы, если она существует."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')
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


@handle_db_errors
@log_time
def insert(metadata, table_name, table_data, raw_values):
    """Добавляет запись в таблицу и возвращает обновленные данные."""
    columns = get_table_columns(metadata, table_name)
    if len(raw_values) != len(columns) - 1:
        raise TypeError(", ".join(raw_values))
    record = {"ID": generate_id(table_data)}
    index = 0
    for name, type_name in columns:
        if name == "ID":
            continue
        record[name] = convert_value(raw_values[index], type_name)
        index += 1
    table_data.append(record)
    print(f'Запись с ID={record["ID"]} успешно добавлена в таблицу "{table_name}".')
    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает записи таблицы по условию."""
    if where_clause is None:
        return table_data
    rows = []
    for row in table_data:
        if matches(row, where_clause):
            rows.append(row)
    return rows


@handle_db_errors
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


@handle_db_errors
@confirm_action("удаление записи")
def delete(table_name, table_data, where_clause):
    """Удаляет записи по условию и возвращает обновленные данные."""
    remaining = []
    for row in table_data:
        if matches(row, where_clause):
            record_id = row["ID"]
            print(f'Запись с ID={record_id} '
                  f'успешно удалена из таблицы "{table_name}".')
        else:
            remaining.append(row)
    return remaining
