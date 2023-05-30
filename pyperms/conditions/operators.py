import operator as op
import re
from typing import Container, Iterable, Sized, Union

from pyperms.conditions.base import BaseLogicOperator1 as _BaseLogicOperator1
from pyperms.conditions.base import BaseLogicOperator2 as _BaseLogicOperator2
from pyperms.conditions.base import BaseOperator as _BaseOperator


def _not_in(__a: Container[object], __b: object, /) -> bool:
    return __b not in __a


def _all(__a: Container[object], __b: Iterable[object]) -> bool:
    return all([e in __a for e in __b])


def _size(__a: Sized, __b: int) -> bool:
    return len(__a) == __b


def _regex(__a: str, __b: Union[str, re.Pattern], /) -> bool:
    return bool(re.match(__b, __a))


class And(_BaseLogicOperator2, func=op.and_):
    "Same as `Operator() and Operator()`"
    ...


class Or(_BaseLogicOperator2, func=op.or_):
    "Same as `Operator() or Operator()`"
    ...


class Not(_BaseLogicOperator1, func=op.not_):
    "Same as `not Operator()`"
    ...


class Eq(_BaseOperator, func=op.eq):
    "Same as `attr == value`"
    ...


class Ne(_BaseOperator, func=op.ne):
    "Same as `attr != value`"
    ...


class Lt(_BaseOperator, func=op.lt):
    "Same as `attr < value`"
    ...


class Le(_BaseOperator, func=op.le):
    "Same as `attr <= value`"
    ...


class Gt(_BaseOperator, func=op.gt):
    "Same as `attr > value`"
    ...


class Ge(_BaseOperator, func=op.ge):
    "Same as `attr >= value`"
    ...


class In(_BaseOperator, func=op.contains):
    "Same as `value in attr`"
    ...


class NIn(_BaseOperator, func=_not_in):
    "Same as `value not in attr`"
    ...


class All(_BaseOperator, func=_all):
    "Checks that `attr` should contain all elements from the specified array (`value`)."
    ...


class Size(_BaseOperator, func=_size):
    "Checks that `attr` length equals to specified `value`"
    ...


class Regex(_BaseOperator, func=_regex):
    "Same as `bool(re.match(value, attr))`"
    ...
