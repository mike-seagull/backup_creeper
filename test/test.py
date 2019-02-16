import unittest
from datetime import datetime
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "src"))
from backup_creeper import *


class TestBackupsToKeep(unittest.TestCase):
    def test_normal_run(self):
        backups = ['2018-07-24', '2018-07-23', '2018-07-15', '2017-01-15', '2017-05-05', '2018-05-05', '2018-03-04', '2018-06-04', '2016-01-13']
        backups = convert_all_datestrings_in_list_to_datetime(backups)
        backups_to_keep = find_backups_to_keep(backups, datetime(2018, 7, 24))
        backups.sort()
        backups_to_keep.sort()
        correct_backups_to_keep = ['2017-05-05', '2018-05-05', '2018-06-04', '2018-07-15', '2018-07-23', '2018-07-24']
        correct_backups_to_keep = convert_all_datestrings_in_list_to_datetime(correct_backups_to_keep)
        correct_backups_to_keep.sort()
        self.assertEqual(backups_to_keep, correct_backups_to_keep)

    def test_first_run(self):
        backups = [
            '2018-07-08', '2018-07-09', '2018-07-10', '2018-07-11', '2018-07-12', '2018-07-13',
            '2018-07-14', '2018-07-15', '2018-07-16', '2018-07-17', '2018-07-18', '2018-07-19',
            '2018-07-20', '2018-07-21', '2018-07-22', '2018-07-23', '2018-07-24'
        ]
        backups = convert_all_datestrings_in_list_to_datetime(backups)
        backups_to_keep = find_backups_to_keep(backups, datetime(2018, 7, 24))
        backups.sort()
        backups_to_keep.sort()
        correct_backups_to_keep = [
            '2018-07-11', '2018-07-12', '2018-07-13', '2018-07-14', '2018-07-15', '2018-07-16', '2018-07-17',
            '2018-07-18', '2018-07-19', '2018-07-20', '2018-07-21', '2018-07-22', '2018-07-23', '2018-07-24'
        ]
        correct_backups_to_keep = convert_all_datestrings_in_list_to_datetime(correct_backups_to_keep)
        correct_backups_to_keep.sort()
        self.assertEqual(backups_to_keep, correct_backups_to_keep)

    def test_first_end_of_month_save(self):
        backups = [
            '2018-07-31',
            '2018-08-01', '2018-08-02', '2018-08-03', '2018-08-04', '2018-08-05', '2018-08-06', '2018-08-07',
            '2018-08-08', '2018-08-09', '2018-08-10', '2018-08-11', '2018-08-12', '2018-08-13', '2018-08-14'
        ]
        backups = convert_all_datestrings_in_list_to_datetime(backups)
        backups_to_keep = find_backups_to_keep(backups, datetime(2018, 8, 14))
        backups.sort()
        backups_to_keep.sort()
        correct_backups_to_keep = [
            '2018-07-31',
            '2018-08-01', '2018-08-02', '2018-08-03', '2018-08-04', '2018-08-05', '2018-08-06', '2018-08-07',
            '2018-08-08', '2018-08-09', '2018-08-10', '2018-08-11', '2018-08-12', '2018-08-13', '2018-08-14'
        ]
        correct_backups_to_keep = convert_all_datestrings_in_list_to_datetime(correct_backups_to_keep)
        correct_backups_to_keep.sort()
        self.assertEqual(backups_to_keep, correct_backups_to_keep)

    def test_4th_end_of_month_save(self):
        backups = [
            '2018-07-31', '2018-08-31', '2018-09-30', '2018-10-31',
            '2018-11-01', '2018-11-02', '2018-11-03', '2018-11-04', '2018-11-05', '2018-11-06', '2018-11-07',
            '2018-11-08', '2018-11-09', '2018-11-10', '2018-11-11', '2018-11-12', '2018-11-13', '2018-11-14'
        ]
        backups = convert_all_datestrings_in_list_to_datetime(backups)
        backups_to_keep = find_backups_to_keep(backups, datetime(2018, 11, 14))
        backups.sort()
        backups_to_keep.sort()
        correct_backups_to_keep = [
            '2018-08-31', '2018-09-30', '2018-10-31',
            '2018-11-01', '2018-11-02', '2018-11-03', '2018-11-04', '2018-11-05', '2018-11-06', '2018-11-07',
            '2018-11-08', '2018-11-09', '2018-11-10', '2018-11-11', '2018-11-12', '2018-11-13', '2018-11-14'
        ]
        correct_backups_to_keep = convert_all_datestrings_in_list_to_datetime(correct_backups_to_keep)
        correct_backups_to_keep.sort()
        self.assertEqual(backups_to_keep, correct_backups_to_keep)

    def test_1st_end_of_year_save(self):
        backups = [
            '2018-12-31', '2019-01-31', '2019-02-28', '2019-03-31',
            '2019-04-01', '2019-04-02', '2019-04-03', '2019-04-04', '2019-04-05', '2019-04-06', '2019-04-07',
            '2019-04-08', '2019-04-09', '2019-04-10', '2019-04-11', '2019-04-12', '2019-04-13', '2019-04-14'
        ]
        backups = convert_all_datestrings_in_list_to_datetime(backups)
        backups_to_keep = find_backups_to_keep(backups, datetime(2019, 4, 14))
        backups.sort()
        backups_to_keep.sort()
        correct_backups_to_keep = [
            '2018-12-31', '2019-01-31', '2019-02-28', '2019-03-31',
            '2019-04-01', '2019-04-02', '2019-04-03', '2019-04-04', '2019-04-05', '2019-04-06', '2019-04-07',
            '2019-04-08', '2019-04-09', '2019-04-10', '2019-04-11', '2019-04-12', '2019-04-13', '2019-04-14'
        ]
        correct_backups_to_keep = convert_all_datestrings_in_list_to_datetime(correct_backups_to_keep)
        correct_backups_to_keep.sort()
        self.assertEqual(backups_to_keep, correct_backups_to_keep)

    def test_2nd_end_of_year_save(self):
        backups = [
            '2018-12-31', '2019-12-31', '2020-01-31', '2020-02-28', '2020-03-31',
            '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06', '2020-04-07',
            '2020-04-08', '2020-04-09', '2020-04-10', '2020-04-11', '2020-04-12', '2020-04-13', '2020-04-14'
        ]
        backups = convert_all_datestrings_in_list_to_datetime(backups)
        backups_to_keep = find_backups_to_keep(backups, datetime(2020, 4, 14))
        backups.sort()
        backups_to_keep.sort()
        correct_backups_to_keep = [
            '2019-12-31', '2020-01-31', '2020-02-28', '2020-03-31',
            '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06', '2020-04-07',
            '2020-04-08', '2020-04-09', '2020-04-10', '2020-04-11', '2020-04-12', '2020-04-13', '2020-04-14'
        ]
        correct_backups_to_keep = convert_all_datestrings_in_list_to_datetime(correct_backups_to_keep)
        correct_backups_to_keep.sort()
        self.assertEqual(backups_to_keep, correct_backups_to_keep)


