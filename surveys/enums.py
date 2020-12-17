from enum import Enum


class QuestionTypes(Enum):
    TEXT = 'text'
    CHOICE = 'choice'
    MULTIPLE_CHOICE = 'muliple_choice'

    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls]
