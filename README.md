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