import os
import unittest


from file_operations_mn.path_string_utilities import parent_path, is_path_of_extension
from file_operations_mn.file_utilities_read import (count_file_lines, max_file_index_in_dir, files_in_dir,
                                                    file_exists, immediate_subdirs)
from file_operations_mn.file_utilities_write import trim_end_of_file_blank_line, make_blank_file, make_empty_file
from file_operations_mn.file_exceptions import InvalidPathError, FileEmptyError
from file_operations_mn.file_writers import CSV_Writer


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


class TestCSV_Writer(unittest.TestCase):
    test_path = "test_csv_writer.csv"

    def test_create_file_from_empty_1_line(self):
        data = [[str(i) for i in range(2)]]
        header = ["col1", "col2"]

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header)
            csv_writer.write(data)

            self.assertEqual(count_file_lines(self.test_path), 3)

            data_loaded = csv_writer.load_all()

            self.assertEqual(data, data_loaded)

    def test_create_file_from_empty_2_lines(self):
        data = [[str(i) for i in range(2)] for _ in range(2)]
        header = ["col1", "col2"]

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header)
            csv_writer.write(data)

            self.assertEqual(count_file_lines(self.test_path), 4)

            data_loaded = csv_writer.load_all()

            self.assertEqual(data, data_loaded)

    def test_append_lines(self):
        data_initial = [[str(i) for i in range(2)] for _ in range(2)]
        header = ("col1", "col2")

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header)
            csv_writer.write(data_initial)

            csv_writer.append_lines(data_initial)
            csv_writer.append_lines(data_initial)

            loaded_data = csv_writer.load_all()
            correct_data = data_initial*3
            print(correct_data)
            self.assertEqual(loaded_data, correct_data)

    def test_append_empty_lines_does_nothing(self):
        data = [[]]
        data_initial = [[str(i) for i in range(2)] for _ in range(2)]

        header = ("col1", "col2")

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header)
            csv_writer.write(data_initial)

            csv_writer.append_lines(data)
            csv_writer.append_lines(data)

            loaded_data = csv_writer.load_all()
            self.assertEqual(loaded_data, data_initial)
            self.assertEqual(count_file_lines(self.test_path), 4)

    def test_write_empty_lines_does_nothing_when_empty_file_exists(self):
        data = [[]]

        header = ("col1", "col2")

        with TestTeardownFile(self.test_path):
            with open(self.test_path, 'w') as file:
                file.write('')

            csv_writer = CSV_Writer(self.test_path, header)
            self.assertTrue(csv_writer.is_empty)
            csv_writer.write(data)

            self.assertTrue(csv_writer.is_empty)

    def test_write_empty_lines_does_not_create_file_when_no_file_exists(self):
        data = [[]]

        header = ("col1", "col2")

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header)
            csv_writer.write(data)

            self.assertFalse(file_exists(self.test_path))

    def test_no_header_csv_write_and_append(self):
        data_initial = [[str(i) for i in range(2)] for _ in range(2)]

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path)
            csv_writer.write(data_initial)

            loaded_data = csv_writer.load_all()
            self.assertEqual(data_initial, loaded_data)
            self.assertTrue(count_file_lines(self.test_path), 3)

            csv_writer.append_lines(data_initial)
            csv_writer.append_lines(data_initial)
            loaded_data = csv_writer.load_all()
            self.assertEqual(data_initial*3, loaded_data)
            self.assertTrue(count_file_lines(self.test_path), 5)

    def test_load_line_with_header(self):
        data_initial = [[str(i) for i in range(2)] for _ in range(2)]
        header = ("col1", "col2")

        # with TestTeardownFile(self.test_path):
        csv_writer = CSV_Writer(self.test_path, header)
        csv_writer.write(data_initial)

        with self.assertRaises(ValueError):
            csv_writer.load_line(2)

        loaded_line1 = csv_writer.load_line(0)
        loaded_line2 = csv_writer.load_line(1)

        self.assertEqual(loaded_line1, [data_initial[0]])
        self.assertEqual(loaded_line2, [data_initial[1]])

    def test_load_line_without_header(self):
        data_initial = [[str(i) for i in range(2)] for _ in range(2)]

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path)
            csv_writer.write(data_initial)

            with self.assertRaises(ValueError):
                csv_writer.load_line(2)

            loaded_line1 = csv_writer.load_line(0)
            loaded_line2 = csv_writer.load_line(1)

            self.assertEqual(loaded_line1, [data_initial[0]])
            self.assertEqual(loaded_line2, [data_initial[1]])

    def test_load_range_with_header(self):
        data_initial = [[str(i) for i in range(2)] for _ in range(3)]
        header = ("col1", "col2")

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header)
            csv_writer.write(data_initial)

            with self.assertRaises(ValueError):
                csv_writer.load_range(0, 4)

            loaded_range = csv_writer.load_range(0, 3)

            self.assertEqual(data_initial, loaded_range)

    def test_load_range_without_header(self):
        data_initial = [[str(i) for i in range(2)] for _ in range(3)]

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path)
            csv_writer.write(data_initial)

            with self.assertRaises(ValueError):
                csv_writer.load_range(0, 4)

            loaded_range = csv_writer.load_range(0, 3)

            self.assertEqual(data_initial, loaded_range)

    def test_load_sequential_without_header(self):
        data_initial0 = [[str(i) for i in range(2)] for _ in range(2)]
        data_initial1 = [['1', '2'] for _ in range(2)]
        data_initial = data_initial0 + data_initial1

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path)
            csv_writer.write(data_initial)

            loaded_data0 = csv_writer.load_sequential(2)
            loaded_data1 = csv_writer.load_sequential(2)
            loaded_data2 = csv_writer.load_sequential(1)

            self.assertEqual(loaded_data0, data_initial0)
            self.assertEqual(loaded_data1, data_initial1)
            self.assertEqual(loaded_data2, [['0', '1']])

    def test_load_sequential_with_header(self):
        data_initial0 = [[str(i) for i in range(2)] for _ in range(2)]
        data_initial1 = [['1', '2'] for _ in range(2)]
        data_initial = data_initial0 + data_initial1

        header = ("col1", "col2")

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header=header)
            csv_writer.write(data_initial)

            loaded_data0 = csv_writer.load_sequential(2)
            loaded_data1 = csv_writer.load_sequential(2)
            loaded_data2 = csv_writer.load_sequential(2)
            loaded_data3 = csv_writer.load_sequential(2)
            loaded_data4 = csv_writer.load_sequential(1)
            loaded_data5 = csv_writer.load_sequential(2)

            self.assertEqual(csv_writer._batch_index, 3)
            self.assertEqual(loaded_data0, data_initial0)
            self.assertEqual(loaded_data1, data_initial1)
            self.assertEqual(loaded_data2, data_initial0)
            self.assertEqual(loaded_data3, data_initial1)
            self.assertEqual(loaded_data4, [['0', '1']])
            self.assertEqual(loaded_data5, [['0', '1'], ['1', '2']])

    def test_auto_header(self):
        data_initial = [[str(i) for i in range(2)] for _ in range(2)]
        header = ["col1", "col2"]

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header)
            csv_writer.write(data_initial)

            csv_writer = CSV_Writer(self.test_path, "$auto")
            self.assertEqual(csv_writer.header, header)

    def test_auto_header_when_empty(self):
        with TestTeardownFile(self.test_path):
            make_empty_file(self.test_path)

            with self.assertRaises(FileEmptyError):
                CSV_Writer(self.test_path, "$auto")

    def test_single_column_create_and_append(self):
        data_initial = [[str(i) for i in range(2)]]
        header = ["col1"]

        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path, header)
            csv_writer.write(data_initial)

            csv_writer.append_lines(data_initial)
            csv_writer.append_lines(data_initial)

            loaded_data = csv_writer.load_all()
            correct_data = data_initial * 3
            print(correct_data)
            self.assertEqual(loaded_data, correct_data)

    def test_make_file_if_not_exists_makes_file_no_header(self):
        with TestTeardownFile(self.test_path):
            csv_writer = CSV_Writer(self.test_path)
            csv_writer.make_empty_file_if_not_exists()
            self.assertTrue(csv_writer.is_empty)

    def test_auto_header_with_no_file_raises_error(self):
        with TestTeardownFile(self.test_path):
            with self.assertRaises(FileNotFoundError):
                CSV_Writer(self.test_path, header="$auto")


class DirectoryFunctions(unittest.TestCase):
    def test_list_files_in_test_directory_correct(self):
        file_paths = files_in_dir("test_directory")
        correct_paths = ['1.txt', '3.txt', 'test_file1.txt']

        self.assertEqual(file_paths, correct_paths)

    def test_maximum_index_correct(self):
        correct_max_index = 3
        self.assertEqual(correct_max_index, max_file_index_in_dir("test_directory"))

    def test_immediate_subdirectories(self):
        self.assertEqual({x for x in immediate_subdirs("test_directory")}, {"sub_dir1", "sub_dir2"})


if __name__ == '__main__':
    unittest.main()
