from typing import TYPE_CHECKING, Any, List, Literal, Mapping
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
        """
        Cria uma instância de :class:`Question` a partir de um dicionário.

        Parameters
        ----------
        data: Mapping[Any, Any]
            Dicionário contendo os dados da questão.

        Returns
        -------
        :class:`Question`
            Instância da questão.
        """
        return cls(**data)


@dataclass
class Test:
    __slots__ = ('id', 'questions')
    id: str
    questions: List[Question]

    @classmethod
    def from_dict(cls, data: dict) -> 'Test':
        """
        Cria uma instância de :class:`Test` a partir de um dicionário.
        Também são criadas instâncias de todos os objetos recursivamente.

        Parameters
        ----------
        data: Mapping[Any, Any]
            Dicionário contendo os dados da avaliação.

        Returns
        -------
        :class:`Test`
            Instância da avaliação com todos os objetos internos criados.
        """
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
    def from_dict(cls, data: Mapping[Any, Any]) -> 'Lesson':
        """
        Cria uma instância de :class:`Lesson` a partir de um dicionário.

        Parameters
        ----------
        data: Mapping[Any, Any]
            Dicionário contendo os dados da aula.

        Returns
        -------
        :class:`Lesson`
            Instância da aula.
        """

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
    def from_dict(cls, data: Mapping[Any, Any]) -> 'Subject':
        """
        Cria uma instância de :class:`Subject` a partir de um dicionário.
        Também são criadas instâncias de todos os objetos recursivamente.

        Parameters
        ----------
        data: Mapping[Any, Any]
            Dicionário contendo os dados da matéria.

        Returns
        -------
        :class:`Subject`
            Instância da matéria com todos os objetos internos criados.
        """
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
    def from_dict(cls, data: Mapping[Any, Any]) -> 'Course':
        """
        Cria uma instância de :class:`Course` a partir de um dicionário.
        Também são criadas instâncias de todos os objetos recursivamente.

        Parameters
        ----------
        data: Mapping[Any, Any]
            Dicionário contendo os dados do curso.

        Returns
        -------
        :class:`Course`
            Instância do curso com todos os objetos internos criados.
        """
        return cls(
            id=data['id'],
            name=data['name'],
            subjects=[
                Subject.from_dict(subject)
                for subject in sorted(data['subjects'], key=lambda x: x['name'])
            ],
        )
