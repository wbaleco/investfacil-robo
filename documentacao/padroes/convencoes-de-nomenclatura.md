# Convenções de nomenclatura

## Objetivo

O InvestFácil precisa seguir um padrão de nomenclatura porque a padronização facilita a identificação e a compreensão dos diferentes elementos do projeto. Por meio dos nomes utilizados, os desenvolvedores poderão reconhecer com mais facilidade se determinado elemento é uma classe, uma função, uma variável, uma constante, um arquivo ou uma pasta. Isso também contribuirá para a organização, a localização dos componentes e a manutenção do projeto.

## Princípios gerais

Os nomes controlados pelo InvestFácil deverão ser escritos em português para facilitar a compreensão do responsável pelo projeto e dos demais desenvolvedores brasileiros.

A nomenclatura deverá seguir os seguintes princípios:

* não utilizar acentos ou caracteres especiais em nomes técnicos;
* não utilizar espaços em nomes de arquivos, pastas ou elementos do código;
* separar as palavras com hífen ou sublinhado, conforme a convenção aplicável a cada elemento;
* utilizar nomes claros que representem a responsabilidade da classe, função, variável, arquivo, pasta ou outro componente;
* evitar abreviações que não sejam amplamente conhecidas ou que possam gerar dúvidas;
* manter o nome oficial dos elementos exigidos pelo Python, por ferramentas ou por bibliotecas externas.

## Código Python

### Arquivos e módulos
Os arquivos e módulos Python deverão utilizar o padrão `snake_case`, formado por letras minúsculas e palavras separadas por sublinhado.

Os nomes deverão indicar claramente a responsabilidade do arquivo ou módulo.

Exemplos:

```text
gerenciador_de_risco.py
dados_de_mercado.py
simulacao_historica.py
calculadora_de_tamanho_da_posicao.py
```

Não utilizar:

```text
GerenciadorDeRisco.py
gerenciador-de-risco.py
gestão_de_risco.py
gerenciador de risco.py
```
### Funções, métodos e variáveis


As funções, os métodos e as variáveis deverão utilizar o padrão `snake_case`, com letras minúsculas e palavras separadas por sublinhado.

Os nomes de funções e métodos deverão indicar uma ação, preferencialmente começando com um verbo. Os nomes de variáveis deverão indicar claramente o valor ou objeto armazenado.

Exemplos:

```python
def calcular_tamanho_da_posicao():
    pass


def validar_limite_de_perda():
    pass


saldo_disponivel = 1000
quantidade_de_contratos = 2
```

Deverão ser evitados nomes genéricos ou pouco explicativos, como:

```python
def fazer():
    pass


valor = 1000
dados = 2
```
### Classes
As classes deverão utilizar o padrão `PascalCase`. Cada palavra deverá começar com letra maiúscula, sem espaços, hífens, sublinhados ou acentos.

Os nomes deverão representar claramente a entidade, o conceito ou a responsabilidade da classe.

Exemplos:

```python
class GerenciadorDeRisco:
    pass


class OrdemDeNegociacao:
    pass


class ResultadoDaSimulacaoHistorica:
    pass


class ProvedorDeDadosDeMercado:
    pass
```
### Constantes

As constantes deverão utilizar o padrão `SCREAMING_SNAKE_CASE`, formado por letras maiúsculas e palavras separadas por sublinhado.

Elas deverão possuir nomes claros e representar valores que não devem ser alterados durante a execução normal do sistema.

Exemplos:

```python
LIMITE_DE_PERDA_DIARIA = 200
QUANTIDADE_MAXIMA_DE_CONTRATOS = 2
AMBIENTE_DE_OPERACAO = "demonstracao"
OPERACAO_REAL_PERMITIDA = False
```

### Pastas e pacotes Python

As pastas que representam pacotes Python deverão utilizar o padrão `snake_case`, formado por letras minúsculas e palavras separadas por sublinhado.

Os nomes deverão indicar claramente a responsabilidade ou o conteúdo do pacote.

Exemplos:

```text
gestao_de_risco/
dados_de_mercado/
aprendizado_de_maquina/
simulacao_historica/
```
### Testes automatizados

As funções de testes automatizados deverão utilizar o padrão `snake_case` e começar obrigatoriamente com o prefixo `test_`, conforme a convenção do `pytest`.

O restante do nome deverá descrever claramente o comportamento ou resultado esperado.

Exemplos:

```python
def test_calcular_tamanho_da_posicao_corretamente():
    pass


def test_bloquear_operacao_quando_o_limite_de_perda_for_atingido():
    pass


def test_rejeitar_ordem_em_conta_real():
    pass


def test_permitir_ordem_em_conta_de_demonstracao():
    pass
```
## Branches do Git

