from typing import List, Literal, Mapping, TypeAlias, TypedDict, cast

Choice: TypeAlias = Literal['a', 'b', 'c', 'd', 'e']


class Question(TypedDict):
    question: str
    options: Mapping[Choice, str]
    answer: Choice


class Test(TypedDict):
    id: str
    questions: List[Question]


class Lesson(TypedDict):
    id: str
    title: str
    content: str


class Subject(TypedDict):
    id: str
    name: str
    lessons: List[Lesson]
    assessment: List[Test]


class Course(TypedDict):
    id: str
    name: str
    subjects: List[Subject]


Courses: TypeAlias = List[Course]

x = cast('Courses', {})
