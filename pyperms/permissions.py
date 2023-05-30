from typing import Generic, List, Optional, Union

from pyperms.rule import Rule
from pyperms.types import Actions, Subjects


class Permissions(Generic[Actions, Subjects]):
    __rules: List[Rule[Actions, Subjects]]

    def __init__(self, rules: List[Rule[Actions, Subjects]]) -> None:
        self.__rules = rules

    def can(
        self,
        action: Actions,
        subject: Union[Subjects, object],
        field: Optional[str] = None,
    ) -> bool:
        return self.__check(action, subject, field)

    def cannot(
        self,
        action: Actions,
        subject: Union[Subjects, object],
        field: Optional[str] = None,
    ) -> bool:
        return not self.__check(action, subject, field)

    def __check(
        self,
        action: Actions,
        subject: Union[Subjects, object],
        field: Optional[str] = None,
    ) -> bool:
        result: List[bool] = []
        for rule in self.__rules:
            if not rule.match_subject(subject):
                continue

            if not rule.match_action(action):
                continue

            if not rule.match_field(field):
                continue

            result.append(rule.match_conditions(subject))

        return len(result) > 0 and all(result)
