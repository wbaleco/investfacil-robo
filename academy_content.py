# Academy Module Content and Quiz System
# Conteúdo educacional estruturado para o InvestFácil Academy

MODULES = {
    "fundamentos": {
        "title": "🏦 Fundamentos",
        "tag": "MÓDULO 01",
        "description": "Aprenda o que é a B3, como funciona o mini-índice e o papel da corretora.",
        "content": """
        ## O que é a B3?
        
        A **B3** (Brasil, Bolsa, Balcão) é a bolsa de valores oficial do Brasil. É onde acontecem as negociações de:
        - **Ações** de empresas
        - **Contratos Futuros** (como o Mini Índice e Mini Dólar)
        - **Opções** e outros derivativos
        
        ### Mini Índice (WIN)
        
        O **Mini Índice** é um contrato futuro que replica o Ibovespa (principal índice da bolsa brasileira). 
        
        **Características principais:**
        - Cada ponto vale **R$ 0,20**
        - Exemplo: Se o WIN está em 130.000 pontos e sobe para 130.100, você ganhou 100 pontos = R$ 20,00
        - Horário de negociação: 9h às 18h (horário de Brasília)
        - Vencimento mensal (sempre na 4ª quarta-feira do mês)
        
        ### O Papel da Corretora
        
        A **corretora** é a intermediária entre você e a B3. Ela:
        - Executa suas ordens de compra e venda
        - Cobra taxas (corretagem, emolumentos, custódia)
        - Fornece plataformas de negociação (como o MetaTrader 5)
        - Garante a segurança das suas operações
        
        **Importante:** Escolha corretoras regulamentadas pela CVM (Comissão de Valores Mobiliários).
        """,
        "quiz": [
            {
                "question": "Quanto vale cada ponto do Mini Índice (WIN)?",
                "options": ["R$ 0,10", "R$ 0,20", "R$ 1,00", "R$ 10,00"],
                "correct": 1,
                "explanation": "Cada ponto do Mini Índice vale R$ 0,20. Isso significa que uma variação de 100 pontos equivale a R$ 20,00."
            },
            {
                "question": "Qual é o horário de negociação do Mini Índice?",
                "options": ["24 horas", "9h às 18h", "10h às 17h", "8h às 20h"],
                "correct": 1,
                "explanation": "O Mini Índice é negociado das 9h às 18h (horário de Brasília), seguindo o horário da B3."
            },
            {
                "question": "Qual órgão regulamenta as corretoras no Brasil?",
                "options": ["Banco Central", "CVM", "Receita Federal", "B3"],
                "correct": 1,
                "explanation": "A CVM (Comissão de Valores Mobiliários) é o órgão responsável por fiscalizar e regulamentar o mercado de capitais brasileiro."
            }
        ]
    },
    "psicologia": {
        "title": "🧠 Psicologia",
        "tag": "MÓDULO 02",
        "description": "Gestão emocional e disciplina: a importância de não se vingar do mercado.",
        "content": """
        ## A Importância da Psicologia no Trading
        
        **90% do sucesso no trading é psicológico.** Você pode ter a melhor estratégia do mundo, mas se não controlar suas emoções, vai perder dinheiro.
        
        ### Os Maiores Inimigos do Trader
        
        1. **Ganância (Greed)**
           - Querer ganhar tudo de uma vez
           - Não respeitar o stop loss
           - Aumentar o tamanho da posição após ganhos
        
        2. **Medo (Fear)**
           - Sair de operações vencedoras cedo demais
           - Não entrar em operações por medo de perder
           - Paralisar após uma sequência de perdas
        
        3. **Vingança (Revenge Trading)**
           - **O MAIS PERIGOSO!**
           - Tentar "recuperar" perdas imediatamente
           - Dobrar o tamanho da posição após um loss
           - Operar sem estratégia, apenas por emoção
        
        ### A Regra de Ouro: Nunca se Vingue do Mercado
        
        > "O mercado não sabe que você existe. Ele não te deve nada."
        
        Quando você perde, o mercado não fez isso de propósito. Aceite a perda, analise o que aconteceu, e siga em frente. **Revenge trading** é a forma mais rápida de zerar sua conta.
        
        ### Como Manter a Disciplina
        
        - ✅ Defina sua meta diária e **pare** quando atingir
        - ✅ Defina seu stop diário e **pare** quando bater
        - ✅ Siga seu plano de trading **sempre**
        - ✅ Aceite que perdas fazem parte do jogo
        - ✅ Mantenha um diário de trades (emocional e técnico)
        """,
        "quiz": [
            {
                "question": "O que é 'Revenge Trading'?",
                "options": [
                    "Uma estratégia agressiva de lucro",
                    "Tentar recuperar perdas operando por emoção",
                    "Operar apenas após uma vitória",
                    "Um tipo de análise técnica"
                ],
                "correct": 1,
                "explanation": "Revenge Trading é quando você tenta 'se vingar' do mercado após uma perda, operando por emoção e não por estratégia. É extremamente perigoso!"
            },
            {
                "question": "Qual a porcentagem aproximada de importância da psicologia no trading?",
                "options": ["30%", "50%", "70%", "90%"],
                "correct": 3,
                "explanation": "Aproximadamente 90% do sucesso no trading está relacionado ao controle emocional e disciplina, não apenas à estratégia técnica."
            },
            {
                "question": "O que você deve fazer após atingir sua meta diária?",
                "options": [
                    "Continuar operando para ganhar mais",
                    "Parar e preservar o lucro",
                    "Dobrar o tamanho das posições",
                    "Mudar de estratégia"
                ],
                "correct": 1,
                "explanation": "Quando você atinge sua meta diária, o correto é PARAR. Preservar o lucro é mais importante do que a ganância de 'ganhar mais'."
            }
        ]
    },
    "gestao_capital": {
        "title": "🛡️ Gestão de Capital",
        "tag": "MÓDULO 03",
        "description": "A regra dos 2% e como configurar suas travas de segurança com sabedoria.",
        "content": """
        ## Gestão de Capital: A Base da Sobrevivência
        
        **Você não vai quebrar por uma operação ruim. Você vai quebrar por má gestão de risco.**
        
        ### A Regra dos 2%
        
        **Nunca arrisque mais de 2% do seu capital em uma única operação.**
        
        **Exemplo prático:**
        - Capital total: R$ 10.000
        - Risco máximo por trade: R$ 200 (2%)
        - Se seu stop loss é de 100 pontos no WIN (R$ 20), você pode operar 10 contratos
        
        ### Como Calcular o Tamanho da Posição
        
        ```
        Contratos = (Capital × 2%) ÷ (Stop Loss em pontos × R$ 0,20)
        ```
        
        **Exemplo:**
        - Capital: R$ 5.000
        - Risco: 2% = R$ 100
        - Stop Loss: 50 pontos = R$ 10 por contrato
        - Contratos = R$ 100 ÷ R$ 10 = **10 contratos**
        
        ### Configurando Suas Travas de Segurança
        
        1. **Stop Loss (por operação)**
           - Defina ANTES de entrar na operação
           - Nunca mova o stop para "dar mais espaço"
           - Use stops técnicos (abaixo de suportes, acima de resistências)
        
        2. **Stop Diário (Meta de Perda)**
           - Exemplo: Se perder R$ 200 no dia, PARE
           - Protege você de revenge trading
           - Preserve seu capital para o próximo dia
        
        3. **Meta Diária (Objetivo de Lucro)**
           - Exemplo: Ganhou R$ 500? PARE
           - Preserve o lucro conquistado
           - Evita devolver ganhos por ganância
        
        ### A Matemática da Recuperação
        
        | Perda | Ganho necessário para recuperar |
        |-------|----------------------------------|
        | 10%   | 11%                              |
        | 20%   | 25%                              |
        | 30%   | 43%                              |
        | 50%   | **100%**                         |
        | 75%   | **300%**                         |
        
        **Conclusão:** É muito mais fácil não perder do que recuperar perdas grandes!
        """,
        "quiz": [
            {
                "question": "Segundo a regra dos 2%, qual o risco máximo em uma conta de R$ 10.000?",
                "options": ["R$ 100", "R$ 200", "R$ 500", "R$ 1.000"],
                "correct": 1,
                "explanation": "2% de R$ 10.000 = R$ 200. Esse é o máximo que você deve arriscar em uma única operação."
            },
            {
                "question": "Se você perder 50% do capital, quanto precisa ganhar para recuperar?",
                "options": ["50%", "75%", "100%", "150%"],
                "correct": 2,
                "explanation": "Se você tem R$ 10.000 e perde 50% (fica com R$ 5.000), precisa ganhar 100% (dobrar) para voltar aos R$ 10.000. Por isso é crucial não ter perdas grandes!"
            },
            {
                "question": "O que você deve fazer ANTES de entrar em uma operação?",
                "options": [
                    "Definir o take profit",
                    "Definir o stop loss",
                    "Calcular o lucro esperado",
                    "Verificar o volume"
                ],
                "correct": 1,
                "explanation": "Você SEMPRE deve definir seu stop loss ANTES de entrar na operação. Isso garante que você sabe exatamente quanto está arriscando."
            }
        ]
    },
    "analise_tecnica": {
        "title": "📊 Análise Técnica",
        "tag": "MÓDULO 04",
        "description": "Entenda como o robô lê Médias Móveis e Volume para disparar os sinais.",
        "content": """
        ## Análise Técnica: A Linguagem do Mercado
        
        A análise técnica estuda o comportamento do preço através de gráficos e indicadores. **O robô usa esses mesmos princípios para tomar decisões.**
        
        ### Médias Móveis (SMA - Simple Moving Average)
        
        Uma média móvel é a média dos preços de fechamento dos últimos N períodos.
        
        **Exemplo:**
        - SMA 9 = média dos últimos 9 candles
        - SMA 21 = média dos últimos 21 candles
        
        #### Como o Robô Usa Médias Móveis
        
        **Cruzamento de Médias (Golden Cross / Death Cross):**
        - 📈 **Sinal de COMPRA:** Quando a média rápida (9) cruza a média lenta (21) para cima
        - 📉 **Sinal de VENDA:** Quando a média rápida (9) cruza a média lenta (21) para baixo
        
        **Por que funciona?**
        - A média rápida reage mais rápido às mudanças de preço
        - A média lenta filtra o "ruído" do mercado
        - O cruzamento indica mudança de tendência
        
        ### Volume
        
        O volume mostra **quantos contratos** foram negociados em cada candle.
        
        **Regra de Ouro:**
        > "Volume confirma tendência. Preço sem volume é suspeito."
        
        #### Como o Robô Usa Volume
        
        - ✅ **Volume Alto + Rompimento = Sinal Forte**
        - ❌ **Volume Baixo + Rompimento = Sinal Fraco (ignorar)**
        
        **Exemplo:**
        - Se o preço rompe uma resistência com volume 3x acima da média → **Sinal confiável**
        - Se o preço rompe com volume baixo → **Falso rompimento (provável)**
        
        ### Bollinger Bands
        
        As Bandas de Bollinger medem a **volatilidade** do mercado.
        
        **Componentes:**
        - Banda Superior = Média + (2 × Desvio Padrão)
        - Banda do Meio = Média Móvel (20)
        - Banda Inferior = Média - (2 × Desvio Padrão)
        
        **Estratégia do Robô:**
        - Quando o preço toca a banda inferior → **Possível compra (sobrevenda)**
        - Quando o preço toca a banda superior → **Possível venda (sobrecompra)**
        
        ### Suporte e Resistência
        
        - **Suporte:** Nível de preço onde a demanda (compradores) é forte
        - **Resistência:** Nível de preço onde a oferta (vendedores) é forte
        
        **O robô identifica automaticamente:**
        - Máximas e mínimas recentes
        - Rompimentos de níveis importantes
        - Zonas de consolidação
        """,
        "quiz": [
            {
                "question": "O que indica um 'Golden Cross'?",
                "options": [
                    "Média rápida cruza a lenta para baixo",
                    "Média rápida cruza a lenta para cima",
                    "Volume acima da média",
                    "Preço toca a banda superior"
                ],
                "correct": 1,
                "explanation": "Golden Cross é quando a média móvel rápida (ex: 9) cruza a média lenta (ex: 21) para CIMA, indicando possível tendência de alta."
            },
            {
                "question": "Por que o volume é importante?",
                "options": [
                    "Ele define o preço do ativo",
                    "Ele confirma a força de um movimento",
                    "Ele substitui a análise de preço",
                    "Ele não é importante"
                ],
                "correct": 1,
                "explanation": "O volume confirma a força de um movimento. Um rompimento com volume alto é mais confiável do que um com volume baixo."
            },
            {
                "question": "O que acontece quando o preço toca a banda inferior de Bollinger?",
                "options": [
                    "É um sinal de venda",
                    "É um sinal de compra (sobrevenda)",
                    "Não significa nada",
                    "O mercado vai fechar"
                ],
                "correct": 1,
                "explanation": "Quando o preço toca a banda inferior, indica que o ativo pode estar sobrevendido, sendo uma possível oportunidade de compra."
            }
        ]
    }
}
