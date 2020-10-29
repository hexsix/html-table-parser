# -----------------------------------------------------------------------------
# Name:        html_table_parser
# Purpose:     Simple class for parsing an (x)html string to extract tables.
#              Written in python3
#
# Author:      Josua Schmid
#
# Created:     05.03.2014
# Copyright:   (c) Josua Schmid 2014
# Licence:     AGPLv3
#
# Modified:    hexsix
# M Date:      19.07.2020
# -----------------------------------------------------------------------------

from html.parser import HTMLParser
from typing import Tuple


class Table(list):
    def __init__(self, st: Tuple[int, int]):
        super().__init__()

        self.st = st
        self.ed = None

        self._is_active = True

        self._in_td = False
        self._in_th = False

        self._current_cell = []
        self._current_row = []

    def __repr__(self) -> str:
        return "Table({}, {}, {})".format(self.st, self.ed, super().__repr__())

    def set_in_td(self, val: bool) -> None:
        if self._is_active:
            self._in_td = val
        else:
            self[-1].set_in_td(val)

    def set_in_th(self, val: bool) -> None:
        if self._is_active:
            self._in_th = val
        else:
            self[-1].set_in_th(val)

    def append_to_cell(self, data: str) -> None:
        if self._is_active:
            if self._in_td or self._in_th:
                self._current_cell.append(data)
        else:
            self[-1].append_to_cell(data)

    def append_to_row(self) -> None:
        if self._is_active:
            final_cell = ' '.join(self._current_cell).strip()
            self._current_row.append(final_cell)
            self._current_cell = []
        else:
            self[-1].append_to_row()

    def append_to_table(self) -> None:
        if self._is_active:
            self.append(self._current_row)
            self._current_row = []
        else:
            self[-1].append_to_table()

    def new_table(self, st: Tuple[int, int]) -> None:
        """ create a sub table at the tail """
        if self._is_active:
            self.append(Table(st))
            self._is_active = False
        else:
            self[-1].new_table(st)

    def close_table(self, ed) -> bool:
        """ close the sub table at the tail """
        if self._is_active:
            if self._current_cell:
                self.append_to_row()
                self.append_to_table()
            self._is_active = False
            self.ed = ed
            return True
        else:
            ret = self[-1].close_table(ed)
            if ret:
                self._is_active = True
            return False


class HTMLTableParser(HTMLParser):
    """ This class serves as a html table parser. It is able to parse multiple
    tables which you feed in. You can access the result per .tables field.
    """

    def error(self, message):
        pass

    def __init__(
        self,
        decode_html_entities=False,
        data_separator=' ',
    ):

        super(HTMLTableParser, self).__init__(convert_charrefs=decode_html_entities)

        self._data_separator = data_separator

        self._current_table = None
        self.tables = []

    def handle_starttag(self, tag, attrs):
        """ We need to remember the opening point for the content of interest.
        The other tags (<tr>) are only handled at the closing point.
        """
        st = self.getpos()
        if tag == 'td' and self._current_table is not None:
            self._current_table.set_in_td(True)
        if tag == 'th' and self._current_table is not None:
            self._current_table.set_in_th(True)
        if tag == 'table':
            if self._current_table is None:
                self._current_table = Table(st)
            else:
                self._current_table.new_table(st)

    def handle_data(self, data):
        """ This is where we save content to a cell """
        if self._current_table is not None:
            self._current_table.append_to_cell(data.strip())
    
    def handle_endtag(self, tag):
        """ Here we exit the tags. If the closing tag is </tr>, we know that we
        can save our currently parsed cells to the current table as a row and
        prepare for a new row. If the closing tag is </table>, we save the
        current table and prepare for a new one.
        """
        if tag == 'td' and self._current_table is not None:
            self._current_table.set_in_td(False)
        elif tag == 'th' and self._current_table is not None:
            self._current_table.set_in_th(False)

        if tag in ['td', 'th'] and self._current_table is not None:
            self._current_table.append_to_row()
        elif tag == 'tr' and self._current_table is not None:
            self._current_table.append_to_table()
        elif tag == 'table' and self._current_table is not None:
            ed = self.getpos()
            if self._current_table.close_table(ed):
                self.tables.append(self._current_table)
                self._current_table = None
