"""Генерирует demo.cast (asciinema-формат) без записи терминала."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
OUTPUT_FILE = PROJECT_ROOT / "demo.cast"

HEADER = {
    "version": 2,
    "width": 100,
    "height": 30,
    "timestamp": 1700000000,
    "env": {"SHELL": "/bin/bash", "TERM": "xterm-256color"},
}

# (время_сек, текст)
EVENTS = [
    (0.5, "$ uv run database\n"),
    (1.0, "\n***Операции с данными***\n"),
    (1.5, "Введите команду: "),
    (2.0, "create_table users name:str age:int is_active:bool\n"),
    (2.3, 'Таблица "users" успешно создана со столбцами: '
          "ID:int, name:str, age:int, is_active:bool\n"),
    (2.8, "\nВведите команду: "),
    (3.2, 'insert into users values ("Sergei", 28, True)\n'),
    (3.5, 'Запись с ID=1 успешно добавлена в таблицу "users".\n'),
    (3.7, "Функция insert выполнилась за 0.000 секунд.\n"),
    (4.2, "\nВведите команду: "),
    (4.6, "select from users\n"),
    (4.9, "Функция select выполнилась за 0.000 секунд.\n"),
    (5.1, "+----+--------+-----+-----------+\n"),
    (5.2, "| ID |  name  | age | is_active |\n"),
    (5.3, "+----+--------+-----+-----------+\n"),
    (5.4, "| 1  | Sergei | 28  |    True   |\n"),
    (5.5, "+----+--------+-----+-----------+\n"),
    (6.0, "\nВведите команду: "),
    (6.5, 'update users set age = 29 where name = "Sergei"\n'),
    (6.8, "Обновлено записей: 1.\n"),
    (7.3, "\nВведите команду: "),
    (7.8, 'select from users where name = "Sergei"\n'),
    (8.1, "Функция select выполнилась за 0.000 секунд.\n"),
    (8.3, "+----+--------+-----+-----------+\n"),
    (8.4, "| ID |  name  | age | is_active |\n"),
    (8.5, "+----+--------+-----+-----------+\n"),
    (8.6, "| 1  | Sergei | 29  |    True   |\n"),
    (8.7, "+----+--------+-----+-----------+\n"),
    (9.2, "\nВведите команду: "),
    (9.7, "delete from users where ID = 1\n"),
    (10.0, 'Вы уверены, что хотите выполнить "удаление записей"? [y/n]: '),
    (10.4, "y\n"),
    (10.7, "Удалено записей: 1.\n"),
    (11.2, "\nВведите команду: "),
    (11.7, "select from users\n"),
    (12.0, "Функция select выполнилась за 0.000 секунд.\n"),
    (12.2, "Записей нет.\n"),
    (12.7, "\nВведите команду: "),
    (13.2, "info users\n"),
    (13.5, "Таблица: users\n"),
    (13.6, "Столбцы: ID:int, name:str, age:int, is_active:bool\n"),
    (13.7, "Количество записей: 0\n"),
    (14.2, "\nВведите команду: "),
    (14.7, "drop_table users\n"),
    (15.0, 'Вы уверены, что хотите выполнить "удаление таблицы"? [y/n]: '),
    (15.4, "y\n"),
    (15.7, 'Таблица "users" успешно удалена.\n'),
    (16.2, "\nВведите команду: "),
    (16.7, "exit\n"),
]


def main():
    """Пишет demo.cast в корень проекта."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(json.dumps(HEADER, ensure_ascii=False) + "\n")
        for delay, text in EVENTS:
            f.write(json.dumps([delay, "o", text], ensure_ascii=False) + "\n")
    print(f"Создан: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()