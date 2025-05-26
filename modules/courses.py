from typing import TYPE_CHECKING, List, Literal, Mapping
from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import TypeAlias

Choice: 'TypeAlias' = Literal['a', 'b', 'c', 'd', 'e']


@dataclass
class Question:
    __slots__ = ('answer', 'index', 'options', 'question', 'weight')
    index: int
    weight: int
    question: str
    options: Mapping[Choice, str]
    answer: Choice

    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        return cls(**data)


@dataclass
class Test:
    __slots__ = ('id', 'questions')
    id: str
    questions: List[Question]

    @classmethod
    def from_dict(cls, data: dict) -> 'Test':
        return cls(
            id=data['id'],
            questions=[
                Question.from_dict(question)
                for question in sorted(data['questions'], key=lambda x: x['index'])
            ],
        )


@dataclass
class Lesson:
    __slots__ = ('content', 'id', 'title')
    id: str
    title: str
    content: str

    @property
    def index(self) -> int:
        return int(self.id[-4:-1])

    @classmethod
    def from_dict(cls, data: dict) -> 'Lesson':
        return cls(**data)


@dataclass
class Subject:
    __slots__ = ('id', 'lessons', 'max_grade', 'name', 'test')
    id: str
    name: str
    max_grade: int
    lessons: List[Lesson]
    test: Test

    @classmethod
    def from_dict(cls, data: dict) -> 'Subject':
        return cls(
            id=data['id'],
            name=data['name'],
            max_grade=data['max_grade'],
            lessons=[
                Lesson.from_dict(lesson)
                for lesson in sorted(data['lessons'], key=lambda x: x['id'])
            ],
            test=Test.from_dict(data['test']),
        )


@dataclass
class Course:
    __slots__ = ('id', 'name', 'subjects')
    id: str
    name: str
    subjects: List[Subject]

    @classmethod
    def from_dict(cls, data: dict) -> 'Course':
        return cls(
            id=data['id'],
            name=data['name'],
            subjects=[
                Subject.from_dict(subject)
                for subject in sorted(data['subjects'], key=lambda x: x['name'])
            ],
        )
