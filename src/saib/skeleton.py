#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
//TODO This
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = tracker.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import configparser
import logging
import re
import sys

import paramiko
import pymysql
import pymysql.cursors

from saib import __version__

config = configparser.ConfigParser()
config.read("./config")

__author__ = "Ryan Long"
__copyright__ = "Ryan Long"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def get_saib_data():
    """
    Fetches saib login credential locally and from the config file and returns
    a dict containing those values.

    Returns:
        dict(username, password, database, address): Saib login credentials
    """
    return {
        'username': config['saib']['username'],
        'password': config['saib']['password'],
        'database': 'saib',
        'address': '172.104.17.17',
    }


def get_cerebro_data():
    """
        Fetches cerebro login credential locally and from the config file and returns
        a dict containing those values.

        Returns:
            dict(username, password, port, address): Cerebro login credentials
        """
    return {
        'username': config['cerebro']['username'],
        'password': config['cerebro']['password'],
        'port': 22,
        'address': '192.168.0.1',
    }

def parse_update(update_data):
    """
    Parses a full dump of the updated login  data

    Args:
        update_data (list[str]): data

    Returns:
        list[str]: data parsed ready for database entry

    """
    result = []
    for entry in update_data:
        result.append(parse_update_entry(entry))
    return result


def parse_update_entry(entry):
    """
    Parses an entry from the login update dump

    Args:
        entry(string): data as name mac and ip

    Returns:
        dict(name, ip, mac): a parsed entry
    """
    entry_map = {
        "name": 0,
        "ip": 1,
        "mac": 3,
    }

    data = re.split(r'\s', entry.strip())
    name = clean_update_item_string(data[entry_map["name"]])
    ip = clean_update_item_string(data[entry_map["ip"]])
    mac_address = clean_update_item_string(data[entry_map["mac"]])
    return {
        "name": name,
        "ip": ip,
        "mac_address": mac_address,
    }


def clean_update_item_string(string):
    """
    Removes "(" and ")" parentheses from a string

    Args:
        string(str): entry

    Returns:
        str: string with parens removed
    """
    return str(string.replace("(", "").replace(")", ""))


def fetch_router_data():  # pragma: no cover
    """
    Fetches data from the target router by running arp-a

    Returns:
        list: each line from stdout from
    """
    cerebro_data = get_cerebro_data()
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(cerebro_data['address'], cerebro_data['port'],
                cerebro_data['username'],
                cerebro_data['password'])
    (ssh_stdin, ssh_stdout, ssh_stderr) = ssh.exec_command("arp -a")
    return [entry for entry in ssh_stdout]


def update():
    """
    Processes update, fetching data from the router and writing to the database

    Returns:
        None:
    """
    _logger.info("Writing update")
    write_update(parse_update(fetch_router_data()))


def write_update(parsed_data):  # pragma: no cover
    """
    Writes the parsed data to the database

    Args:
        parsed_data(list): data

    Returns:
        None
    """
    _logger.debug("Writing update with parsed_data")
    connection = get_saib_connection()
    try:
        with connection.cursor() as cursor:
            for item in parsed_data:
                sql = '''INSERT INTO `log_in_range`
                 (`ip`, `mac_address`, `name`) 
                 VALUES (%s, %s, %s)'''
                cursor.execute(sql,
                               (item["ip"], item["mac_address"], item["name"]))
                connection.commit()
            _logger.debug("Running %s" % sql)
    finally:
        connection.close()


def get_saib_connection():
    """
    Attempts to get a connection to Saib

    Returns:
        obj: live connection to saib

    """
    _logger.debug("Getting saib connection")
    saib_data = get_saib_data()
    connection = pymysql.connect(host=saib_data['address'],
                                 user=saib_data['username'],
                                 password=saib_data['password'],
                                 db=saib_data['database'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def update_mac_to_name_entries():
    """Updates the mac_to_name table with new entries from the log
    """
    _logger.debug("Updating mac_to_name table")
    connection = get_saib_connection().cursor()
    try:
        with connection.cursor() as cursor:
            sql = '''
                INSERT INTO mac_to_name (mac_address)
                SELECT DISTINCT(mac_address) FROM log_in_range
                WHERE mac_address NOT IN (SELECT mac_address FROM mac_to_name)
                '''
            _logger.debug("Running %s" % sql)
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Saib tracker")
    parser.add_argument(
        '--version',
        action='version',
        version='saib {ver}'.format(ver=__version__))
    parser.add_argument(
        '-u',
        '--update',
        help="Fetches updated info and posts to persistence",
        action='store_true')
    parser.add_argument(
        '-um',
        '--update-mac',
        help="Updates the mac_to_name table with new mac_addresses from the log",
        action='store_true')
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    if args.update:
        _logger.info("Updating persistence...")
        update()
        _logger.info("Updating persistence complete")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
