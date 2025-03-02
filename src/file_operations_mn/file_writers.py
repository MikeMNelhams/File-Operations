from abc import ABC, abstractmethod
import os
import json
import csv

from typing import Iterable

from file_operations_mn.path_string_utilities import file_path_extension, is_path_of_extension
from file_operations_mn.file_utilities_read import count_file_lines
from file_operations_mn.file_utilities_write import make_empty_file, make_empty_file_safe
from file_operations_mn.file_exceptions import InvalidPathError, FileEmptyError
from file_operations_mn.printing_decorators import save_print_decorator, load_print_decorator

import warnings


class FileReader(ABC):
    def __init__(self, file_path: str, *args, **kwargs):
        self.file_path = file_path

    @property
    def exists(self) -> bool:
        return os.path.isfile(self.file_path)

    @property
    def is_empty(self) -> bool:
        return os.stat(self.file_path).st_size == 0

    def touch_with_prompt_warning(self) -> None:
        user_response = input(f"Are you sure you want to possibly overwrite \'{self.file_path}\' to make an empty file? Y/N?: ")
        if user_response.lower() == 'n':
            print(f"Ok. Aborting overwriting file: \'{self.file_path}\'.")
            return None
        with open(self.file_path, 'a'):
            os.utime(self.file_path, None)
        return None

    def touch_no_prompt(self) -> None:
        with open(self.file_path, 'a'):
            os.utime(self.file_path, None)
        return None

    @abstractmethod
    @save_print_decorator
    def save(self, data) -> None:
        raise NotImplementedError

    @abstractmethod
    @load_print_decorator
    def load(self):
        raise NotImplementedError


class JSON_FileReader(FileReader):
    def __init__(self, file_path: str):
        super(JSON_FileReader, self).__init__(file_path)

    def save(self, data: dict) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return None

    def load(self) -> dict:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data


