"""Основной цикл программы и обработка команд."""

import shlex

from prettytable import PrettyTable

from primitive_db.constants import HELP_LINES, META_FILE, PROMPT
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    get_table_columns,
    insert,
    select,
    update,
)
from primitive_db.decorators import create_cacher, handle_db_errors
from primitive_db.parser import parse_columns, parse_condition, parse_values
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    remove_table_data,
    save_metadata,
    save_table_data,
)

cacher = create_cacher()


def reset_cache():
    """Сбрасывает кэш запросов после изменения данных."""
    global cacher
    cacher = create_cacher()


def print_help():
    """Печатает справку по командам."""
    for line in HELP_LINES:
        print(line)


def print_table(columns, rows):
    """Печатает записи в виде таблицы."""
    table = PrettyTable()
    for name, _ in columns:
        values = []
        for row in rows:
            values.append(row[name])
        table.add_column(name, values)
    print(table)


def handle_create_table(args):
    """Обрабатывает команду create_table."""
    if len(args) < 2:
        print(f"Некорректное значение: {' '.join(args)}. Попробуйте снова.")
        return
    columns = parse_columns(args[1:])
    metadata = load_metadata(META_FILE)
    result = create_table(metadata, args[0], columns)
    if result is not None:
        save_metadata(META_FILE, result)
        reset_cache()


def handle_drop_table(args):
    """Обрабатывает команду drop_table."""
    if len(args) != 1:
        print(f"Некорректное значение: {' '.join(args)}. Попробуйте снова.")
        return
    metadata = load_metadata(META_FILE)
    result = drop_table(metadata, args[0])
    if result is not None:
        save_metadata(META_FILE, result)
        remove_table_data(args[0])
        reset_cache()


def handle_list_tables():
    """Обрабатывает команду list_tables."""
    metadata = load_metadata(META_FILE)
    if not metadata:
        print("Таблиц нет")
        return
    for table_name in metadata:
        print(f"- {table_name}")


def handle_insert(user_input):
    """Обрабатывает команду insert into."""
    parts = user_input.split(" values ", 1)
    header = parts[0].split()
    if len(parts) != 2 or len(header) != 3 or header[1] != "into":
        print(f"Некорректное значение: {user_input}. Попробуйте снова.")
        return
    table_name = header[2]
    raw_values = parse_values(parts[1])
    metadata = load_metadata(META_FILE)
    data = load_table_data(table_name)
    result = insert(metadata, table_name, data, raw_values)
    if result is not None:
        save_table_data(table_name, result)
        reset_cache()


@handle_db_errors
def handle_select(user_input):
    """Обрабатывает команду select from."""
    parts = user_input.split(" where ", 1)
    header = parts[0].split()
    if len(header) != 3 or header[1] != "from":
        raise TypeError(user_input)
    table_name = header[2]
    metadata = load_metadata(META_FILE)
    columns = get_table_columns(metadata, table_name)
    where_clause = None
    if len(parts) == 2:
        where_clause = parse_condition(parts[1], columns)
    data = load_table_data(table_name)
    cache_key = (table_name, str(where_clause))
    rows = cacher(cache_key, lambda: select(data, where_clause))
    print_table(columns, rows)


@handle_db_errors
def handle_update(user_input):
    """Обрабатывает команду update."""
    parts = user_input.split(" set ", 1)
    if len(parts) != 2:
        raise TypeError(user_input)
    header = parts[0].split()
    if len(header) != 2:
        raise TypeError(user_input)
    table_name = header[1]
    set_raw, _, where_raw = parts[1].partition(" where ")
    if not where_raw:
        raise TypeError(user_input)
    metadata = load_metadata(META_FILE)
    columns = get_table_columns(metadata, table_name)
    set_clause = parse_condition(set_raw, columns)
    where_clause = parse_condition(where_raw, columns)
    data = load_table_data(table_name)
    result = update(table_name, data, set_clause, where_clause)
    if result is not None:
        save_table_data(table_name, result)
        reset_cache()


@handle_db_errors
def handle_delete(user_input):
    """Обрабатывает команду delete from."""
    parts = user_input.split(" where ", 1)
    header = parts[0].split()
    if len(parts) != 2 or len(header) != 3 or header[1] != "from":
        raise TypeError(user_input)
    table_name = header[2]
    metadata = load_metadata(META_FILE)
    columns = get_table_columns(metadata, table_name)
    where_clause = parse_condition(parts[1], columns)
    data = load_table_data(table_name)
    result = delete(table_name, data, where_clause)
    if result is not None:
        save_table_data(table_name, result)
        reset_cache()


@handle_db_errors
def handle_info(args):
    """Обрабатывает команду info."""
    if len(args) != 1:
        raise TypeError(" ".join(args))
    table_name = args[0]
    metadata = load_metadata(META_FILE)
    columns = get_table_columns(metadata, table_name)
    data = load_table_data(table_name)
    columns_line = ", ".join(f"{name}:{type_name}" for name, type_name in columns)
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {columns_line}")
    print(f"Количество записей: {len(data)}")


def run():
    """Основной цикл программы."""
    print_help()
    while True:
        try:
            user_input = input(PROMPT)
        except EOFError:
            break
        args = shlex.split(user_input)
        if not args:
            continue
        command = args[0]
        if command == "help":
            print_help()
        elif command == "exit":
            break
        elif command == "create_table":
            handle_create_table(args[1:])
        elif command == "drop_table":
            handle_drop_table(args[1:])
        elif command == "list_tables":
            handle_list_tables()
        elif user_input.startswith("insert into"):
            handle_insert(user_input)
        elif user_input.startswith("select from"):
            handle_select(user_input)
        elif command == "update":
            handle_update(user_input)
        elif user_input.startswith("delete from"):
            handle_delete(user_input)
        elif command == "info":
            handle_info(args[1:])
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
