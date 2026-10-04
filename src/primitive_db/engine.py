"""Основной цикл программы и обработка команд."""

import shlex

from primitive_db.constants import HELP_LINES, META_FILE, PROMPT
from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata


def print_help():
    """Печатает справку по командам."""
    for line in HELP_LINES:
        print(line)


def parse_columns(args):
    """Разбирает аргументы вида имя:тип в список пар."""
    columns = []
    for arg in args:
        name, _, type_name = arg.partition(":")
        if not name or not type_name:
            print(f"Некорректное значение: {arg}. Попробуйте снова.")
            return None
        columns.append((name, type_name))
    return columns


def handle_create_table(args):
    """Обрабатывает команду create_table."""
    if len(args) < 2:
        print(f"Некорректное значение: {' '.join(args)}. Попробуйте снова.")
        return
    columns = parse_columns(args[1:])
    if columns is None:
        return
    metadata = load_metadata(META_FILE)
    result = create_table(metadata, args[0], columns)
    if result is not None:
        save_metadata(META_FILE, result)


def handle_drop_table(args):
    """Обрабатывает команду drop_table."""
    if len(args) != 1:
        print(f"Некорректное значение: {' '.join(args)}. Попробуйте снова.")
        return
    metadata = load_metadata(META_FILE)
    result = drop_table(metadata, args[0])
    if result is not None:
        save_metadata(META_FILE, result)


def handle_list_tables():
    """Обрабатывает команду list_tables."""
    metadata = load_metadata(META_FILE)
    if not metadata:
        print("Таблиц нет")
        return
    for table_name in metadata:
        print(f"- {table_name}")


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
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
