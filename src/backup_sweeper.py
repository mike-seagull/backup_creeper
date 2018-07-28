#!/usr/bin/env python2.7

import os
import os.path
import re
from datetime import datetime, timedelta
import argparse
import logging
import sys

if getattr(sys, 'frozen', False):
    # running in a bundle
    log_file = os.path.join("/var/log", "%s.log" % sys.executable)
else:
    # running live
    repo_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    log_file = os.path.join(repo_root, "logs", "%s.log" % __file__)
formatter = logging.Formatter('[%(asctime)s] - %(filename)s - %(levelname)s: %(message)s')
# make logger
log = logging.getLogger(__file__)   # create logger
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()    # log to console
# log debug messages
ch.setLevel(logging.INFO)
# create formatter and add it to the handler
ch.setFormatter(formatter)
# add the handlers to the logger
log.addHandler(ch)
try:
    # create file handler
    fh = logging.FileHandler(log_file)  # log to file
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log.addHandler(fh)
except IOError:
    log.error("Failed to create log file handler. Check permissions for: %s" % log_file)


def get_backups(backup_dir):
    """ This returns only the names of files and dirs in the given dir
    This does not give the full path
    """
    log.debug("in get_backups")
    return os.listdir(backup_dir)


'''
def get_all_dates_from_list_of_backup_strings(regex, list_of_backups):
    log.debug("get_all_dates_from_list_of_backup_strings")
    pattern = re.compile(regex)
    return [match.group(0) for backup in list_of_backups for match in [pattern.search(backup)] if match]
'''


def get_all_dates_from_list_of_backup_strings(regex, list_of_backups, backup_dir="./"):
    log.debug("in get_all_dates_from_list_of_backup_strings")
    dates = {}
    pattern = re.compile(regex)
    for backup in list_of_backups:
        for match in [pattern.search(backup)]:
            if match:
                # this is {date_string: {filename: "", path: ""}}
                dates[match.group(0)] = {
                    "filename": backup,
                    "path": os.path.join(backup_dir, backup)
                }
    return dates


def convert_all_datestrings_in_list_to_datetime(list_of_date_strings, date_string_format='%Y-%m-%d'):
    log.debug("in convert_all_datestrings_in_list_to_datetime")
    return [datetime.strptime(date_string, date_string_format) for date_string in list_of_date_strings]


def convert_all_datetimes_to_strings(list_of_datetimes, date_string_format='%Y-%m-%d'):
    log.debug("in convert_all_datetimes_to_strings")
    return [date.strftime(date_string_format) for date in list_of_datetimes]


def is_date_within_weeks_ago(date, weeks_ago=2, today=None):
    """ returns true if datetime is within x weeks_ago from "today"
        expects a datetime object
    """
    log.debug("is_date_within_weeks_ago")
    if not today:
        today = datetime.today()
    margin = timedelta(weeks=weeks_ago)
    return today - margin < date <= today + margin


def get_latest_backup_from_months_ago(backups, months_ago=1, lastMonth=None):
    log.debug("in get_latest_backup_from_months_ago")
    log.debug("backups= %s" % str(backups))
    if not lastMonth:
        lastMonth = datetime.today()
    log.debug("lastMonth=%s" % str(lastMonth))
    for _ in range(months_ago):
        first = lastMonth.replace(day=1)
        log.debug("first=%s" % str(first))
        lastMonth = first - timedelta(days=1)
        log.debug("lastMonth=%s" % str(lastMonth))
    all_backups_this_month = [backup for backup in backups if lastMonth.month == backup.month and lastMonth.year == backup.year]
    all_backups_this_month.sort()
    log.debug("all_backups_this_month=%s" % str(all_backups_this_month))
    try:
        return all_backups_this_month.pop()
    except IndexError:
        log.warning("No backups for month of: %s" % str(lastMonth))
        return None


