from typing import Generic, List, Optional, Union

from pyperms.conditions.types import Operator
from pyperms.types import Actions, Subjects


class Rule(Generic[Actions, Subjects]):
    action: Actions
    subject: Subjects
    __fields: Optional[List[str]]
    __condition: Optional[Operator]
    __inverted: bool

    def __init__(
        self,
        *,
        action: Actions,
        subject: Subjects,
        fields: Optional[List[str]],
        condition: Optional[Operator],
        inverted: bool = False,
    ) -> None:
        self.action = action
        self.subject = subject
        self.__fields = fields
        self.__condition = condition
        self.__inverted = inverted

    def match_subject(self, subject: Union[Subjects, object]) -> bool:
        if self.subject == "*":
            return True

        if isinstance(subject, str):
            return subject == self.subject

        return type(subject).__name__ == self.subject

    def match_action(self, action: Actions) -> bool:
        if self.action == "*":
            return True

        return action == self.action

    def match_conditions(self, obj: Union[Subjects, object]) -> bool:
        if self.__condition is None:
            return not self.__inverted

        if isinstance(obj, str):
            return False

        return self.__condition(obj) ^ self.__inverted

    def match_field(self, field: Optional[str]) -> bool:
        if self.__fields is None:
            return True

        return field in self.__fields
