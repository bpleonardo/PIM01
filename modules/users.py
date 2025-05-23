import sys
import time
from typing import Optional
from getpass import getpass
from functools import cached_property

from .data import get_data_file, save_data_file
from .courses import Course
from .passwords import hash_password, check_password
from .utilities import print_menu


class User:
    def __init__(
        self, username: str, age: int, full_name: str, course_id: Optional[str] = None
    ):
        self.age = age
        self.username = username
        self.full_name = full_name
        self._course_id = course_id

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented

        return self.username == other.username

    @property
    def first_name(self):
        return self.full_name.split(' ')[0]

    @property
    def course_id(self):
        return self._course_id

    @course_id.setter
    def course_id(self, value):
        self._course_id = value

        # Precisamos remover o cache do curso, pois ele pode ter mudado.
        del self.course

    @cached_property
    def course(self) -> Optional[Course]:
        if self.course_id is None:
            return None

        courses = get_data_file('cursos.json')
        course = courses[self.course_id]

        return Course.from_dict(course)

    @classmethod
    def find(cls, username: str) -> Optional['User']:
        """
        Busca um usuário pelo nome de usuário.

        Parameters
        ----------
        username: :class:`str`
            Nome de usuário a ser buscado.

        Returns
        -------
        :class:`User`
            O usuário encontrado.
        :class:`None`
            Caso o usuário não seja encontrado.
        """
        users = get_data_file('usuarios.json')
        user = users.get(username)

        if user is None:
            return None

        return cls(**user)

    def _set_password(self, new_password: str):
        logins = get_data_file('logins.json')

        data = logins.get(self.username, {})

        data['password'] = hash_password(new_password)
        logins[self.username] = data

        save_data_file('logins.json', logins)

    def check_password(self, password: str) -> bool:
        """
        Verifica se a senha especificada é igual à armazenada.

        Parameters
        ----------
        password: :class:`str`
            Senha a ser verificada.

        Returns
        -------
        :class:`bool`
            Se a senha é igual à armazenada.
        """
        logins = get_data_file('logins.json')
        user = logins.get(self.username)

        if user is None:
            return False

        return check_password(user['password'], password)

    def write(self):
        """
        Salva os dados do usuário no disco.
        """
        data = {
            'age': self.age,
            'username': self.username,
            'full_name': self.full_name,
            'course_id': self._course_id,
        }

        users = get_data_file('usuarios.json')
        users[self.username] = data

        save_data_file('usuarios.json', users)


def create_account() -> User:
    """
    Cadastra um novo usuário.

    Returns
    -------
    :class:`User`
        O usuário cadastrado.
    """

    print_menu('Realizando cadastro...', 'Aperte Ctrl+C para voltar.', title='cadastro')

    while True:
        full_name = input('Seu nome completo > ').strip().title()
        if full_name != '':
            break

    while True:
        age = input('Sua idade > ')
        if not age.isdigit():
            print('Idade inválida.\n')
            continue

        age = int(age)
        if age < 14:
            print('É necessário ter mais de 14 anos para usar o serviço.')
            sys.exit(0)

        break

    while True:
        username = input('Seu usuário > ')

        if User.find(username) is not None:
            print('Usuário já existe.\n')
            continue

        break

    while True:
        password = getpass('Sua senha (não é exibida)> ')
        password2 = getpass('Repita sua senha > ')

        if password != password2:
            print('As senhas não coincidem.\n')
            continue

        break

    user = User(username, age, full_name)
    user._set_password(password)

    user.write()

    return user


def login_account() -> User:
    """
    Faz o login do usuário.

    Returns
    -------
    :class:`User`
        O usuário logado.
    """
    while True:
        print_menu('Realizando login...', 'Aperte Ctrl+C para voltar.', title='Entrada')
        username = input('Seu usuário > ').strip().lower()

        user = User.find(username)
        if user is None:
            print('Usuário não encontrado.')
            time.sleep(0.5)
            continue

        password = getpass('Sua senha (não é exibida)> ')

        if user.check_password(password):
            return user

        print('Senha incorreta.\n')
        time.sleep(0.5)
