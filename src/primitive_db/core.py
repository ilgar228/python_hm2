"""Ядро базы данных - управление таблицами"""

ALLOWED_TYPES = {"int", "str", "bool"}

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


def drop_table(metadata, table_name):
    """Удаляет таблицу из metadata.

    Если таблицы нет — печатает ошибку и возвращает metadata без изменений.
    """
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

