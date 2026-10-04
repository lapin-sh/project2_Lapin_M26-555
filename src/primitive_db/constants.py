"""Константы проекта."""

META_FILE = "db_meta.json"
DATA_DIR = "data"
VALID_TYPES = ("int", "str", "bool")
PROMPT = ">>> Введите команду: "

HELP_LINES = [
    "",
    "***База данных***",
    "Функции:",
    "<command> create_table <имя> <столбец:тип> .. - создать таблицу",
    "<command> list_tables - показать список всех таблиц",
    "<command> drop_table <имя> - удалить таблицу",
    "<command> insert into <имя> values (<значение1>, ...) - создать запись",
    "<command> select from <имя> [where <столбец> = <значение>] - прочитать",
    "<command> update <имя> set <столбец> = <знач> where <столбец> = <знач> - обновить",
    "<command> delete from <имя> where <столбец> = <значение> - удалить запись",
    "<command> info <имя> - вывести информацию о таблице",
    "<command> exit - выход из программы",
    "<command> help - справочная информация",
    "",
]
