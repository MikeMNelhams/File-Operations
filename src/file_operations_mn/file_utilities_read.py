import os

from file_operations_mn.path_string_utilities import is_path_dir, file_path_without_extension, is_path_of_extension


def count_file_lines(file_path: str) -> int:
    with open(file_path, "r") as file:
        data = file.read()

    if len(data) == 0:
        return 1

    number_of_lines = sum(1 for line in data if line[-1] == '\n') + 1

    return number_of_lines


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


def files_in_dir(directory_path: str, extension: str = '.txt') -> list:
    child_file_paths = os.listdir(directory_path)
    return [file_path for file_path in child_file_paths if is_path_of_extension(file_path, extension=extension)]


def file_exists(file_path: str) -> bool:
    if len(file_path) == 0:
        return False
    if not os.path.isfile(file_path):
        return False
    if len(file_path) < 2:
        return False
    return True
