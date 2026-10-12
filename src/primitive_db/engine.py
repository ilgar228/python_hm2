"""Запуск, игровой цикл и парсинг команд."""

import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.constants import META_FILE
from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from primitive_db.decorators import create_cacher
from primitive_db.parser import parse_condition, parse_values
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def _print_table(table_data):
    """Печатает список записей через PrettyTable."""
    if not table_data:
        print("Записей нет.")
        return

    table = PrettyTable()
    table.field_names = list(table_data[0].keys())
    for row in table_data:
        table.add_row([row[key] for key in table.field_names])
    print(table)


def print_help():
    """Вывод текста с командами и описанием."""
    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> create_table <имя> <столбец:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя> - удалить таблицу")
    print("<command> insert into <имя> values (<значение1>, ...) - создать запись")
    print("<command> select from <имя> [where <столбец> = <значение>] - прочитать")
    print(
        "<command> update <имя> set <столбец> = <знач> "
        "where <столбец> = <знач> - обновить"
    )
    print("<command> delete from <имя> where <столбец> = <значение> - удалить запись")
    print("<command> info <имя> - информация о таблице")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """Главный цикл программы."""
    metadata = load_metadata(META_FILE)
    select_cache = create_cacher()

    while True:
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)

        if not args:
            continue

        command = args[0]

        if command == "exit":
            break

        elif command == "help":
            print_help()

        elif command == "create_table":
            if len(args) < 3:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILE, metadata)

        elif command == "list_tables":
            if not metadata:
                print("Таблиц нет.")
            else:
                for table in metadata:
                    print(f"- {table}")

        elif command == "drop_table":
            if len(args) < 2:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(META_FILE, metadata)
            select_cache = create_cacher()

        elif command == "insert":
            if len(args) < 5 or args[1] != "into" or args[3] != "values":
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[2]
            values = parse_values(args[4:])
            if values is None:
                continue
            data = insert(metadata, table_name, values)
            if data is not None:
                save_table_data(table_name, data)
                select_cache = create_cacher()

        elif command == "select":
            if len(args) < 3 or args[1] != "from":
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[2]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            if len(args) > 3:
                if args[3] != "where":
                    print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                    continue
                where_clause = parse_condition(args[4:])
                if where_clause is None:
                    continue
            else:
                where_clause = None

            key_part = tuple(sorted((where_clause or {}).items()))
            cache_key = (table_name, key_part)

            def fetch():
                data = load_table_data(table_name)
                return select(data, where_clause)

            result = select_cache(cache_key, fetch)
            _print_table(result)

        elif command == "update":
            if "set" not in args or "where" not in args:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue

            set_index = args.index("set")
            where_index = args.index("where")

            set_tokens = args[set_index + 1:where_index]
            where_tokens = args[where_index + 1:]

            set_clause = parse_condition(set_tokens)
            where_clause = parse_condition(where_tokens)
            if set_clause is None or where_clause is None:
                continue

            data = load_table_data(table_name)
            data = update(data, set_clause, where_clause)
            save_table_data(table_name, data)
            select_cache = create_cacher()

        elif command == "delete":
            if len(args) < 6 or args[1] != "from" or args[3] != "where":
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[2]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            where_clause = parse_condition(args[4:])
            if where_clause is None:
                continue

            data = load_table_data(table_name)
            data = delete(data, where_clause)
            save_table_data(table_name, data)
            select_cache = create_cacher()

        elif command == "info":
            if len(args) < 2:
                print(f"Некорректное значение: {user_input}. Попробуйте снова.")
                continue
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            schema = metadata[table_name]
            columns_str = ", ".join(f'{c["name"]}:{c["type"]}' for c in schema)
            data = load_table_data(table_name)
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {columns_str}")
            print(f"Количество записей: {len(data)}")

        else:
            print(f"Функции {command} нет. Попробуйте снова.")