from abc import ABC, abstractmethod
import os
import json

from file_operations_mn.path_string_utilities import file_path_extension
from file_operations_mn.file_utilities_write import make_empty_file
from file_operations_mn.file_exceptions import InvalidPathError
from file_operations_mn.printing_decorators import save_print_decorator, load_print_decorator


class FileReader(ABC):
    def __init__(self, file_path: str, *args):
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