def get_latest_backup_from_last_years_ago(backups, years_ago=1, lastYear=None):
    log.debug("in get_latest_backup_from_last_years_ago")
    log.debug("backups= %s" % str(backups))
    if not lastYear:
        lastYear = datetime.today()
    log.debug("lastYear=%s" % str(lastYear))
    for _ in range(years_ago):
        first = lastYear.replace(day=1, month=1)
        lastYear = first - timedelta(days=1)
    all_backups_lastYear = [backup for backup in backups if lastYear.year == backup.year]
    all_backups_lastYear.sort()
    try:
        return all_backups_lastYear.pop()
    except IndexError:
        log.warning("No backups for year of: %s" % lastYear)
        return None


def find_backups_to_keep(backup_dates, today=None):
    """ This is the main algorithm magic """
    log.debug("in find_backups_to_keep")
    backups_to_keep = []
    if not today:
        today = datetime.today()
    log.debug("today=%s" % str(today))
    WEEKS_AGO = 2  # how many weeks of daily backups to keep
    log.debug("WEEKS_AGO=%i" % WEEKS_AGO)
    for backup_date in backup_dates:
        if is_date_within_weeks_ago(backup_date, WEEKS_AGO, today):
            backups_to_keep.append(backup_date)
    MONTHS_AGO_TO_KEEP = 3  # how many months of months of monthly backups
    log.debug("MONTHS_AGO_TO_KEEP=%i" % MONTHS_AGO_TO_KEEP)
    for i in range(MONTHS_AGO_TO_KEEP):
        months_ago = i + 1
        backup_date = get_latest_backup_from_months_ago(backup_dates, months_ago, today)
        if backup_date:
            backups_to_keep.append(backup_date)
    YEARS_AGO = 1  # how many years of annual backups
    log.debug("YEARS_AGO=%i" % YEARS_AGO)
    backup_date = get_latest_backup_from_last_years_ago(backup_dates, YEARS_AGO, today)
    if backup_date:
        backups_to_keep.append(backup_date)
    backups_to_keep = list(set(backups_to_keep))  # remove duplicates
    return backups_to_keep


def get_dates_to_remove_from_dates_to_keep(dates_to_keep, all_dates):
    log.debug("get_dates_to_remove_from_dates_to_keep")
    return list(set(all_dates) - set(dates_to_keep))


def delete_backups(date_strings_to_remove, backup_info):
    log.debug("in delete_backups")
    for date_string_to_remove in date_strings_to_remove:
        try:
            log.info("about to delete this backups: %s" % (backup_info[date_string_to_remove]["path"]))
            os.remove(backup_info[date_string_to_remove]["path"])
        except OSError as oe:  # if failed, report it back to the user ##
            log.error(oe)


def main(backup_dir):
    log.debug("in main")
    log.info("backup_dir = %s" % backup_dir)
    log.info("about to get backups")
    backups = get_backups(backup_dir)
    log.debug("backups are: %s" % backups)
    log.info("about to get the list of all backups as strings")
    backup_info = get_all_dates_from_list_of_backup_strings(r'\d{4}-\d{2}-\d{2}', backups, backup_dir)
    log.debug("backup dates and paths are: %s" % str(backup_info))
    log.info("about to convert all datestrings to datetimes")
    all_backup_dates = convert_all_datestrings_in_list_to_datetime(backup_info.keys())
    log.debug("all_backup_dates_are: %s" % str(all_backup_dates))
    log.info("about to find all backups to keep")
    datetimes_to_keep = find_backups_to_keep(all_backup_dates)
    log.debug("datetimes_to_keep are: %s" % str(datetimes_to_keep))
    log.info("about to get the datetimes to remove")
    datetimes_to_remove = get_dates_to_remove_from_dates_to_keep(datetimes_to_keep, all_backup_dates)
    log.debug("datetimes_to_remove are: %s" % str(datetimes_to_remove))
    log.info("about to convert all datetimes to remove to datestrings")
    date_strings_to_remove = convert_all_datetimes_to_strings(datetimes_to_remove)
    log.debug("date_strings_to_remove are: %s" % str(date_strings_to_remove))
    delete_backups(date_strings_to_remove, backup_info)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--backupdir', '-b', help="full path to backup directory", required=True)
    args = parser.parse_args()
    if not os.path.isabs(args.backupdir):
        print("Backup directory is not a full path")
        parser.print_help()
        sys.exit(2)
    log.info("Starting")
    main(args.backupdir)
    log.info("Done")
