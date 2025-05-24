import time
from typing import TYPE_CHECKING, Tuple, Mapping, Sequence

from modules.data import get_data_file
from modules.users import User, login_account, create_account
from modules.utilities import get_choice, print_menu

if TYPE_CHECKING:
    from modules.courses import Test, Choice, Subject, Question


def create_or_login_user():
    """
    Cadastra ou faz login de um usuário.

    Returns
    -------
    :class:`User`
        O usuário cadastrado ou logado.
    :class:`None`
        Caso o usuário interrompa o processo de cadastro ou login.
    """

    choice = get_choice(['c', 'l'], '> ', 'l')

    try:
        if choice == 'l':
            return login_account()
        if choice == 'c':
            return create_account()
    except KeyboardInterrupt:
        return None

    raise RuntimeError('Você não deveria ver isso...')


def set_user_course(user: User):
    """
    Seleciona um curso para o usuário.

    Parameters
    ----------
    user: :class:`User`
        O usuário que está selecionando o curso.
    """
    courses = tuple(
        sorted(get_data_file('cursos.json').values(), key=lambda x: x['name'])
    )

    texts = [
        'Parece que você não está matrículado em nenhum curso.',
        '',
        'Selecione o curso desejado:',
    ]
    for i, course in enumerate(courses):
        texts.append(f'[{i + 1}] {course["name"]}')

    while True:
        print_menu(*texts, title='Seleção de curso')

        choice = get_choice([str(i) for i in range(1, len(courses) + 1)], '> ')
        if choice is None:
            print('Opção inválida.')
            time.sleep(0.5)
            continue

        choice = int(choice)

        selected_course = courses[choice - 1]

        print_menu(
            f'Você selecionou {selected_course["name"]}.',
            'Isso está correto? [S/n]',
            title='Seleção de curso',
        )
        choice = get_choice(['s', 'n'], '> ', 's')

        if choice == 's':
            break

    user.course_id = selected_course['id']
    user.write()

    print_menu(
        f'{user.first_name}, você foi matriculado no curso "{selected_course["name"]}".',
        'Aperte Enter para continuar.',
        title='Seleção de curso',
    )
    input()


def select_subject(user: User) -> str:
    assert user.course is not None  # FIXME: Remover em produção.

    texts = ['Selecione a disciplina desejada:', '']

    subjects = user.course.subjects

    for i, subject in enumerate(subjects):
        texts.append(f'[{i + 1}] {subject.name}')

    while True:
        print_menu(*texts, title='Seleção de matéria')

        choice = get_choice([str(i) for i in range(1, len(subjects) + 1)], '> ')
        if choice is None:
            print('Opção inválida.')
            time.sleep(0.5)
            continue

        choice = int(choice)

        selected_subject = subjects[choice - 1]

        break

    return selected_subject.id


def show_lesson(user: User, subject: 'Subject', lesson_id: str):
    lesson = next(i for i in subject.lessons if i.id == lesson_id)
    print_menu(
        lesson.content,
        '',
        'Pressione Enter para ir para a próxima aula.',
        title=lesson.title,
    )

    try:
        user.current_lesson[subject.id] = next(
            i for i in subject.lessons if i.index == lesson.index + 1
        ).id
    except StopIteration:
        # Não temos mais aulas.
        # A prova é a próxima.
        user.current_lesson[subject.id] = subject.assessment.id

    user.write()

    input()


def show_assessment(user: User, subject: 'Subject', _):
    assessment = subject.assessment
    print_menu(
        'Você finalizou todas as aulas.',
        '',
        'Aperte Enter para começar a prova.',
        title=subject.name,
    )

    input()

    results = {}

    for question in assessment.questions:
        answer = show_question(question, assessment)
        results[question.index] = (answer, question.answer)

    grade = round(
        sum(
            question.weight
            for question in assessment.questions
            if results[question.index][0] == question.answer
        )
        / 100,
        3,
    )
    user.grades[subject.id] = grade
    user.current_lesson[subject.id] = '-'
    user.write()

    grade = round(grade * subject.max_grade, 1)

    print_menu(
        'Prova finalizada.',
        f'Você tirou {grade}/{subject.max_grade}.',
        '',
        'Aperte Enter para fazer a revisão.',
        title=subject.name,
    )

    input()

    start_revision(assessment.questions, results)

    print_menu(
        'Prova revisada.',
        'Aperte Enter para selecionar outra matéria.',
        title=subject.name,
    )

    input()


def start_revision(
    questions: Sequence['Question'], results: Mapping[int, Tuple['Choice', 'Choice']]
):
    for question in questions:
        selected_answer = results[question.index][0]
        right_answer = results[question.index][1]

        texts = [question.question, '']
        if selected_answer == right_answer:
            texts.extend(
                (
                    'Você acertou esta questão.',
                    '',
                    'Resposta correta:',
                    f'[{right_answer}] {question.options[right_answer]}',
                )
            )
        else:
            texts.extend(
                (
                    'Você errou esta questão.',
                    '',
                    'Sua resposta:',
                    f'[{selected_answer}] {question.options[selected_answer]}',
                    '',
                    'Resposta correta:',
                    f'[{right_answer}] {question.options[right_answer]}',
                )
            )

        texts.extend(('', 'Aperte Enter para continuar.'))

        print_menu(
            *texts,
            title=f'Questão {question.index + 1} de {len(questions)}.',
        )
        input()


def show_question(question: 'Question', assessment: 'Test') -> str:
    while True:
        print_menu(
            question.question,
            '',
            *(f'[{option}] {content}' for option, content in question.options.items()),
            title=f'Questão {question.index + 1} de {len(assessment.questions)}.',
        )

        choice = get_choice(tuple(question.options.keys()), '> ')
        if choice is not None:
            return choice
        print('Opção inválida.')
        time.sleep(0.5)


def main():
    user = None
    while user is None:
        print_menu(
            'Bem ao vindo ao PIM (Plataforma Integrada de Mentoria).',
            'Para acessar a plataforma, é necessário fazer login.',
            '',
            'Selecione uma opção:',
            '[c]adastro',
            '[L]ogin',
            title='Entrada',
        )

        user = create_or_login_user()

    print_menu(f'Bem vindo, {user.first_name}', title='Entrada')
    time.sleep(1)

    if user.course_id is None:
        set_user_course(user)

    assert user.course is not None  # FIXME: Remover em produção.

    print_menu('Você está matriculado no curso', user.course.name, title='Entrada')
    time.sleep(1)

    while True:
        subject = select_subject(user)
        subject = next(s for s in user.course.subjects if s.id == subject)

        while True:
            user.update()

            current_lesson = user.current_lesson.get(subject.id)
            if current_lesson is None:
                current_lesson = subject.lessons[0].id
            if current_lesson[-1] == 'L':
                show_lesson(user, subject, current_lesson)
            elif current_lesson[-1] == 'A':
                break

        show_assessment(user, subject, current_lesson)


if __name__ == '__main__':
    try:  # noqa: SIM105
        main()
    except KeyboardInterrupt:
        # Caso o usuário aperte Ctrl+C, o programa é encerrado sem erros.
        pass
