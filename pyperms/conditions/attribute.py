from typing import Any
from weakref import WeakKeyDictionary

from pyperms.conditions.utils import getattr_recursive


class Attribute:
    __name: str
    __values: WeakKeyDictionary

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__values = WeakKeyDictionary()

    def get_value(self, obj: object) -> Any:
        if obj not in self.__values:
            self.__values[obj] = getattr_recursive(obj, self.__name)
        return self.__values[obj]


def attr(name: str) -> Attribute:
    return Attribute(name)
