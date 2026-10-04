"""Декораторы и замыкание для кэширования запросов."""

import functools
import time


def handle_db_errors(func):
    """Перехватывает ошибки базы данных и печатает сообщение."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. "
                  "Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except TypeError as e:
            print(f"Некорректное значение: {e}. Попробуйте снова.")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

    return wrapper


def confirm_action(action_name):
    """Декоратор-фабрика: запрашивает подтверждение опасной операции."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
            if answer.strip().lower() != "y":
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Замеряет и печатает время выполнения функции."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result

    return wrapper


def create_cacher():
    """Создает кэш на замыкании для результатов запросов."""
    cache = {}

    def cache_result(key, value_func):
        """Возвращает результат по ключу, вычисляя его при первом обращении."""
        if key not in cache:
            cache[key] = value_func()
        return cache[key]

    return cache_result
