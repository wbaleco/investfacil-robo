# Registros de Decisões Arquiteturais

## Objetivo

Esta documentação foi criada para registrar as decisões tomadas durante o desenvolvimento do InvestFácil e explicar os motivos de cada escolha.

Com o passar do tempo, ela permitirá consultar o histórico do projeto, compreender a finalidade de cada componente e recordar por que determinada solução foi adotada.

As decisões não devem depender apenas da memória, pois detalhes importantes podem ser esquecidos ao longo da evolução do sistema. O registro escrito também facilitará futuras revisões, manutenções e mudanças no projeto.

## O que é um ADR

Um ADR é um documento utilizado para registrar uma decisão arquitetural. Ele descreve o problema existente, a solução adotada, as alternativas consideradas e os motivos que levaram à escolha.

O documento também registra as consequências esperadas da decisão, permitindo compreender futuramente não apenas o que foi escolhido, mas por que determinada solução foi considerada a mais adequada.

## Quando criar um ADR

Um ADR deverá ser criado quando houver uma decisão com impacto relevante e duradouro sobre a arquitetura, a segurança, os dados ou a evolução do InvestFácil.

São exemplos de decisões que precisam de ADR:

* escolha da arquitetura do sistema;
* escolha ou substituição do banco de dados;
* definição da forma de integração com o MetaTrader 5;
* definição dos mecanismos obrigatórios de gestão de risco;
* escolha das tecnologias principais do projeto;
* alteração das responsabilidades entre os módulos.

Mudanças simples, como alterar cores, textos, espaçamentos ou a posição de um elemento na tela, normalmente não precisam de ADR, pois produzem pouco ou nenhum impacto estrutural.

Em caso de dúvida, deverá ser avaliado se a decisão:

* afeta vários módulos;
* apresenta alternativas relevantes;
* é difícil ou custosa de reverter;
* produz consequências de longo prazo;
* interfere na segurança ou na confiabilidade das operações.

Se uma ou mais dessas condições estiverem presentes, a decisão deverá ser registrada.

## Status possíveis

Cada ADR deverá possuir um status que represente a situação atual da decisão:

| Status            | Significado                                                              |
| ----------------- | ------------------------------------------------------------------------ |
| **Proposta**      | A decisão está sendo analisada e ainda não foi aprovada.                 |
| **Aceita**        | A decisão foi aprovada e deve orientar o desenvolvimento do projeto.     |
| **Rejeitada**     | A decisão foi analisada, mas não será adotada.                           |
| **Substituída**   | Uma nova decisão arquitetural tomou o lugar da decisão anterior.         |
| **Descontinuada** | A decisão deixou de ser aplicável e não foi necessariamente substituída. |

Quando o status de uma decisão mudar, o ADR original deverá ser preservado. Caso uma decisão seja substituída, o documento deverá indicar qual novo ADR passou a valer.

## Convenção de nomes

Os arquivos de ADR deverão seguir o padrão:

`NNNN-nome-curto-da-decisao.md`

A nomenclatura deverá respeitar as seguintes regras:

* utilizar numeração sequencial com quatro dígitos;
* não reutilizar nem renumerar identificadores;
* utilizar somente letras minúsculas;
* utilizar nomes técnicos em inglês;
* separar palavras com hífen;
* não utilizar espaços, acentos ou caracteres especiais;
* descrever a decisão de forma curta e específica;
* utilizar a extensão `.md`.

Exemplos:

* `0001-modular-monolith.md`;
* `0002-demo-account-only.md`;
* `0003-src-layout.md`.

O título e o conteúdo dos documentos deverão ser escritos em português, mesmo quando o nome técnico do arquivo estiver em inglês.

## Regras

Os registros de decisões arquiteturais deverão seguir estas regras:

* um ADR aceito não deverá ser apagado, pois faz parte do histórico do projeto;
* os números dos ADRs não deverão ser reutilizados, permitindo identificar cada decisão de forma única;
* quando a situação de uma decisão mudar, seu status deverá ser atualizado para evitar a utilização de uma orientação rejeitada, substituída ou descontinuada;
* quando uma decisão for substituída, o ADR anterior deverá indicar qual novo ADR passou a representar o cenário atual;
* toda nova decisão arquitetural relevante deverá receber um novo ADR;
* correções ortográficas e ajustes que não alterem o significado poderão ser realizados no próprio documento;
* qualquer mudança que altere o significado de uma decisão aceita deverá ser registrada em um novo ADR;
* os ADRs não deverão ser renumerados, mesmo quando existirem intervalos na sequência.

## Índice

| ADR                                    | Decisão                                | Status | Data       |
| -------------------------------------- | -------------------------------------- | ------ | ---------- |
| [ADR-0001](./0001-modular-monolith.md) | Adotar arquitetura de monólito modular | Aceita | 2026-08-24 |
