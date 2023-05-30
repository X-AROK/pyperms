from typing import Any


def getattr_recursive(obj: object, attrs_chain: str) -> Any:
    current = obj
    attrs = attrs_chain.split(".")
    for attr in attrs:
        current = getattr(current, attr)

    return current
