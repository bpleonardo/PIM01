import time
from typing import TYPE_CHECKING, Tuple, Mapping, Sequence

from modules.data import get_data_file
from modules.users import User, login_account, create_account
from modules.utilities import find, get_choice, print_menu

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

    choice = get_choice(['c', 'l', 's'], '> ', 'l')

    try:
        if choice == 'l':
            return login_account()
        if choice == 'c':
            return create_account()
        if choice == 's':
            # Precisamos utilizar RuntimeError pois KeyboardInterrupt está sendo capturado
            # para implementação do voltar no menu de cadastro e login.
            # O valor 115 é um código arbitrário para verificação.
            raise RuntimeError(0x115)
    except KeyboardInterrupt:
        return None
    except RuntimeError as e:
        if e.args[0] == 0x115:
            raise KeyboardInterrupt() from None
        raise  # Devevolver o erro original se não for o caso de voltar.


def set_user_course(user: User):
    """
    Seleciona um curso para o usuário.

    Parameters
    ----------
    user: :class:`User`
        O usuário que está selecionando o curso.
    """
    courses = tuple(
        sorted(get_data_file('data/cursos.json').values(), key=lambda x: x['name'])
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
        '',
        'Aperte Enter para continuar.',
        title='Seleção de curso',
    )
    input()


def select_subject(user: User) -> 'Subject':
    """
    Pede para o usuário selecionar uma matéria do curso.

    Parameters
    ----------
    user: :class:`User`
        O usuário que está selecionando a matéria.

    Returns
    -------
    :class:`Subject`
        A matéria selecionada pelo usuário.
    """
    assert user.course is not None  # Diminuir o tipo.

    texts = ['Selecione a disciplina desejada:', '']

    subjects = user.course.subjects

    for i, subject in enumerate(subjects):
        texts.append(f'[{i + 1}] {subject.name}')

    texts.append('[0] Sair do programa.')

    while True:
        print_menu(*texts, title='Seleção de matéria')

        choice = get_choice([str(i) for i in range(len(subjects) + 1)], '> ')
        if choice is None:
            print('Opção inválida.')
            time.sleep(0.5)
            continue

        choice = int(choice)

        if choice == 0:
            raise KeyboardInterrupt()

        selected_subject = subjects[choice - 1]

        break

    return selected_subject


def show_lesson(user: User, subject: 'Subject', lesson_id: str):
    """
    Mostra o conteúdo de uma aula para o usuário e atualiza seu progresso.

    Parameters
    ----------
    user: :class:`User`
        O usuário que está lendo a aula.
    subject: :class:`Subject`
        A matéria da qual a aula faz parte.
    lesson_id: :class:`str`
        O ID da aula que será exibida.
    """
    lesson = find(subject.lessons, lambda x: x.id == lesson_id)
    assert lesson is not None

    action = (
        'ir para próxima aula'
        if user.current_lesson.get(subject.id) != '-'
        else 'voltar'
    )

    print_menu(
        lesson.content,
        '',
        f'Pressione Enter para {action}.',
        'Pressione Ctrl+C para sair do programa.',
        title=lesson.title,
    )

    if user.current_lesson.get(subject.id) != '-':
        next_lesson = find(subject.lessons, lambda x: x.index == lesson.index + 1)
        user.current_lesson[subject.id] = (
            next_lesson.id if next_lesson else subject.test.id
        )

        user.write()

    input()


def show_test(user: User, subject: 'Subject'):
    """
    Exibe a avaliação de uma matéria para o usuário, coleta as respostas e calcula a nota.

    Parameters
    ----------
    user: :class:`User`
        O usuário que está fazendo a avaliação.
    subject: :class:`Subject`
        A matéria da qual a avaliação faz parte.
    lesson_id: :class:`str`
        Não é utilizado.
    """
    test = subject.test
    print_menu(
        'Você finalizou todas as aulas.',
        '',
        'Aperte Enter para começar a avaliação.',
        title=subject.name,
    )

    input()

    results = {}

    for question in test.questions:
        answer = show_question(question, test)
        results[question.index] = (answer, question.answer)

    grade = round(
        sum(
            question.weight
            for question in test.questions
            if results[question.index][0] == question.answer
        )
        / 100,
        5,
    )
    if user.grades.get(subject.id) is None:
        user.grades[subject.id] = grade * 100
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

    start_revision(test.questions, results)

    action = (
        'escolher outra matéria'
        if user.current_lesson.get(subject.id) != '-'
        else 'voltar'
    )

    print_menu(
        'Prova revisada.',
        '',
        f'Aperte Enter para {action}.',
        title=subject.name,
    )

    input()


