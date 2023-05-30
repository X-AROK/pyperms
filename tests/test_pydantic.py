from datetime import datetime, timedelta

import pytest
from pydantic import BaseModel, Field

from pyperms import PermissionsBuilder
from pyperms import operators as _


class User(BaseModel):
    id: int
    login: str


class Info(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())


class Post(BaseModel):
    id: int
    name: str
    info: Info
    user_id: int


@pytest.fixture
def user():
    user = User(id=1, login="test")
    return user


@pytest.fixture
def post():
    info = Info()
    post = Post(id=1, name="test", info=info, user_id=1)

    return post


def define_perms_for(user: User):
    builder = PermissionsBuilder()

    builder.can("read", "Post")
    builder.can(
        "update",
        "Post",
        fields=["name"],
        condition=_.Eq("user_id", user.id),
    )
    builder.can(
        "update",
        "Post",
        fields=["test"],
        condition=_.Lt("info.created_at", datetime.now() + timedelta(days=1)),
    )

    return builder.build()


def test_pydantic(user, post):
    perms = define_perms_for(user)

    assert perms.can("update", "Post") is False
    assert perms.cannot("update", "Post") is True

    assert perms.can("update", post, field="name") is True
    assert perms.cannot("update", post, field="name") is False

    assert perms.can("read", post) is True
    assert perms.cannot("read", post) is False

    assert perms.can("update", post, field="test") is True
    assert perms.cannot("update", post, field="test") is False
