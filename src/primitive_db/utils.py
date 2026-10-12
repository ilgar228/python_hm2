"""Вспм. функции: работа с файлами"""

import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла. Если файла нет — возвращает {}."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _data_path(table_name):
    """Возвращает путь к JSON-файлу с данными таблицы."""
    return os.path.join(DATA_DIR, f"{table_name}.json")


def load_table_data(table_name):
    """Загружает данные таблицы из data/<table_name>.json.
    Если файла нет — возвращает пустой список."""
    try:
        with open(_data_path(table_name), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    """Сохраняет данные таблицы в data/<table_name>.json."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_data_path(table_name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)