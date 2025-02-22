class InvalidPathError(Exception):
    """ When a path could never point to a file, e.g. missing .extension"""
    def __init__(self, file_path: str):
        message = f"The file path: \'{file_path}\' is an invalid file path!"
        super().__init__(message)