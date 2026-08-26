# ADR-0002: Adotar português como idioma padrão

## Status

Aceita

## Data

2026-08-25

## Contexto

O responsável pelo desenvolvimento do InvestFácil não domina o idioma inglês. A utilização generalizada de termos em inglês pode gerar dúvidas sobre quais nomes são palavras reservadas da linguagem, exigências de bibliotecas externas ou apenas escolhas realizadas durante o desenvolvimento.

A adoção do português nos elementos controlados pelo projeto facilitará o aprendizado, pois permitirá concentrar a atenção nos conceitos de programação, arquitetura e regras de negócio sem exigir, ao mesmo tempo, a memorização constante de termos em outro idioma.

Essa padronização também facilitará a compreensão, a manutenção e a colaboração de desenvolvedores brasileiros que não dominem o inglês.

A consistência da nomenclatura é considerada mais importante do que a adoção automática do inglês. Um padrão em português, quando aplicado e documentado de maneira uniforme, permitirá melhor organização e maior foco na execução e evolução do projeto.


## Decisão

O português será adotado como idioma padrão para todos os nomes controlados pelo InvestFácil, incluindo:

* pastas e módulos;
* arquivos de código;
* classes;
* funções e métodos;
* variáveis;
* constantes;
* branches;
* mensagens de commit;
* arquivos e conteúdos de documentação;
* termos próprios das regras de negócio.

Os nomes técnicos deverão ser escritos sem acentos, espaços ou caracteres especiais, respeitando os padrões definidos para cada tipo de elemento.

Exemplos:

```text
gerenciador_de_risco.py
dados_de_mercado.py
simulacao_historica/
0002-portugues-como-idioma-padrao.md
```

```python
class GerenciadorDeRisco:
    pass


def calcular_tamanho_da_posicao():
    pass


LIMITE_DE_PERDA_DIARIA = 200
```

## Exceções

Não serão traduzidos os elementos cujo nome seja definido ou exigido pela linguagem, pelas ferramentas ou por bibliotecas externas.

São exemplos de exceções:

* palavras reservadas do Python, como `class`, `def`, `return` e `import`;
* arquivos especiais, como `README.md`, `.gitignore`, `pyproject.toml` e `__init__.py`;
* bibliotecas e tecnologias, como `MetaTrader5`, `Streamlit`, `pandas` e `scikit-learn`;
* classes, funções e constantes fornecidas por dependências externas;
* formatos e extensões padronizados, como `.py`, `.md`, `.json` e `.csv`;
* termos técnicos sem tradução adequada ou cuja tradução prejudique a compreensão.

As exceções deverão conservar o nome oficial para preservar compatibilidade e facilitar consultas à documentação original.

## Alternativas consideradas

### Utilizar inglês em todo o projeto

Rejeitada porque aumentaria a dificuldade de aprendizado e poderia gerar confusão entre nomes escolhidos pelo projeto e elementos obrigatórios da linguagem ou das bibliotecas.

### Utilizar português e inglês sem uma regra definida

Rejeitada porque produziria inconsistência e dificultaria a localização e compreensão dos componentes.

### Utilizar português com exceções documentadas

Aceita porque permite trabalhar com nomes mais compreensíveis, mantendo compatibilidade com padrões e ferramentas externas.

## Consequências positivas

* maior facilidade de compreensão do código;
* redução da dificuldade causada pelo idioma;
* melhor distinção entre escolhas do projeto e exigências externas;
* maior foco no aprendizado de programação e arquitetura;
* facilidade de manutenção por colaboradores brasileiros;
* nomenclatura alinhada às regras de negócio do InvestFácil.

## Consequências negativas

* necessidade de traduzir a nova estrutura já criada;
* coexistência temporária com arquivos antigos nomeados em inglês;
* necessidade de atenção ao consultar documentações e exemplos em inglês;
* menor familiaridade imediata para desenvolvedores estrangeiros;
* possibilidade de alguns termos técnicos permanecerem em inglês por exceção.

## Plano de adoção

A adoção do português será realizada gradualmente:

1. renomear as pastas da nova arquitetura;
2. atualizar os documentos que mencionam os nomes anteriores;
3. atualizar o índice e as regras de nomenclatura dos ADRs;
4. utilizar português em todo novo código controlado pelo projeto;
5. manter temporariamente os arquivos do protótipo com seus nomes atuais;
6. traduzir os arquivos antigos somente durante sua migração para a nova arquitetura;
7. executar testes após cada etapa de migração.

Os arquivos antigos não serão renomeados em massa, pois isso poderia quebrar imports e dificultar a identificação de erros.

## Critérios de revisão

Esta decisão poderá ser revisada se o InvestFácil passar a contar com uma equipe internacional, exigir integração com padrões externos incompatíveis ou se a nomenclatura em português produzir dificuldades técnicas comprovadas.

Qualquer revisão deverá ser registrada em um novo ADR.
