import shutil
from typing import Union, TypeVar, Callable, Iterable, Optional, Sequence

T = TypeVar('T')

# \ESC[2J = Limpa a tela, \033[3J = Apaga o histórico de rolagem, \ESC[H = Move o cursor para o início da tela.
# REF:
CLEAR_SCREEN = '\033[H\033[2J\033[3J'


def print_menu(*texts: str, title: str = '', sep: str = '-'):
    """
    Imprime `texts` na tela, centralizando o título capitalizado entre `sep`.

    Parameters
    ----------
    *texts: :class:`str`
    title: :class:`str`
        Título a ser impresso. Opcional.
    sep: :class:`str`
        Separador a ser utilizado para o título. O padrão é "-".
    """
    terminal_size = shutil.get_terminal_size().columns

    # Limita o tamanho a pelo menos o tamanho do título e no máximo o tamanho do terminal.
    max_len = min(max(len(title) + 8, *(len(text) for text in texts)), terminal_size)

    print(CLEAR_SCREEN, end='')

    if title:
        # Printa o título centralizado entre "="
        title = f' {title} '.upper()
        print(f'{title:{sep}^{max_len}}')
    else:
        print(sep * max_len)

    for text in texts:
        # Printa o texto impedindo que ele ultrapasse o tamanho máximo.
        if text == '':
            print()
            continue
        for text_slice in (text[i : i + max_len] for i in range(0, len(text), max_len)):
            print(text_slice)

    print(sep * max_len)


def get_choice(
    options: Sequence[str],
    prompt: str = 'Escolha uma opção > ',
    default: Optional[str] = None,
) -> Union[str, None]:
    """
    Recebe a entrada do usuário e verifica se a opção escolhida é válida.

    Returns
    -------
    :class:`str`
        A opção escolhida pelo usuário.
    :class:`None`
        Caso o usuário tenha escolhido uma opção inválida.
    """
    while True:
        selected = input(prompt).strip().lower()
        if selected == '':
            return default

        if selected[0] not in options:
            return None

        return selected[0]


def find(
    sequence: Iterable[T], predicate: Callable[[T], bool], default: Optional[T] = None
) -> Optional[T]:
    """
    Encontra o primeiro elemento da sequência que satisfaz a condição dada.

    Parameters
    ----------
    sequence: Iterable[T]
        A sequência a ser pesquisada.
    predicate: Callable[[T], bool]
        A função que define a condição a ser satisfeita.
    default: Optional[T]
        O valor a ser retornado se nenhum elemento satisfizer a condição. O padrão é `None`.

    Returns
    -------
    Optional[T]
        O primeiro elemento que satisfaz a condição, ou `default` se nenhum elemento satisfizer a condição.
    """
    return next((item for item in sequence if predicate(item)), default)
