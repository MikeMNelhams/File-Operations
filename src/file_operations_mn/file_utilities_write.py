import os
from pathlib import Path

from file_operations_mn.file_exceptions import InvalidPathError
from file_operations_mn.path_string_utilities import is_path_dir


def trim_end_of_file_blank_line(file_path: str) -> None:
    with open(file_path, 'r') as in_file:
        data = in_file.read()

    with open(file_path, 'w') as out_file:
        out_file.write(data.rstrip('\n'))

    return None


def make_dir_if_not_exists(dir_path: str, parents=True) -> None:
    if is_path_dir(dir_path):
        return None

    if dir_path[-1] != '/':
        raise InvalidPathError(dir_path)

    Path(dir_path).mkdir(parents=parents, exist_ok=True)
    return None


def make_empty_file_safe(file_path: str) -> None:
    if os.path.isfile(file_path):
        raise FileExistsError
    make_empty_file(file_path)
    return None


def make_blank_file(file_path: str, num_lines_non_blank: int, num_lines_blank: int) -> None:
    if num_lines_non_blank == 0:
        lines = ['\n' for _ in range(num_lines_blank - 1)]

        with open(file_path, 'w') as out_file:
            out_file.writelines(lines)

        return None

    lines = ["test\n" for _ in range(num_lines_non_blank - 1)]
    if num_lines_non_blank > 1:
        lines += "test"

    if num_lines_blank > 0:
        lines += ['\n' for _ in range(num_lines_blank)]

    with open(file_path, 'w') as out_file:
        out_file.writelines(lines)

    return None


def make_empty_file(file_path: str) -> None:
    """Use make_empty_file_safe if you don't want to overwrite data"""

    with open(file_path, "w") as outfile:
        outfile.write('')
    return None
