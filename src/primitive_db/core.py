"""Основная логика работы с таблицами."""

from primitive_db.constants import VALID_TYPES


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
