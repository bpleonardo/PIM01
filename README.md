# PIM

Plataforma de ensino desenvolvida para o Projeto Integrador Multidisciplinar do 1º semestre do curso de Análise e Desenvolvimento de Sistemas da UNIP.

## Execução

O projeto pode ser executado em qualquer versão ainda ativa do Python, ou seja, qualquer versão acima da 3.9.0 (testado no Linux).

A única dependência do programa é o arquivo "cursos.json" localizado na pasta "data" do projeto.
Caso ele não tenha sido disponibilizado, leia sua [especificação](https://github.com/bpleonardo/PIM01/blob/main/SPEC.md#cursosjson) ou seu [esquema](https://github.com/bpleonardo/PIM01/blob/main/json_schemas/cursos.schema.json) para instruções de como gerá-lo.

Para executar, rode o seguinte comando no diretório raiz do projeto:

```sh
python main.py
```

## Desenvolvimento

O desenvolvimento foi feito no Windows com o [Visual Studio Code](https://code.visualstudio.com/), utilizando o _linter_ e formatador [Ruff](https://github.com/astral-sh/ruff/) e o _type checker_ [pyright](https://github.com/microsoft/pyright/).

Recomenda-se a utilização de uma versão recente do Python para desenvolvimento. De preferência acima da versão 3.10.0, pois o projeto utiliza algumas funcionalidades de tipagem não disponíveis em versões anteriores (elas não afetam a execução do programa).

Foi utilizado o programa [jsonschema2md](https://github.com/sbrunner/jsonschema2md/) para a geração do arquivo [SPEC.md](https://github.com/bpleonardo/PIM01/blob/main/SPEC.md), porém a tradução foi feita manualmente.
