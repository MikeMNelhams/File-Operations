import os
from pathlib import Path

from file_exceptions import InvalidPathError


def parent_dir(file_path: str) -> str:
    return os.path.dirname(file_path)


def file_exists(file_path: str) -> bool:
    if len(file_path) == 0:
        return False
    if not os.path.isfile(file_path):
        return False
    if len(file_path) < 2:
        return False
    return True


def is_dir(dir_path: str) -> bool:
    if len(dir_path) == 0:
        return False
    return os.path.isdir(dir_path)


def file_path_is_of_extension(file_path: str, extension: str= '.txt') -> bool:
    """ Only checks the string, not that file exists"""
    if len(file_path) <= len(extension):
        return False

    if '.' not in extension:
        raise ValueError(f"The extension \'{extension}\' is invalid.")

    if file_path[-len(extension):] != extension:
        return False
    return True


def file_path_without_extension(file_path: str) -> str:
    """ Does not read/write to the file in any way"""
    if '.' not in file_path:
        raise InvalidPathError
    if file_path[-1] == '.':
        raise InvalidPathError
    if file_path[-2] == '.':
        raise InvalidPathError

    stop_index = 0
    for i, character in enumerate(reversed(file_path)):
        if character == '.':
            stop_index = i + 1
            break

    return file_path[:-stop_index]


def make_dir_if_not_exists(dir_path: str, parents=True) -> None:
    if is_dir(dir_path):
        return None

    if dir_path[-1] != '/':
        raise InvalidPathError

    Path(dir_path).mkdir(parents=parents, exist_ok=True)
    return None
