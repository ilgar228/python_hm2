"""Функции для разбора команд (where, set, values)."""


def _convert_value(raw):
    """Преобразует строковое значение к int, bool или str."""
    if raw == "True":
        return True
    if raw == "False":
        return False
    try:
        return int(raw)
    except ValueError:
        return raw


def parse_condition(tokens):
    """Разбирает токены вида ["age", "=", "28"] в словарь {"age": 28}.

    Возвращает None при ошибке формата.
    """
    if len(tokens) != 3 or tokens[1] != "=":
        print("Ошибка: неверный формат условия.")
        return None
    column = tokens[0]
    value = _convert_value(tokens[2])
    return {column: value}


def parse_values(args):
    """Разбирает секцию values (...) из токенов args.

    args — токены после "values", например ["(Sergei,", "28,", "True)"].
    Возвращает список значений или None при ошибке.
    """
    joined = " ".join(args)
    if not (joined.startswith("(") and joined.endswith(")")):
        print("Ошибка: значения должны быть в скобках.")
        return None

    inner = joined[1:-1].strip()
    if inner == "":
        return []

    raw_values = [v.strip() for v in inner.split(",")]
    return [_convert_value(v) for v in raw_values]