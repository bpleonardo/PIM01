import time
from typing import TYPE_CHECKING

from modules.data import get_data_file
from modules.users import User, login_account, create_account
from modules.utilities import get_choice, print_menu

if TYPE_CHECKING:
    from modules.courses import Subject


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

    subjects = sorted(user.course.subjects, key=lambda x: x.name)

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

        print_menu(
            f'Você selecionou {selected_subject.name}.',
            'Isso está correto? [S/n]',
            title='Seleção de matéria',
        )
        choice = get_choice(['s', 'n'], '> ', 's')

        if choice == 's':
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
    input()


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

    subject = select_subject(user)
    subject = next(s for s in user.course.subjects if s.id == subject)

    current_lesson = user.current_lesson.get(subject.id)
    if current_lesson is None:
        current_lesson = subject.lessons[0].id

    if current_lesson[-1] == 'L':
        show_lesson(user, subject, current_lesson)
    elif current_lesson[-1] == 'A':
        show_assessment(user, subject, current_lesson)


if __name__ == '__main__':
    try:  # noqa: SIM105
        main()
    except KeyboardInterrupt:
        # Caso o usuário aperte Ctrl+C, o programa é encerrado sem erros.
        pass
