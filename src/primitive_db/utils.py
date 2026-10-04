"""Вспомогательные функции для работы с файлами."""

import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла, если файла нет - пустой словарь."""
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_table_data(table_name):
    """Загружает данные таблицы из файла data/<имя>.json."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(filepath, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет данные таблицы в файл data/<имя>.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def remove_table_data(table_name):
    """Удаляет файл с данными таблицы."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
