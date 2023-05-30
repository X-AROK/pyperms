from dataclasses import dataclass
from typing import List

import pytest

from pyperms import PermissionsBuilder


@dataclass
class User:
    id: int
    name: str
    roles: List[str]


@pytest.fixture
def admin():
    user = User(id=1, name="admin", roles=["admin"])
    return user


@pytest.fixture
def user():
    user = User(id=1, name="test", roles=["user"])
    return user


def all_perms(user):
    builder = PermissionsBuilder()

    if "admin" in user.roles:
        builder.can("*", "*")
    else:
        builder.can("read", "Post")
        builder.cannot("create", "Post")

    return builder.build()


def field_perms(user):
    builder = PermissionsBuilder()

    builder.can("read", "Post", fields=["name", "created_at"])
    if "admin" not in user.roles:
        builder.cannot("read", "Post", fields=["created_at"])
        builder.can("read", "Post", fields=["author"])
    if "user" in user.roles:
        builder.can("update", "Post")
        builder.cannot("update", "Post", fields=["title"])

    return builder.build()


def test_perms(user, admin):
    user_perms = all_perms(user)
    admin_perms = all_perms(admin)

    assert user_perms.can("read", "Post") is True
    assert user_perms.cannot("read", "Post") is False

    assert user_perms.can("create", "Post") is False
    assert user_perms.cannot("create", "Post") is True

    assert admin_perms.can("read", "Post") is True
    assert admin_perms.cannot("read", "Post") is False

    assert admin_perms.can("create", "Post") is True
    assert admin_perms.cannot("create", "Post") is False

    assert admin_perms.can("update", "Roles") is True
    assert admin_perms.cannot("update", "Roles") is False


def test_fields(user, admin):
    user_perms = field_perms(user)
    admin_perms = field_perms(admin)

    assert user_perms.can("read", "Post") is False
    assert user_perms.cannot("read", "Post") is True

    assert user_perms.can("read", "Post", field="name") is True
    assert user_perms.cannot("read", "Post", field="name") is False

    assert user_perms.can("read", "Post", field="author") is True
    assert user_perms.cannot("read", "Post", field="author") is False

    assert user_perms.can("read", "Post", field="created_at") is False
    assert user_perms.cannot("read", "Post", field="created_at") is True

    assert user_perms.can("update", "Post") is True
    assert user_perms.cannot("update", "Post") is False

    assert user_perms.can("update", "Post", field="title") is False
    assert user_perms.cannot("update", "Post", field="title") is True

    assert admin_perms.can("read", "Post", field="name") is True
    assert admin_perms.cannot("read", "Post", field="name") is False

    assert admin_perms.can("read", "Post", field="author") is False
    assert admin_perms.cannot("read", "Post", field="author") is True

    assert admin_perms.can("read", "Post", field="created_at") is True
    assert admin_perms.cannot("read", "Post", field="created_at") is False
