from typing import List, Literal, Mapping, TypeAlias
from dataclasses import dataclass

Choice: TypeAlias = Literal['a', 'b', 'c', 'd', 'e']


@dataclass(slots=True)
class Question:
    question: str
    options: Mapping[Choice, str]
    answer: Choice

    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        return cls(**data)


@dataclass(slots=True)
class Test:
    id: str
    questions: List[Question]

    @classmethod
    def from_dict(cls, data: dict) -> 'Test':
        return cls(
            id=data['id'],
            questions=[Question.from_dict(question) for question in data['questions']],
        )


@dataclass(slots=True)
class Lesson:
    id: str
    title: str
    content: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Lesson':
        return cls(**data)


@dataclass(slots=True)
class Subject:
    id: str
    name: str
    lessons: List[Lesson]
    assessment: Test

    @classmethod
    def from_dict(cls, data: dict) -> 'Subject':
        return cls(
            id=data['id'],
            name=data['name'],
            lessons=[Lesson.from_dict(lesson) for lesson in data['lessons']],
            assessment=Test.from_dict(data['assessment']),
        )


@dataclass(slots=True)
class Course:
    id: str
    name: str
    subjects: List[Subject]

    @classmethod
    def from_dict(cls, data: dict) -> 'Course':
        return cls(
            id=data['id'],
            name=data['name'],
            subjects=[Subject.from_dict(subject) for subject in data['subjects']],
        )
