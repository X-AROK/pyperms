from typing import Any, Dict

from pyperms.conditions.utils import getattr_recursive


class Attribute:
    __name: str
    __values: Dict[object, Any]

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__values = {}

    def get_value(self, obj: object) -> Any:
        id_ = id(obj)
        if id_ not in self.__values:
            self.__values[id_] = getattr_recursive(obj, self.__name)
        return self.__values[id_]


def attr(name: str) -> Attribute:
    return Attribute(name)
