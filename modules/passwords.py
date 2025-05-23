import random
import hashlib


def hash_password(password: str):
    """
    Gera um hash da senha utilizando SHA256 e um salt de 8 bytes.

    Parameters
    ----------
    password: :class:`str`
        Senha a ser hasheada.

    Returns
    -------
    :class:`str`
        O hash da senha.
    """

    salt = random.randbytes(8)

    salted_pwd = password.encode() + salt

    # sha256 não é recomendável para senhas.
    # Apesar de estarmos usando "salt", a velocidade de hash é muito alta,
    # portanto o ideal seria utilizar algorítmos como "argon2" ou "bcrypt".
    hashed = hashlib.sha256(salted_pwd).hexdigest()

    # Aqui, "g" é usado como separador pois não é um caractere hexadecimal.
    return f'{hashed}g{salt.hex()}'


def check_password(hash: str, password: str):
    """
    Verifica se a senha especificada corresponde ao hash.

    Parameters
    ----------
    hash: :class:`str`
        Hash da senha a ser verificada.
    password: :class:`str`
        Senha a ser verificada.

    Returns
    -------
    :class:`bool`
        Se as duas senhas são iguais.
    """
    hashed, salt = hash.split('g')
    salted_pwd = password.encode() + bytes.fromhex(salt)
    return hashlib.sha256(salted_pwd).hexdigest() == hashed
