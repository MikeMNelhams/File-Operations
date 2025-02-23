from file_operations_mn.file_exceptions import InvalidPathError

import os


def is_path_dir(dir_path: str) -> bool:
    if len(dir_path) == 0:
        return False
    return os.path.isdir(dir_path)


def path_parent_dir(file_path: str) -> str:
    return os.path.dirname(file_path)


def is_path_of_extension(file_path: str, extension: str= '.txt') -> bool:
    """ Only checks the string, not that file exists"""
    if len(extension) == 1:
        raise InvalidPathError(f"The extension \'{extension}\' is invalid.")

    if len(file_path) <= len(extension):
        return False

    if '.' not in extension:
        raise InvalidPathError(f"The extension \'{extension}\' is invalid.")

    if file_path[-len(extension):] != extension:
        return False
    return True


def file_path_without_extension(file_path: str) -> str:
    """ Does not read/write to the file in any way"""
    if '.' not in file_path or file_path[-1] == '.' or file_path[-2] == '.':
        raise InvalidPathError(file_path)

    stop_index = 0
    for i, character in enumerate(reversed(file_path)):
        if character == '.':
            stop_index = i + 1
            break

    return file_path[:-stop_index]


def parent_path(path: str, parent_num: int=1) -> str:
    if len(path) <= 1:
        raise InvalidPathError(path)

    parent_path_start = 0

    for i, char in enumerate(reversed(path)):
        if char == '/' or char == '\\':
            parent_path_start = i + 1
            break

    parent_path_str = path
    if parent_path_start != 0:
        parent_path_str = path[:-parent_path_start]

    if parent_num > 1:
        return parent_path(parent_path_str, parent_num - 1)

    return parent_path_str