def show_question(question: 'Question', test: 'Test') -> str:
    """
    Exibe uma questão da avaliação e coleta a resposta do usuário.

    Parameters
    ----------
    question: :class:`Question`
        A questão a ser exibida.
    test: :class:`Test`
        A avaliação à qual a questão pertence.

    Returns
    -------
    :class:`str`
        A resposta escolhida pelo usuário.
    """
    while True:
        print_menu(
            question.question,
            '',
            *(f'[{option}] {content}' for option, content in question.options.items()),
            title=f'Questão {question.index + 1} de {len(test.questions)}.',
        )

        choice = get_choice(tuple(question.options.keys()), '> ')
        if choice is not None:
            return choice
        print('Opção inválida.')
        time.sleep(0.5)


def start_revision(
    questions: Sequence['Question'], results: Mapping[int, Tuple['Choice', 'Choice']]
):
    """
    Inicia a revisão das questões respondidas pelo usuário, mostrando as respostas
    corretas e incorretas.

    Parameters
    ----------
    questions: Sequence[:class:`Question`]
        As questões da avaliação que foram respondidas.
    results: Mapping[:class:`int`, Tuple[:class:`Choice`, :class:`Choice`]]
        Um dicionário que mapeia o índice da questão para uma tupla contendo a resposta
        selecionada pelo usuário e a resposta correta.
    """
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


def show_all_lessons(user: User, subject: 'Subject'):
    """
    Mostra todas as aulas de uma matéria para o usuário, permitindo que ele
    escolha uma para revisar ou fazer a avaliação.

    Parameters
    ----------
    user: :class:`User`
        O usuário que está revisando as aulas.
    subject: :class:`Subject`
        A matéria cujas aulas serão revisadas.
    """
    texts = [
        'Você já assistiu todas as aulas desta matéria.',
        '',
        'Selecione a aula que deseja revisar:',
    ]

    test_index = subject.lessons[-1].index + 1
    exit_index = test_index + 1

    texts.extend(f'[{lesson.index}] {lesson.title}' for lesson in subject.lessons)
    texts.extend((f'[{test_index}] Prova', f'[{exit_index}] Voltar'))

    while True:
        print_menu(*texts, title=subject.name)
        choice = get_choice(tuple(map(str, range(1, exit_index + 1))), '> ')
        if choice is None:
            print('Opção inválida.')
            time.sleep(0.5)
            continue

        choice = int(choice)

        if choice == exit_index:
            return

        if choice == test_index:
            show_test(user, subject)
        else:
            lesson = find(subject.lessons, lambda le: le.index == choice)  # noqa: B023
            assert lesson is not None

            show_lesson(user, subject, lesson.id)


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
            '[s]air',
            title='Entrada',
        )

        user = create_or_login_user()

    print_menu(f'Bem vindo, {user.first_name}', title='Entrada')
    time.sleep(1)

    if user.course_id is None:
        set_user_course(user)

    assert user.course is not None  # Diminuir o tipo.

    print_menu('Você está matriculado no curso', user.course.name, title='Entrada')
    time.sleep(1)

    while True:
        subject = select_subject(user)

        while True:
            user.update()

            current_lesson = user.current_lesson.get(subject.id, subject.lessons[0].id)
            if current_lesson[-1] == 'L':
                show_lesson(user, subject, current_lesson)
            elif current_lesson[-1] in ('-', 'A'):
                break

        if current_lesson[-1] == '-':
            show_all_lessons(user, subject)
        if current_lesson[-1] == 'A':
            show_test(user, subject)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Caso o usuário aperte Ctrl+C, o programa é encerrado sem erros.
        print_menu('Saindo...')
    except Exception:  # noqa: BLE001
        print_menu(
            'Ocorreu um erro inesperado.',
            'Por favor, entre em contato com o suporte.',
            title='Erro',
        )
