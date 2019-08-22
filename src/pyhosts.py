#!/usr/bin/python
# coding=utf-8

__author__ = 'Simon Charest'
__copyright__ = 'Copyright 2019, SLCIT inc.'
__credits__ = [
    'Steven Black',
    'Guillaume Veck'
]
__email__ = 'simoncharest@gmail.com'
__license__ = 'GNU'
__maintainer__ = 'Simon Charest'
__project__ = 'PyHosts'
__status__ = 'Developement'
__version__ = '1.0.0'

"""
This app will download a list of black listed hosts and add them to the local hosts file, to be ignored.
"""

import os
import sys
import urllib
from urllib import request

# Global constants definitions
USAGE = 'Usage:\n' \
        '  python pyhosts.py --update\n' \
        '  python pyhosts.py --install master | fakenews | gambling | porn | social [--whitelist "site1,siteN"]\n' \
        '  python pyhosts.py --remove master | fakenews | gambling | porn | social\n' \
        'Examples:\n' \
        '  python pyhosts.py --update\n' \
        '  python pyhosts.py --install social --whitelist "0.0.0.0 www.linkedin.com,0.0.0.0 www.twitter.com"\n' \
        '  python pyhosts.py --remove social'

# All files include master list
HOSTS = {
    "master": "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",  # Adware and malware
    "fakenews": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews/hosts",
    "gambling": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling/hosts",
    "porn": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn/hosts",
    "social": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/social/hosts",
    "fakenews-gambling":
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling/hosts",
    "fakenews-porn": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-porn/hosts",
    "fakenews-social": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-social/hosts",
    "gambling-porn": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn/hosts",
    "gambling-social": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-social/hosts",
    "porn-social": "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/porn-social/hosts",
    "fakenews-gambling-porn":
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn/hosts",
    "fakenews-gambling-social":
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-social/hosts",
    "fakenews-porn-social":
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-porn-social/hosts",
    "gambling-porn-social":
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/gambling-porn-social/hosts",
    "fakenews-gambling-porn-social":
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn-social/hosts",
}
ENCODING = 'utf8'
EXTENSION = '.txt'


def main():
    # Manage input arguments
    if intersect(['--help', '-h', '/?'], sys.argv):
        print(USAGE)

    elif len(sys.argv) == 2 and intersect(['--update', '-u', '/u'], sys.argv[1]):
        for file, url in HOSTS.items():
            # Get remote black listed hosts file content
            content = get(url)

            # Write black listed content locally
            write(file + EXTENSION, content)

    elif len(sys.argv) in [3, 5] and intersect(['--install', '-i', '/i'], sys.argv[1]):
        # Get hosts file name
        file = get_hosts()

        # Read hosts file content
        hosts = read(file)

        # Read black listed hosts file contents
        content = read(sys.argv[2] + EXTENSION)

        # Combine black listed hosts and hosts file contents, removing duplicates
        content = add(hosts, content)

        # Remove white listed elements
        if len(sys.argv) == 5 and intersect(['--whitelist', '-w', '/w'], sys.argv[3]):
            content = remove(content, sys.argv[4].split())

        # Rewrite hosts file content
        write(file, content)

    elif len(sys.argv) == 3 and intersect(['--remove', '-r', '/r'], sys.argv[1]):
        # Get hosts file name
        file = get_hosts()

        # Read hosts file content
        hosts = read(file)

        # Read black listed hosts file contents
        content = read(sys.argv[2] + EXTENSION)

        # Remove black listed elements
        content = remove(hosts, content)

        # Rewrite hosts file content
        write(file, content)

    else:
        print(USAGE)


def intersect(list1, list2):
    return [element for element in list1 if element in list2]


def get_hosts():
    """ Get local hosts file, by operating system """
    file = '/etc/hosts'

    if os.name == 'nt':
        file = 'C:/Windows/System32/drivers/etc/hosts'

    return file


def get(url):
    """ Get remote file content """
    return trim(decode(urllib.request.urlopen(url)))


def decode(list_, encoding=ENCODING):
    """ Decode all elements from list, from bytes to string """
    return [bytes_.decode(encoding) for bytes_ in list_]


def trim(list_):
    """ Strip elements in list """
    return [element.strip() for element in list_]


def read(file, mode='rt'):
    """ Read file and return content, line by line, as a list """
    with open(file, mode) as handle:
        lines = handle.read().splitlines()

    return lines


def write(file, content, mode='wt'):
    """ Write file, line by line """
    with open(file, mode) as handle:
        for line in content:
            handle.write(line + '\n')

    return True


def add(list_, elements, duplicate=False):
    """ Add elements to a list, ignoring or not duplicates """
    for element in elements:
        if element not in list_ or duplicate:
            list_.append(element)

    return list_


def remove(list_, elements):
    """ Remove all occurrences of certain elements from a list """
    return [element for element in list_ if element not in elements]


def print_list(list_):
    """ Print each element of a list """
    for element in list_:
        print(element)

    return True


if __name__ == '__main__':
    main()
