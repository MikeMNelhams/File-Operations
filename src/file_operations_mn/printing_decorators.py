from typing import Any


def load_print_decorator(func: callable) -> callable:
    type_return = Any

    try:
        type_return = func.__annotations__["return"]
    except KeyError:
        pass

    def wrapper(*args, **kwargs) -> type_return:
        file_path = args[0].file_path
        print('-'*80)
        print(f"Loading file: {file_path}")
        data = func(*args, **kwargs)
        print(f"Finished loading file: {file_path}")
        print('-'*80)
        return data
    return wrapper


def save_print_decorator(func: callable) -> callable:
    type_return = Any

    try:
        type_return = func.__annotations__["return"]
    except KeyError:
        pass

    def wrapper(*args, **kwargs) -> type_return:
        file_path = args[0].file_path
        print('-' * 80)
        print(f"Saving to file: {file_path}")
        data = func(*args, **kwargs)
        print(f"Finished saving to file: {file_path}")
        print('-' * 80)
        return data
    return wrapper
