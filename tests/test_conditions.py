from dataclasses import dataclass
from typing import List

import pytest

from pyperms import operators as _


@dataclass
class User:
    id: int
    name: str
    roles: List[str]


@pytest.fixture
def user():
    user = User(id=1, name="test", roles=["admin"])
    return user


def test_eq(user):
    eq = _.Eq("id", 1)
    not_eq = _.Eq("id", 2)

    assert eq(user) is True
    assert not_eq(user) is False


def test_ne(user):
    eq = _.Ne("id", 1)
    not_eq = _.Ne("id", 2)

    assert eq(user) is False
    assert not_eq(user) is True


def test_ge(user):
    lt = _.Ge("id", 0)
    eq = _.Ge("id", 1)
    gt = _.Ge("id", 2)

    assert lt(user) is True
    assert eq(user) is True
    assert gt(user) is False


def test_gt(user):
    lt = _.Gt("id", 0)
    eq = _.Gt("id", 1)
    gt = _.Gt("id", 2)

    assert lt(user) is True
    assert eq(user) is False
    assert gt(user) is False


def test_in(user):
    in_ = _.In("roles", "admin")
    nin = _.In("roles", "test")

    assert in_(user) is True
    assert nin(user) is False


def test_nin(user):
    in_ = _.NIn("roles", "admin")
    nin = _.NIn("roles", "test")

    assert in_(user) is False
    assert nin(user) is True


def test_le(user):
    lt = _.Le("id", 0)
    eq = _.Le("id", 1)
    gt = _.Le("id", 2)

    assert lt(user) is False
    assert eq(user) is True
    assert gt(user) is True


def test_lt(user):
    lt = _.Lt("id", 0)
    eq = _.Lt("id", 1)
    gt = _.Lt("id", 2)

    assert lt(user) is False
    assert eq(user) is False
    assert gt(user) is True


def test_all(user):
    all_ = _.All("name", ["t", "s"])
    not_all = _.All("name", ["t", "a"])

    assert all_(user) is True
    assert not_all(user) is False


def test_regex(user):
    match_ = _.Regex("name", r"^t")
    not_match = _.Regex("name", r"[0-9]")

    assert match_(user) is True
    assert not_match(user) is False


def test_size(user):
    eq = _.Size("roles", 1)
    not_eq = _.Size("roles", 0)

    assert eq(user) is True
    assert not_eq(user) is False


def test_and(user):
    gt = _.Lt("id", 2)  # True
    eq = _.Eq("id", 1)  # True
    lt = _.Lt("id", 0)  # False
    not_eq = _.Eq("id", 2)  # False

    false_false = _.And(lt, not_eq)
    false_true = _.And(lt, gt)
    true_false = _.And(gt, lt)
    true_true = _.And(gt, eq)

    assert false_false(user) is False
    assert false_true(user) is False
    assert true_false(user) is False
    assert true_true(user) is True


def test_or(user):
    gt = _.Lt("id", 2)  # True
    eq = _.Eq("id", 1)  # True
    lt = _.Lt("id", 0)  # False
    not_eq = _.Eq("id", 2)  # False

    false_false = _.Or(lt, not_eq)
    false_true = _.Or(lt, gt)
    true_false = _.Or(gt, lt)
    true_true = _.Or(gt, eq)

    assert false_false(user) is False
    assert false_true(user) is True
    assert true_false(user) is True
    assert true_true(user) is True


def test_not(user):
    gt = _.Lt("id", 2)  # True
    lt = _.Lt("id", 0)  # False

    not_true = _.Not(gt)
    not_false = _.Not(lt)

    assert not_true(user) is False
    assert not_false(user) is True
