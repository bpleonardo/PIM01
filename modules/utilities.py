from typing import Union, Optional, Sequence

# \ESC[2J = Limpa a tela, \ESC[H = Move o cursor para o início da tela.
# REF: https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
CLEAR_SCREEN = '\033[2J\033[H'


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
    max_len = max(len(text) for text in texts)

    print(CLEAR_SCREEN, end='')

    if title:
        # Printa o título centralizado entre "="
        title = f' {title} '.upper()
        print(f'{title:{sep}^{max_len}}')
    else:
        print(sep * max_len)

    for text in texts:
        print(text)

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
