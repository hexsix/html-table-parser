# -----------------------------------------------------------------------------
# Created:     04.03.2014
# Copyright:   (c) Josua Schmid 2014
# Licence:     AGPLv3
#
# Sample script for parsing HTML tables
# -----------------------------------------------------------------------------

import urllib.request
from pprint import pprint
from html_table_parser import HTMLTableParser


def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()


def main():
    url = 'http://oeis.org/search?q=12%2C21%2C13%2C31%2C14%2C41&sort=&language=english&go=Search'
    html = url_get_contents(url).decode('utf-8')

    p = HTMLTableParser()
    p.feed(html)
    pprint(p.tables)


if __name__ == '__main__':
    main()
