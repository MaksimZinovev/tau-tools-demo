from typing import Optional
from re import findall


class El:
    def __init__(self, elems):
        self._list = elems

    def __getitem__(self, item):
        if len(self._list) > 0:
            return self._list[item]
        else:
            raise IndexError('Cannot get last() from an empty list.')

    def last(self) -> int:
        if len(self._list) > 0:
            return self._list[-1]
        else:
            raise IndexError('Cannot get last() from an empty list.')

    def first(self) -> int:
        if len(self._list) > 0:
            return self._list[0]
        else:
            raise IndexError('Cannot get first() from an empty list.')


class Ut:
    def __init__(self):
        self._ut = None

    def find_all_nums(self, _str: str, return_int=True) -> El:
        value = findall(r'[0-9.]+', _str)
        if value:
            value = [int(float(e)) for e in value] if return_int is True else [float(e) for e in value]
        self._ut = value
        return El(value)


def find_nums(_str: str, return_int=True) -> list:
    value = findall(r'[-+]?[0-9]*\.?[0-9]+', _str)
    if len(value) > 0:
        value = [int(float(e)) for e in value] if return_int is True else [float(e) for e in value]
    return value


