"""Ядро базы данных - управление таблицами"""

import os

from primitive_db.constants import ALLOWED_TYPES, DATA_DIR
from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import load_table_data


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создаёт таблицу в metadata. Добавляет ID:int в начало.
    columns — список строк вида "имя:тип", например ["name:str", "age:int"].
    Возвращает обновлённый metadata (или исходный, если была ошибка).
    """
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    parsed_columns = []
    for column in columns:
        if ":" not in column:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
        name, type_ = column.split(":", 1)
        if type_ not in ALLOWED_TYPES:
            print(f"Некорректное значение: {column}. Попробуйте снова.")
            return metadata
        parsed_columns.append({"name": name, "type": type_})
    parsed_columns.insert(0, {"name": "ID", "type": "int"})
    metadata[table_name] = parsed_columns
    columns_str = ", ".join(f'{col["name"]}:{col["type"]}' for col in parsed_columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')
    return metadata


@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    """Удаляет таблицу из metadata и её файл данных.

    Если таблицы нет — печатает ошибку и возвращает metadata без изменений.
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]

    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    if os.path.exists(filepath):
        os.remove(filepath)

    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def _check_type(value, type_name):
    """Проверяет, что value соответствует типу type_name ('int', 'str', 'bool')."""
    if type_name == "bool":
        return isinstance(value, bool)
    if type_name == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "str":
        return isinstance(value, str)
    return False


@log_time
@handle_db_errors
def insert(metadata, table_name, values):
    """Добавляет запись в таблицу.

    Возвращает обновлённый список данных или None при ошибке.
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    schema = metadata[table_name]
    columns_without_id = schema[1:]

    if len(values) != len(columns_without_id):
        print(
            f"Ошибка: неверное количество значений. "
            f"Ожидалось {len(columns_without_id)}, получено {len(values)}."
        )
        return None

    for value, col in zip(values, columns_without_id):
        if not _check_type(value, col["type"]):
            print(
                f'Ошибка: значение "{value}" не соответствует типу '
                f'{col["type"]} для столбца "{col["name"]}".'
            )
            return None

    data = load_table_data(table_name)
    new_id = max((row["ID"] for row in data), default=0) + 1

    record = {"ID": new_id}
    for value, col in zip(values, columns_without_id):
        record[col["name"]] = value
    data.append(record)

    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return data


@log_time
@handle_db_errors
def select(table_data, where_clause=None):
    """Возвращает записи, подходящие под where_clause.

    where_clause — словарь вида {"age": 28}. Если None — возвращает все записи.
    """
    if where_clause is None:
        return table_data

    result = []
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if row.get(key) != value:
                match = False
                break
        if match:
            result.append(row)
    return result


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет записи, подходящие под where_clause, согласно set_clause.

    Возвращает обновлённый список данных.
    """
    updated_count = 0
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if row.get(key) != value:
                match = False
                break
        if match:
            for key, value in set_clause.items():
                row[key] = value
            updated_count += 1

    print(f"Обновлено записей: {updated_count}.")
    return table_data


@confirm_action("удаление записей")
@handle_db_errors
def delete(table_data, where_clause):
    """Удаляет записи, подходящие под where_clause.

    Возвращает обновлённый список данных.
    """
    result = []
    deleted_count = 0
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if row.get(key) != value:
                match = False
                break
        if match:
            deleted_count += 1
        else:
            result.append(row)

    print(f"Удалено записей: {deleted_count}.")
    return result