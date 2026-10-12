# primitive-db

Учебный проект: примитивная база данных с управлением таблицами.

## Установка

```bash
uv sync
```

## Запуск

```bash
uv run project
```

## Управление таблицами

После запуска доступны команды:

| Команда | Описание |
|---|---|
| `create_table <имя> <столбец:тип> ...` | Создать таблицу |
| `list_tables` | Показать список таблиц |
| `drop_table <имя>` | Удалить таблицу |
| `help` | Справка |
| `exit` | Выход |

Поддерживаемые типы данных: `int`, `str`, `bool`.

### Пример

```
>>> create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>> list_tables
- users

>>> drop_table users
Таблица "users" успешно удалена.
```

## CRUD-операции

После создания таблицы можно работать с данными:

| Команда | Описание |
|---|---|
| `insert into <имя> values (<знач1>, <знач2>, ...)` | Создать запись |
| `select from <имя>` | Показать все записи |
| `select from <имя> where <столбец> = <значение>` | Показать по условию |
| `update <имя> set <столбец> = <знач> where <столбец> = <знач>` | Обновить записи |
| `delete from <имя> where <столбец> = <значение>` | Удалить записи |
| `info <имя>` | Информация о таблице |

Строковые значения указываются в кавычках: `"Sergei"`. Числа и `True`/`False` — без кавычек.

### Пример

```
>>> create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>> insert into users values ("Sergei", 28, True)
Запись с ID=1 успешно добавлена в таблицу "users".

>>> select from users
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Sergei | 28  |    True   |
+----+--------+-----+-----------+

>>> update users set age = 29 where name = "Sergei"
Обновлено записей: 1.

>>> delete from users where ID = 1
Удалено записей: 1.

>>> info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 0
```