class TestOtherFuctions(unittest.TestCase):
    def test_remove_dates(self):
        all_backups = [
            '2018-07-31', '2018-08-31', '2018-09-30', '2018-10-31',
            '2018-11-01', '2018-11-02', '2018-11-03', '2018-11-04', '2018-11-05', '2018-11-06', '2018-11-07',
            '2018-11-08', '2018-11-09', '2018-11-10', '2018-11-11', '2018-11-12', '2018-11-13', '2018-11-14'
        ]
        all_backups = convert_all_datestrings_in_list_to_datetime(all_backups)
        backups_to_keep = [
            '2018-08-31', '2018-09-30', '2018-10-31',
            '2018-11-01', '2018-11-02', '2018-11-03', '2018-11-04', '2018-11-05', '2018-11-06', '2018-11-07',
            '2018-11-08', '2018-11-09', '2018-11-10', '2018-11-11', '2018-11-12', '2018-11-13', '2018-11-14'
        ]
        backups_to_keep = convert_all_datestrings_in_list_to_datetime(backups_to_keep)
        backups_to_remove = get_dates_to_remove_from_dates_to_keep(backups_to_keep, all_backups)

        correct_backups_to_remove = ['2018-07-31']
        correct_backups_to_remove = convert_all_datestrings_in_list_to_datetime(correct_backups_to_remove)
        self.assertEqual(backups_to_remove, correct_backups_to_remove)


if __name__ == '__main__':
    unittest.main()
