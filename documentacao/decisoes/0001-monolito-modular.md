# ADR-0001: Adotar arquitetura de monólito modular

## Status

Aceita

## Data

2026-08-24

## Contexto

O InvestFácil possui duas frentes principais:

* **InvestFácil Academia:** voltada à educação sobre mercado financeiro, gestão de risco, estratégias e funcionamento do sistema;
* **InvestFácil Robô:** voltada à pesquisa, simulação histórica, simulação e automação de operações.

Na versão inicial, a interface, as estratégias, a conexão com o MetaTrader 5, o aprendizado de máquina e parte das regras de negócio estão concentrados em poucos arquivos Python localizados na raiz do projeto.

Essa estrutura foi suficiente para a criação do protótipo, mas dificulta:

* a separação entre regras de negócio e infraestrutura;
* a execução de testes automatizados;
* a reutilização das estratégias de simulação histórica;
* a substituição do MetaTrader 5 por um simulador;
* - a evolução independente da Academia e do Robô;
* a aplicação consistente das regras de segurança;
* a manutenção e compreensão do código.

Também existe o risco de as estratégias dependerem diretamente do MetaTrader 5, impossibilitando sua validação isolada.

## Decisão

O InvestFácil adotará inicialmente uma arquitetura de **monólito modular**.

O sistema permanecerá em um único repositório, mas seu código será separado em módulos com responsabilidades bem definidas:

- `aplicacoes`: interfaces executáveis da Academia e do Painel Operacional;
- `dominio`: entidades e regras puras de negócio;
- `aplicacao`: casos de uso e coordenação das operações;
- `infraestrutura`: integrações com MetaTrader 5, banco de dados, arquivos e serviços externos;
- `simulacao_historica`: simulação histórica e cálculo de métricas;
- `aprendizado_de_maquina`: treinamento, avaliação e utilização experimental de modelos;
- `testes`: testes unitários, de integração e de simulação histórica;
- `documentacao`: documentação técnica e registro das decisões.

As regras do domínio não deverão depender diretamente de:

* MetaTrader 5;
* Streamlit;
* banco de dados;
* arquivos CSV;
* APIs externas;
* bibliotecas de interface.

As integrações externas deverão ser acessadas por contratos definidos pela aplicação e implementados pela infraestrutura.

## Motivos

A arquitetura de monólito modular foi escolhida porque:

* oferece separação profissional de responsabilidades;
* facilita o aprendizado gradual de backend e arquitetura;
* permite testar estratégias sem conexão com o MetaTrader 5;
* possibilita utilizar as mesmas regras na simulação histórica testing e na conta demo;
* reduz o acoplamento entre interface, estratégias e execução;
* possui menor complexidade operacional do que microserviços;
* permite evolução incremental sem descartar o protótipo atual.

## Alternativas consideradas

### Manter a estrutura atual

Rejeitada porque o acoplamento entre interface, estratégia e infraestrutura dificulta testes, manutenção e evolução segura.

### Reescrever todo o sistema de uma vez

Rejeitada porque aumentaria o risco de perda de funcionalidades e dificultaria a identificação de erros durante a migração.

A refatoração será incremental: cada módulo será migrado, testado e validado separadamente.

### Adotar microserviços

Rejeitada nesta fase porque introduziria complexidade adicional de comunicação, implantação, monitoramento e gerenciamento de dados sem benefício proporcional ao estágio atual do projeto.

Microserviços poderão ser reconsiderados se surgirem necessidades reais de escalabilidade, implantação independente ou separação de equipes.

## Consequências positivas

* melhor organização do código;
* responsabilidades mais claras;
* estratégias testáveis isoladamente;
* menor dependência do MetaTrader 5;
* maior segurança na execução de operações;
* possibilidade de substituir componentes de infraestrutura;
* documentação alinhada ao código;
* evolução gradual para uma API e interface web;
* base adequada para simulação histórica e validação estatística.

## Consequências negativas

* necessidade de refatorar o código existente;
* coexistência temporária da estrutura antiga com a nova;
* maior quantidade inicial de pastas e módulos;
* necessidade de compreender os limites de cada camada;
* aumento do trabalho de documentação e testes.

## Restrições de segurança

A adoção desta arquitetura não representa aprovação das estratégias existentes.

Durante a versão 0.2:

* operações em conta real permanecerão bloqueadas;
* somente conta demo poderá ser utilizada;
* nenhuma estratégia será considerada lucrativa sem validação estatística;
* o aprendizado de máquina será tratado como componente experimental;
* nenhuma estratégia poderá enviar ordens diretamente;
* toda ordem deverá passar pelo módulo de gestão de risco;
* a liberação de uma estratégia dependerá de simulação histórica e critérios documentados.

## Plano de migração

A migração seguirá uma abordagem incremental:

1. criar a estrutura da nova arquitetura;
2. documentar responsabilidades e nomenclaturas;
3. configurar o projeto Python;
4. criar as primeiras entidades do domínio;
5. definir contratos para dados de mercado e execução;
6. isolar a integração com o MetaTrader 5;
7. migrar uma estratégia por vez;
8. criar testes unitários;
9. implementar o motor de simulação histórica;
10. validar as estratégias estatisticamente;
11. liberar exclusivamente a operação em conta demo.

## Critérios de revisão

Esta decisão poderá ser revisada quando ocorrer pelo menos uma das seguintes situações:

* necessidade comprovada de implantação independente de módulos;
* aumento significativo da equipe de desenvolvimento;
* exigência de escalabilidade independente;
* limitação técnica comprovada do monólito modular;
* necessidade de separar produtos ou serviços em repositórios distintos.

Uma revisão deverá ser registrada em um novo ADR. Este documento não deverá ser apagado, pois faz parte do histórico do projeto.