class TXT_FileReader(FileReader):
    def save(self, lines: list[str]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    def load(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content


class TextWriterSingleLine(FileReader):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        if not self.exists:
            make_empty_file(file_path)

    def load(self) -> str:
        file_extension = file_path_extension(self.file_path)
        if file_extension == ".txt":
            return self.__load_text()
        raise InvalidPathError(self.file_path)

    @load_print_decorator
    def load_safe(self):
        if not self.exists:
            return None

        return self.load()

    def save(self, data: str) -> None:
        assert hasattr(data, "__repr__")
        file_extension = file_path_extension(self.file_path)
        if file_extension == ".txt":
            self.__save_text(str(data))
        return None

    def __load_text(self) -> str:
        with open(self.file_path, "r") as text_file:
            data = text_file.read()
        return data

    def __save_text(self, data) -> None:
        with open(self.file_path, "w") as text_file:
            text_file.write(data)
        return None


class CSV_Writer(FileReader):
    """ I made this because I can't stand how files die when there is or isn't an empty line at EOF"""

    def __init__(self, file_path: str, header: Iterable = None, delimiter='|', *args, **kwargs):
        super().__init__(file_path, *args, **kwargs)
        self.__assert_is_csv(file_path)
        self.file_path = file_path
        self.delimiter = delimiter
        self.header = header

        if header == '$auto':
            if len(self) <= 1:
                raise FileEmptyError(self.file_path)
            self.header = None
            self.header = self.load_line(0)[0]

        self._batch_index = 0

    def __len__(self):
        # Remove 1, due to the empty line @ EOF.
        return count_file_lines(self.file_path) - 1

    def load(self, delimiter=',') -> list[list[str]]:
        with open(self.file_path, 'r') as file:
            lines = [x for x in csv.reader(file, delimiter=delimiter)]
        return lines

    def save(self, data: list[list[str]]) -> None:
        with open(self.file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        return None

    @load_print_decorator
    def load_line(self, line_number: int) -> list:
        """ For efficiently loading a specific line number """

        self.__assert_valid_line_number(line_number)

        line_increment = 1 if self.header is not None else 0

        with open(self.file_path, "r") as file:
            content = [self.__parse_row(x) for i, x in enumerate(file) if i == line_number + line_increment]

        return content

    @load_print_decorator
    def load_range(self, start_index: int, end_index: int) -> list[list]:
        if start_index == end_index:
            return self.load_line(start_index)

        line_increment = 1 if self.header is not None else 0

        self.__assert_valid_line_number(start_index, end_index - 1)
        # Makes use of early stopping AND known list memory allocation.
        with open(self.file_path, "r") as file:
            lower_limit = start_index + line_increment
            upper_limit = end_index + line_increment
            content = [[] for _ in range(start_index, end_index)]
            for i, x in enumerate(file):
                if i >= upper_limit:
                    break
                if i >= lower_limit:
                    content[i - line_increment - start_index] = self.__parse_row(x)

        return content

    @load_print_decorator
    def load_sequential(self, batch_size: int, from_start=False) -> list[list]:
        if from_start:
            self._batch_index = 0

        line_increment = 1 if self.header is not None else 0

        if batch_size > len(self) - line_increment:
            raise ValueError

        start_index = self._batch_index
        end_index = self._batch_index + batch_size

        overlap = False
        if end_index > len(self) - line_increment:
            overlap = True
            end_index = len(self) - line_increment

        content1 = self.load_range(start_index, end_index)

        if overlap:
            end_index_wrapped = batch_size - (len(self) - line_increment - start_index)

            content2 = self.load_range(0, end_index_wrapped)

            self._batch_index = end_index_wrapped
            return content1 + content2

        if end_index >= len(self) - line_increment:
            self._batch_index = 0
        else:
            self._batch_index = end_index

        return content1

    @load_print_decorator
    def load_all(self, safe=True, as_float=False) -> list:
        if safe and not self.exists:
            raise FileNotFoundError

        return self.__load_as_list(as_float=as_float)

    @save_print_decorator
    def write(self, data: Iterable) -> None:
        assert isinstance(data, Iterable), TypeError
        file_extension = file_path_extension(self.file_path)
        if file_extension == ".csv":
            self.__save(data)
        return None

    def make_empty_file_if_not_exists(self) -> None:
        if not self.exists:
            if self.header is None:
                make_empty_file_safe(self.file_path)
                return None
            with open(self.file_path, 'w', newline='', encoding="utf-8") as file:
                csv_writer = csv.writer(file, delimiter=self.delimiter)
                csv_writer.writerow(self.header)
        return None

    def append_lines(self, lines: list) -> None:
        if not self.exists or self.is_empty:
            self.__save(lines)
        else:
            if self.__lines_are_empty(lines):
                return None

            with open(self.file_path, 'a') as file:
                for line in lines:
                    file.write(self.delimiter.join(line) + '\n')
        return None

    def remove_last_line(self) -> None:
        if len(self) == 0:
            warnings.warn("File is empty, cannot remove empty line")
            return None

        with open(self.file_path, 'r') as text_file:
            content = text_file.readlines()

        with open(self.file_path, 'w') as text_file:
            text_file.writelines(content[:-1])

        return None

    def __load_as_list(self, as_float=False) -> list:
        with open(self.file_path, 'r') as file:
            csv_reader = csv.reader(file, delimiter=self.delimiter)
            if self.header is not None:
                next(csv_reader)

            if as_float:
                data = [[float(element) for element in row] for row in csv_reader]
            else:
                data = [row for row in csv_reader]
        return data

    def __save(self, lines: list) -> None:
        if self.__lines_are_empty(lines):
            return None

        rows_to_write = [*lines]
        if self.header is not None:
            rows_to_write = [list(self.header)] + rows_to_write

        with open(self.file_path, 'w', newline='', encoding="utf-8") as file:
            csv_writer = csv.writer(file, delimiter=self.delimiter)
            csv_writer.writerows(rows_to_write)
        return None

    @staticmethod
    def __assert_is_csv(file_path) -> None:
        assert is_path_of_extension(file_path, '.csv'), InvalidPathError
        return None

    @staticmethod
    def __lines_are_empty(lines: list[list]) -> bool:
        if sum([1 for line in lines if not line]) > 0:
            warnings.warn("Do not try to write an empty list.")
            return True
        return False

    def __assert_valid_line_number(self, *line_numbers: int) -> None:
        assert self.exists and not self.is_empty, FileNotFoundError(self.file_path)
        maximum_line_number = len(self) - 1 if self.header is None else len(self) - 2
        for line_number in line_numbers:
            if line_number < 0 or line_number > maximum_line_number:
                print(f'Invalid line {line_number}')
                raise ValueError
        return None

    def __parse_row(self, row: str) -> list:
        return row[:-1].split(self.delimiter)
