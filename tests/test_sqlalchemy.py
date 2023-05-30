from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
    sessionmaker,
)

from pyperms import PermissionsBuilder
from pyperms import operators as _

Base = declarative_base()


class User(Base):
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    posts: Mapped[List["Post"]] = relationship(back_populates="author")


class Post(Base):
    __tablename__: str = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")


engine = create_engine("sqlite:///")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    user = User(name="admin")
    post = Post(title="Test")
    user.posts.append(post)
    session.add(user)
    session.commit()


def define_perms_for(user: User):
    builder = PermissionsBuilder()

    builder.can("read", "Post", condition=_.Gt("id", 0))
    builder.can(
        "update",
        "Post",
        condition=_.Eq("author.id", user.id),
    )

    return builder.build()


def test_sqlalchemy():
    with Session() as session:
        user: User = session.get(User, 1)
        post: Post = session.get(Post, 1)

        perms = define_perms_for(user)

        assert perms.can("update", "Post") is False
        assert perms.cannot("update", "Post") is True

        assert perms.can("update", post) is True
        assert perms.cannot("update", post) is False

        assert perms.can("read", post) is True
        assert perms.cannot("read", post) is False
