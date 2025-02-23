class InvalidPathError(Exception):
    """ When a path could never point to a file, e.g. missing .extension"""
    def __init__(self, file_path: str):
        message = f"The file path: \'{file_path}\' is an invalid file path!"
        super().__init__(message)


class FileEmptyError(Exception):
    def __init__(self, file_path: str):
        self.message = f"The file {file_path} is empty!"
        super(FileEmptyError, self).__init__(self.message)
