from typing import Any, Callable, Union, cast

from pyperms.conditions.attribute import Attribute
from pyperms.conditions.types import Operator
from pyperms.conditions.utils import getattr_recursive


class BaseOperator:
    __attr: Union[str, Attribute]
    __value: Any
    __func: Callable[[Any, Any], bool]

    def __init__(self, attr: Union[str, Attribute], value: Any) -> None:
        self.__attr = attr
        self.__value = value

    def __init_subclass__(cls, func: Callable[[Any, Any], bool]) -> None:
        cls.__func = cast(Callable[[Any, Any], bool], staticmethod(func))

    def __call__(self, obj: object) -> bool:
        if isinstance(self.__attr, Attribute):
            attr = self.__attr.get_value(obj)
        else:
            attr = getattr_recursive(obj, self.__attr)
        return self.__func(attr, self.__value)


class BaseLogicOperator2:
    __op1: Operator
    __op2: Operator
    __func: Callable[[bool, bool], bool]

    def __init__(self, op1: Operator, op2: Operator) -> None:
        self.__op1 = op1
        self.__op2 = op2

    def __init_subclass__(cls, func: Callable[[bool, bool], bool]) -> None:
        cls.__func = cast(Callable[[bool, bool], bool], staticmethod(func))

    def __call__(self, obj: object) -> bool:
        return self.__func(self.__op1(obj), self.__op2(obj))


class BaseLogicOperator1:
    __op1: Operator
    __func: Callable[[bool], bool]

    def __init__(self, op1: Operator) -> None:
        self.__op1 = op1

    def __init_subclass__(cls, func: Callable[[bool], bool]) -> None:
        cls.__func = cast(Callable[[bool], bool], staticmethod(func))

    def __call__(self, obj: object) -> bool:
        return self.__func(self.__op1(obj))
