from typing import Generic, List, Optional

from pyperms.conditions.types import Operator
from pyperms.permissions import Permissions
from pyperms.rule import Rule
from pyperms.types import Actions, Subjects


class PermissionsBuilder(Generic[Actions, Subjects]):
    __rules: List[Rule[Actions, Subjects]]

    def __init__(self) -> None:
        self.__rules = []

    def can(
        self,
        action: Actions,
        subject: Subjects,
        *,
        fields: Optional[List[str]] = None,
        condition: Optional[Operator] = None
    ) -> None:
        self.__add_rule(
            action,
            subject,
            False,
            fields,
            condition,
        )

    def cannot(
        self,
        action: Actions,
        subject: Subjects,
        *,
        fields: Optional[List[str]] = None,
        condition: Optional[Operator] = None
    ) -> None:
        self.__add_rule(action, subject, True, fields, condition)

    def __add_rule(
        self,
        action: Actions,
        subject: Subjects,
        inverted: bool,
        fields: Optional[List[str]],
        condition: Optional[Operator],
    ) -> None:
        self.__rules.append(
            Rule(
                action=action,
                subject=subject,
                inverted=inverted,
                fields=fields,
                condition=condition,
            )
        )

    def build(self) -> Permissions[Actions, Subjects]:
        return Permissions(self.__rules)
