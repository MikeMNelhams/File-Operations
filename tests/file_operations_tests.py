import os
import unittest


from file_operations_mn.path_string_utilities import parent_path, is_path_of_extension

from file_operations_mn.file_utilities_read import count_file_lines, max_file_index_in_dir, files_in_dir, file_exists
from file_operations_mn.file_utilities_write import trim_end_of_file_blank_line, make_blank_file

from file_operations_mn.file_exceptions import InvalidPathError


class TestTeardownFile:
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def __delete(self) -> None:
        if file_exists(self.__file_path):
            os.remove(self.__file_path)
        return None

    def __enter__(self):
        self.__delete()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__delete()


class TestFilePathOfExtension(unittest.TestCase):
    def test_txt_is_txt_returnTrue(self):
        self.assertTrue(is_path_of_extension("test.txt", ".txt"))

    def test_txt_is_csv_returnFalse(self):
        self.assertFalse(is_path_of_extension("test.txt", '.csv'))

    def test_csv_is_csv_returnTrue(self):
        self.assertTrue(is_path_of_extension("test.csv", '.csv'))

    def test_csv_is_txt_returnFalse(self):
        self.assertFalse(is_path_of_extension("test.csv", '.txt'))

    def test_empty_but_correct_extension_False(self):
        self.assertFalse(is_path_of_extension(".csv", ".csv"))

    def test_empty_and_incorrect_extension_False(self):
        self.assertFalse(is_path_of_extension(".txt", ".csv"))

    def test_has_csv_but_no_dot(self):
        self.assertFalse(is_path_of_extension("test_csv", ".csv"))

    def test_extension_to_check_has_no_dot(self):
        with self.assertRaises(InvalidPathError):
            is_path_of_extension("test.csv", "csv")

    def test_extension_is_only_dot_returns_path_error(self):
        with self.assertRaises(InvalidPathError):
            is_path_of_extension("test.", ".")


class TestCountLines(unittest.TestCase):
    def test_blank1(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 10, 2)
            self.assertEqual(12, count_file_lines(test_path))

    def test_blank2(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 10, 1)
            self.assertEqual(11, count_file_lines(test_path))

    def test_blank3(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 10, 0)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(10, count_file_lines(test_path))

    def test_blank4(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 1, 2)
            self.assertEqual(3, count_file_lines(test_path))

    def test_blank5(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 1, 1)
            self.assertEqual(2, count_file_lines(test_path))

    def test_blank6(self):
        test_path = "test.txt"

        # with TestTeardown(test_path):
        make_blank_file(test_path, 0, 1)
        self.assertEqual(1, count_file_lines(test_path))

    def test_blank7(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 0, 0)
            self.assertEqual(1, count_file_lines(test_path))

    def test_file_not_exists_raises_error(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            with self.assertRaises(FileNotFoundError):
                count_file_lines(test_path)


class TestTrimEmptyLines(unittest.TestCase):
    """ Relies on TestCountLines to pass all tests."""

    def test_blank1(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 10, 2)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(10, count_file_lines(test_path))

    def test_blank2(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 10, 1)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(10, count_file_lines(test_path))

    def test_blank3(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 10, 0)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(10, count_file_lines(test_path))

    def test_blank4(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 1, 2)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(1, count_file_lines(test_path))

    def test_blank5(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 1, 1)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(1, count_file_lines(test_path))

    def test_blank6(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 1, 0)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(1, count_file_lines(test_path))

    def test_blank7(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 0, 2)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(1, count_file_lines(test_path))

    def test_blank8(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 0, 1)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(1, count_file_lines(test_path))

    def test_blank9(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 0, 0)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(1, count_file_lines(test_path))

    def test_double_trim(self):
        test_path = "test.txt"

        with TestTeardownFile(test_path):
            make_blank_file(test_path, 10, 5)
            trim_end_of_file_blank_line(test_path)
            trim_end_of_file_blank_line(test_path)
            self.assertEqual(10, count_file_lines(test_path))


class TestParentDirPath(unittest.TestCase):
    def test_flat_file(self):
        test_path = "test_path.csv"
        self.assertEqual(parent_path(test_path), test_path)

    def test_single_nest_file(self):
        test_path = "test_dir/test_path.csv"
        self.assertEqual(parent_path(test_path), "test_dir")

    def test_double_nested_file_1_iter(self):
        test_path = "test_dir2/test_dir1/test_path.csv"
        self.assertEqual(parent_path(test_path), "test_dir2/test_dir1")

    def test_double_nested_file_2_iter(self):
        test_path = "test_dir2/test_dir1/test_path.csv"
        self.assertEqual(parent_path(test_path, 2), "test_dir2")

    def test_empty_path(self):
        test_path = ""
        with self.assertRaises(InvalidPathError):
            parent_path(test_path)


class DirectoryFunctions(unittest.TestCase):
    def test_list_files_in_test_directory_correct(self):
        file_paths = files_in_dir("test_directory")
        correct_paths = ['1.txt', '3.txt', 'test_file1.txt']

        self.assertEqual(file_paths, correct_paths)

    def test_maximum_index_correct(self):
        correct_max_index = 3
        self.assertEqual(correct_max_index, max_file_index_in_dir("test_directory"))


if __name__ == '__main__':
    unittest.main()
