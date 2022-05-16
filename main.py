import pickle
import re

SAVE_PERIOD = 10


def delete(db: dict, key: str) -> int:
    # Если значения нет, то возвращается 0, в
    # случае успешного выполнения возвращается
    # 1
    return 1 if (db.pop(key, None) is not None) else 0


def db_set(db: dict, key: str, val: str) -> None:
    # Если такой ключ уже существует, то значение
    # перезаписывается
    db[key] = val


def get(db: dict, key: str) -> str:
    # Если значения не существует, возвращается
    # null
    return db.get(key)


def keys(db_keys, expr: str) -> None:
    if expr == '*':
        correct_keys = db_keys
    elif expr[0] == '*' and expr[-1] == '*':
        expr = expr[1:-1]
        correct_keys = [key for key in db_keys if expr in key]
    elif expr[-1] == '*':
        expr = expr[:-1]
        correct_keys = [key for key in db_keys if key.startswith(expr)]
    elif expr[0] == '*':
        expr = expr[1:]
        correct_keys = [key for key in db_keys if key.endswith(expr)]
    else:
        correct_keys = [key for key in db_keys if key == expr]
    if len(correct_keys):
        print("Подходящие ключи:")
        for key in correct_keys:
            print(key)
    else:
        print("Нет подходящих ключей!")


if __name__ == '__main__':
    file_name = "db_save.pkl"
    file = open(file_name, "rb")
    try:
        db = pickle.load(file)
    except EOFError:
        db = {}
    file.close()
    flag = True
    counter = 0
    while flag:
        counter += 1
        print("Введите команду:")
        command = input(">> ").split()
        command[0] = command[0].lower()
        if counter == SAVE_PERIOD:
            file = open(file_name, "wb")
            pickle.dump(db, file)
            file.close()
            print("== База данных сохранена ==")
            counter = 0
        if command[0] == "exit":
            flag = False
            file = open(file_name, "wb")
            pickle.dump(db, file)
            file.close()
        elif command[0] == "flushall":
            db.clear()
            print("База данных удалена...")
        elif command[0] == "keys":
            try:
                keys(db.keys(), command[1])
            except IndexError:
                print("Вы не ввели выражение для поиска!")
        elif command[0] == "set":
            try:
                db_set(db, command[1], command[2])
            except IndexError:
                print("Вы не ввели ключ и/или значение")
        elif command[0] == "get":
            try:
                print(f"{command[1]}: {get(db, command[1])}")
            except IndexError:
                print("Вы не ввели ключ!")
        elif command[0] == "del":
            try:
                print(f"Ключ и значение удалены: {delete(db, command[1])}")
            except IndexError:
                print("Вы не ввели ключ!")
        elif command[0] == "help":
            print("KEYS * -- Получить список всех ключей по шаблону *\n"
                  "SET key value -- Установить значение по ключу\n"
                  "GET key -- Получить значение по ключу\n"
                  "DEL key -- Удалить ключ и значение по ключу\n"
                  "FLUSHALL -- Удалить все ключи и значения\n"
                  "HELP -- просмотреть список доступных команд\n"
                  "EXIT -- выйти из программы")
        else:
            print("Введена некорректная команда!\n"
                  "Для просмотра списка доступных команд, введите \"HELP\"\n")
