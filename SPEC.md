# Especificações dos arquivos de dados.

## [cursos.json](https://github.com/bpleonardo/PIM01/blob/main/json_schemas/cursos.schema.json)

_Representa os cursos e suas respectivas disciplinas, aulas e avaliações._
_**Este arquivo deve estar presente para a execução do programa.**_

### Propriedades

- **`^[A-Z]{3}$`** _(objeto)_: Representa um curso. A chave é o ID do curso, consistindo em 3 iniciais em maiúsculas.

  - **`id`** _(string, obrigatório)_: O ID do curso, consistindo em 3 iniciais em maiúsculas. Deve seguir a expressão regular: `^[A-Z]{3}$`.

    Exemplos:

    ```json
    "ADS"
    ```

    ```json
    "EDF"
    ```

  - **`name`** _(string, obrigatório)_: O nome do curso.
  - **`subjects`** _(lista, obrigatório)_: Lista de disciplinas do curso.

    - **Itens** _(objeto)_,

      - **`id`** _(string, obrigatório)_: O ID da disciplina, consistindo em 2 letras iniciais do curso e 3 letras iniciais da disciplina. Deve seguir a expressão regular: `^[A-Z]{5}$`.

        Exemplos:

        ```json
        "ADPLC"
        ```

        ```json
        "EDBIE"
        ```

      - **`name`** _(string, obrigatório)_: O nome da disciplina.
      - **`max_grade`** _(número, obrigatório)_: A nota máxima que pode ser atribuída na disciplina. Mínimo: `0`.
      - **`lessons`** _(lista, obrigatório)_: Lista de aulas da disciplina.

        - **Itens** _(objeto)_

          - **`id`** _(string, obrigatório)_: O ID da aula, consistindo no ID da matéria seguido de um número sequencial de 3 digitos seguido da letra L. Deve seguir a expressão regular: `^[A-Z]{5}[0-9]{3}L$`.

            Exemplos:

            ```json
            "ADPLC001L"
            ```

            ```json
            "EDBIE003L"
            ```

          - **`title`** _(string, obrigatório)_: O título da aula.
          - **`content`** _(string, obrigatório)_: O conteúdo da aula.

      - **`assessment`** _(objeto, obrigatório)_: A avaliação da disciplina.

        - **`id`** _(string, obrigatório)_: O ID da avaliação, consistindo no ID da matéria seguido de um número sequencial de 3 digitos seguido da letra A. Deve seguir a expressão regular: `^[A-Z]{5}[0-9]{3}A$`.

          Exemplos:

          ```json
          "ADPLC001A"
          ```

          ```json
          "EDBIE003A"
          ```

        - **`questions`** _(lista, obrigatório)_: Lista de questões da avaliação.
          - **Itens** _(objeto)_:
            - **`index`** _(inteiro, obrigatório)_: O índice da questão na avaliação. Mínimo: `0`.
            - **`weight`** _(número, obrigatório)_: O peso da questão na avaliação. Deve ser um número entre 0 a 100 representando a porcentagem da nota total.
            - **`question`** _(string, obrigatório)_: O texto da questão.
            - **`options`** _(objeto, obrigatório)_: As opções de resposta da questão.
              - **`a`** _(string, obrigatório)_: Opção A da questão.
              - **`b`** _(string, obrigatório)_: Opção B da questão.
              - **`c`** _(string, obrigatório)_: Opção C da questão.
              - **`d`** _(string, obrigatório)_: Opção D da questão.
              - **`e`** _(string, obrigatório)_: Opção E da questão.
            - **`answer`** _(string, obrigatório)_: A resposta correta da questão. Deve ser um de `["a", "b", "c", "d", "e"]`.

## [logins.json](https://github.com/bpleonardo/PIM01/blob/main/json_schemas/logins.schema.json)

_Representa os dados de login dos usuários do sistema, incluindo o hash da senha e o salt._
_**Este arquivo é gerenciado pelo programa e você NÃO deve editar diretamente.**_

### Propriedades

- **`^.+$`** _(string)_: A chave representa um nome de usuário cadastrado no sistema, e o valor é o hash da senha com o salt. Deve ter 81 caracteres. Deve seguir a expressão regular: `^[0-9a-fA-F]{64}g[0-9a-fA-F]{16}$`

## [usuarios.json](https://github.com/bpleonardo/PIM01/blob/main/json_schemas/usuarios.schema.json)

_Representa os dados dos usuários do sistema, incluindo informações pessoais, notas e aulas atuais._
_**Este arquivo é gerenciado pelo programa e você NÃO deve editar diretamente.**_

### Propriedades

- **`^.+$`** _(objeto)_: A chave é o nome de usuário do aluno.

  - **`age`** _(inteiro, obrigatório)_: A idade do aluno. Mínimo: `14`.
  - **`username`** _(string, obrigatório)_: O nome de usuário do aluno.
  - **`full_name`** _(string, obrigatório)_: O nome completo do aluno.
  - **`gender`** _(string ou null, obrigatório)_: O gênero do aluno. `null` caso não especificado. Deve ser um de `["h", "m", null]`.
  - **`city`** _(string, obrigatório)_: A cidade onde o aluno reside.
  - **`course_id`** _(string ou null, obrigatório)_: O ID do curso em que o aluno está matriculado. `null` caso não esteja matriculado. Deve seguir a expressão regular: `^[A-Z]{3}$`.

    Exemplos:

    ```json
    "ADS"
    ```

    ```json
    "EDF"
    ```

  - **`grades`** _(objeto, obrigatório)_: As notas do aluno nas disciplinas.
    - **`^[A-Z]{5}$`** _(número)_: A chave é o ID da disciplina e o valor é a nota do aluno na disciplina em forma de porcentagem. Mínimo: `0`. Máximo: `100`.
  - **`current_lesson`** _(objeto, obrigatório)_: As aulas ou provas que o aluno está fazendo atualmente.

    - **`^[A-Z]{5}$`** _(string)_: A chave é o ID da disciplina e o valor é o id da aula ou prova. Caso o aluno já tenha terminado todas as aulas e provas, o valor será `"-"`. Deve seguir a expressão regular: `^(([A-Z]{5}[0-9]{3}(A|L))|-)$`.

      Exemplos:

      ```json
      "ADPLC002L"
      ```

      ```json
      "ADPLC001A"
      ```

> Arquivo gerado com a ajuda de [jsonschema2md](https://github.com/sbrunner/jsonschema2md/tree/master).
