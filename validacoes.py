from typing import List

ANDARES_VALIDOS = [-2, -1, 0, 1, 2, 3, 4]

def validar_andar(andar: int) -> bool:#valida se o andar está dentro do intervalo permitido
    return andar in ANDARES_VALIDOS

def formatar_andar(andar: int) -> str:
    mapeamento = {-2: "Subsolo 2", -1: "Subsolo 1", 0: "Térreo"}
    return mapeamento.get(andar, f"{andar}º Andar")