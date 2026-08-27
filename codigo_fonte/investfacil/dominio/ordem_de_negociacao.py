from dataclasses import dataclass
from enum import StrEnum


class DirecaoDaOrdem(StrEnum):
    COMPRA = "compra"
    VENDA = "venda"


class AmbienteDeOperacao(StrEnum):
    DEMONSTRACAO = "demonstracao"
    REAL = "real"


@dataclass(frozen=True, slots=True)
class OrdemDeNegociacao:
    ativo: str
    direcao: DirecaoDaOrdem
    quantidade_de_contratos: int
    ambiente: AmbienteDeOperacao = AmbienteDeOperacao.DEMONSTRACAO

    def __post_init__(self):
        ativo_normalizado = self.ativo.strip().upper()

        if not ativo_normalizado:
            raise ValueError("O ativo deve ser informado.")

        if (
            isinstance(self.quantidade_de_contratos, bool)
            or not isinstance(self.quantidade_de_contratos, int)
            or self.quantidade_de_contratos <= 0
        ):
            raise ValueError(
                "A quantidade de contratos deve ser um numero inteiro maior que zero."
            )

        if not isinstance(self.direcao, DirecaoDaOrdem):
            raise ValueError("A direcao deve ser compra ou venda.")

        if self.ambiente is not AmbienteDeOperacao.DEMONSTRACAO:
            raise ValueError(
                "Operacoes reais estao bloqueadas. Utilize o ambiente de demonstracao."
            )

        object.__setattr__(self, "ativo", ativo_normalizado)