As branches deverão possuir um prefixo que identifique o tipo de alteração, seguido por uma barra e uma descrição curta em português.

A descrição deverá utilizar letras minúsculas, sem acentos ou caracteres especiais, com as palavras separadas por hífen.

Formato:

```text
prefixo/descricao-curta

feature: criação de funcionalidade;
fix: correção de problema;
docs: alteração exclusiva de documentação;
refactor: reorganização do código sem alteração intencional de comportamento;
test: criação ou alteração de testes;
chore: manutenção técnica sem alteração funcional.

feature/criar-gerenciador-de-risco
fix/corrigir-calculo-da-posicao
docs/atualizar-documentacao-da-arquitetura
refactor/refatorar-simulacao-historica
test/adicionar-testes-de-gestao-de-risco
chore/configurar-formatador
```
## Mensagens de commit

feat: adiciona gerenciador de risco
fix: corrige cálculo do tamanho da posição
docs: atualiza documentação da arquitetura
refactor: refatora motor de simulação histórica

As mensagens de commit deverão utilizar um prefixo que identifique o tipo de alteração, seguido de dois-pontos, espaço e uma descrição objetiva em português.

Formato:

```text
tipo: descrição da alteração

A descrição deverá:

ser escrita em português;
começar com letra minúscula;
utilizar um verbo no presente;
informar objetivamente a alteração realizada;
não terminar com ponto final.

Prefixos adotados:

feat: inclusão de funcionalidade;
fix: correção de problema;
docs: alteração exclusiva de documentação;
refactor: reorganização do código sem alteração intencional de comportamento;
test: criação ou alteração de testes;
chore: manutenção técnica sem alteração funcional.

Exemplos:

feat: adiciona gerenciador de risco
fix: corrige cálculo do tamanho da posição
docs: atualiza documentação da arquitetura
refactor: refatora motor de simulação histórica
test: adiciona testes de limite de perda
chore: configura formatador de código
```
## Arquivos de documentação

Os arquivos de documentação deverão utilizar letras minúsculas, com palavras em português separadas por hífen e extensão `.md`.

Os nomes deverão indicar claramente o assunto documentado e não poderão conter espaços, acentos, sublinhados ou caracteres especiais.

Exemplos:

```text
guia-de-instalacao.md
arquitetura-do-sistema.md
politica-de-seguranca.md
plano-de-migracao.md
```
## Exceções

Não deverão ser traduzidos ou alterados os nomes definidos por linguagens, bibliotecas, ferramentas, protocolos ou formatos externos.

São exemplos:

- palavras reservadas do Python, como `class`, `def`, `return` e `import`;
- arquivos especiais, como `README.md`, `.gitignore`, `pyproject.toml` e `__init__.py`;
- bibliotecas e tecnologias, como `pandas`, `pytest`, `Streamlit`, `MetaTrader5` e `scikit-learn`;
- funções, classes e constantes fornecidas por dependências externas;
- extensões e formatos padronizados, como `.py`, `.md`, `.json` e `.csv`;
- prefixos técnicos adotados para branches e commits.

Quando houver dúvida sobre a tradução de um termo técnico, deverão ser considerados:

1. a existência de uma tradução clara e amplamente compreendida;
2. a compatibilidade com ferramentas e bibliotecas externas;
3. a facilidade de consulta à documentação oficial;
4. a consistência com os nomes já utilizados no InvestFácil.

A exceção deverá ser registrada neste documento quando passar a fazer parte do padrão do projeto.

## Resumo das convenções

| Elemento | Padrão | Exemplo |
|---|---|---|
| Arquivo Python | `snake_case` | `gerenciador_de_risco.py` |
| Pasta ou pacote Python | `snake_case` | `gestao_de_risco/` |
| Função ou método | `snake_case` | `calcular_tamanho_da_posicao` |
| Variável | `snake_case` | `saldo_disponivel` |
| Classe | `PascalCase` | `GerenciadorDeRisco` |
| Constante | `SCREAMING_SNAKE_CASE` | `LIMITE_DE_PERDA_DIARIA` |
| Função de teste | prefixo `test_` | `test_rejeitar_ordem_em_conta_real` |
| Arquivo de documentação | palavras com hífen | `politica-de-seguranca.md` |
| Branch | prefixo e palavras com hífen | `feature/criar-gerenciador-de-risco` |
| Commit | tipo e descrição em português | `feat: adiciona gerenciador de risco` |