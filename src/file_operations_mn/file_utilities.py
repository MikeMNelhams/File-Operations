import os
from pathlib import Path

from file_operations_mn.file_exceptions import InvalidPathError
from file_operations_mn.path_string_utilities import is_path_dir, is_path_of_extension, file_path_without_extension


def file_exists(file_path: str) -> bool:
    if len(file_path) == 0:
        return False
    if not os.path.isfile(file_path):
        return False
    if len(file_path) < 2:
        return False
    return True


def make_empty_file(file_path: str) -> None:
    """Use make_empty_file_safe if you don't want to overwrite data"""

    with open(file_path, "w") as outfile:
        outfile.write('')
    return None


def make_empty_file_safe(file_path: str) -> None:
    if os.path.isfile(file_path):
        raise FileExistsError
    make_empty_file(file_path)
    return None


def make_dir_if_not_exists(dir_path: str, parents=True) -> None:
    if is_path_dir(dir_path):
        return None

    if dir_path[-1] != '/':
        raise InvalidPathError

    Path(dir_path).mkdir(parents=parents, exist_ok=True)
    return None


def files_in_dir(directory_path: str, extension: str = '.txt') -> list:
    child_file_paths = os.listdir(directory_path)
    return [file_path for file_path in child_file_paths if is_path_of_extension(file_path, extension=extension)]


def max_file_index_in_dir(directory_path: str, extension_type: str = '.txt') -> int:
    """ Assuming all files are named: 1.[ext] 2.[ext] ETC for any given extension, find the max number index name"""
    assert is_path_dir(directory_path), NotADirectoryError
    child_file_paths = os.listdir(directory_path)
    file_names = [file_path_without_extension(file_path) for file_path in child_file_paths
                  if is_path_of_extension(file_path, extension=extension_type)]

    file_names = [int(file_name) for file_name in file_names if file_name.isnumeric()]
    if not file_names:
        return 0
    maximum_index = max(file_names)
    return maximum_index


def count_file_lines(file_path: str) -> int:
    with open(file_path, "r") as file:
        data = file.read()

    if len(data) == 0:
        return 1

    number_of_lines = sum(1 for line in data if line[-1] == '\n') + 1

    return number_of_lines


def trim_end_of_file_blank_line(file_path: str) -> None:
    with open(file_path, 'r') as in_file:
        data = in_file.read()

    with open(file_path, 'w') as out_file:
        out_file.write(data.rstrip('\n'))

    return None
