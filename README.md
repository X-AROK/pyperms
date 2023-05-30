# PyPerms (Python Permissions)

PyPerms is a library for convenient access control. The inspiration was the JS library - [CASL](https://casl.js.org/).

## Simple Usage

```python
from pyperms import PermissionsBuilder

from .models import User


def define_perms_for(user):
    builder = PermissionsBuilder()

    builder.can("read", "Post")
    if "admin" in user.roles:
        builder.can("*", "*")

    return builder.build()


admin = User(id=1, roles=["admin"])
user = User(id=2, roles=["user"])

admin_perms = define_perms_for(admin)
user_perms = define_perms_for(user)

admin_perms = define_perms_for(admin)
user_perms = define_perms_for(user)

admin_perms.can("read", "Post")  # True
admin_perms.can("create", "Post")  # True
admin_perms.can("read", "Article")  # True

user_perms.can("read", "Post")  # True
user_perms.can("create", "Post")  # False
```

## Typing

For typing `Actions` and `Subjects`, you can use `Literal` from the standard module `typing`.

```python
from typing import Literal

from pyperms import PermissionsBuilder

Actions = Literal["*", "read"]
Subjects = Literal["*", "Post"]


def define_perms():
    builder = PermissionsBuilder[Actions, Subjects]()

    builder.can("read", "Post")  # OK
    builder.can("*", "*")  # OK

    builder.can("create", "Post")  # Error

    return builder.build()
```

## Fields

For more flexible permission settings, you can use the `fields` parameter.

```python
from pyperms import PermissionsBuilder


def define_perms():
    builder = PermissionsBuilder()
    builder.can("read", "Post", fields=["title", "author"])
    return builder.build()


perms = define_perms()
perms.can("read", "Post", field="title")  # True
perms.can("read", "Post", field="created_at")  # False
```

## Conditions

Sometimes permission checks may require conditions, such as whether the user is the author of the post. For such cases, there is a `condiotion` parameter in the builder `can` and `cannot` methods. For it to work, it is necessary to pass an instance of the class with the same name in the `subject`.

```python
from pyperms import PermissionsBuilder
from pyperms import operators as _

from .models import Post, User


def define_perms_for(user):
    builder = PermissionsBuilder()
    builder.can("update", "Post", condition=_.Eq("author", user.id))
    return builder.build()


post = Post(id=1, author=1)

user1 = User(id=1)
user2 = User(id=2)

user1_perms = define_perms_for(user1)
user2_perms = define_perms_for(user2)

user1_perms.can("update", post)  # True
user2_perms.can("update", post)  # False
```

`Operator` is a callable object that returns a boolean value. When it is initialized, the first parameter is the path to the attribute (can be separated by dot for recursive access), the second parameter is the value to be checked.

Here is a list of default operators:

-   Logical:
    -   And
    -   Or
    -   Not
-   Other:
    -   Eq
    -   Ne
    -   Lt
    -   Le
    -   Gt
    -   Ge
    -   In
    -   NIn
    -   All
    -   Size
    -   Regex

## Attributes

Each operator, when called, tries to get the attribute using `getattr`. To reduce the number of `getattr` calls, you can use the `Attribute` class or the `attr` function. An instance of this class stores the received attribute value for each object (comparison by id).

```python
from pyperms import PermissionsBuilder, attr
from pyperms import operators as _


def define_perms_for(user):
    builder = PermissionsBuilder()

    author = attr("author")
    builder.can("read", "Post", condition=_.Eq(author, user.id))
    builder.can("update", "Post", condition=_.Eq(author, user.id))

    return builder.build()
```

## Custom operators

All operators are subclasses of one of three base classes: `BaseLogicOperator1`, `BaseLogicOperator2`, `BaseOperator`.

An example of your own operator:

```python
from pyperms.conditions.base import BaseOperator


def my_func(__a: int, __b: int) -> bool:
    return __a + __b == 2


class MyOperator(BaseOperator, func=my_func):
    "Docstring for MyOperator"
    ...
```
