import pytest

from investfacil.dominio.ordem_de_negociacao import (
    AmbienteDeOperacao,
    DirecaoDaOrdem,
    OrdemDeNegociacao,
)


def test_criar_ordem_de_compra_em_ambiente_de_demonstracao():
    ordem = OrdemDeNegociacao(
        ativo=" winq26 ",
        direcao=DirecaoDaOrdem.COMPRA,
        quantidade_de_contratos=1,
    )

    assert ordem.ativo == "WINQ26"
    assert ordem.direcao is DirecaoDaOrdem.COMPRA
    assert ordem.quantidade_de_contratos == 1
    assert ordem.ambiente is AmbienteDeOperacao.DEMONSTRACAO


def test_rejeitar_ativo_vazio():
    with pytest.raises(ValueError, match="ativo deve ser informado"):
        OrdemDeNegociacao(
            ativo="   ",
            direcao=DirecaoDaOrdem.COMPRA,
            quantidade_de_contratos=1,
        )


@pytest.mark.parametrize(
    "quantidade_invalida",
    [0, -1, 1.5, "1", True],
)
def test_rejeitar_quantidade_de_contratos_invalida(quantidade_invalida):
    with pytest.raises(ValueError, match="inteiro maior que zero"):
        OrdemDeNegociacao(
            ativo="WINQ26",
            direcao=DirecaoDaOrdem.COMPRA,
            quantidade_de_contratos=quantidade_invalida,
        )


def test_rejeitar_direcao_invalida():
    with pytest.raises(ValueError, match="compra ou venda"):
        OrdemDeNegociacao(
            ativo="WINQ26",
            direcao="comprar",
            quantidade_de_contratos=1,
        )


def test_bloquear_operacao_em_ambiente_real():
    with pytest.raises(ValueError, match="Operacoes reais estao bloqueadas"):
        OrdemDeNegociacao(
            ativo="WINQ26",
            direcao=DirecaoDaOrdem.COMPRA,
            quantidade_de_contratos=1,
            ambiente=AmbienteDeOperacao.REAL,
        )