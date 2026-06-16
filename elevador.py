import time
from validacoes import formatar_andar

class Elevador:
    def __init__(self, id_elevador: int):
        self.id = id_elevador
        self.posicao = 0
        self.ocupado = False
        self.direcao = None

    def mover_para(self, destino: int, estatisticas):
        dist = abs(self.posicao - destino)
        estatisticas.registrar_distancia(self.id, dist)

        while self.posicao != destino:
            self.direcao = "Subindo" if destino > self.posicao else "Descendo"
            self.posicao += 1 if self.direcao == "Subindo" else -1
            print(f"  [Elevador {self.id}] 🛗 {self.direcao}... {formatar_andar(self.posicao)}")
            time.sleep(0.4)

        self.direcao = None
        print(f"  [Elevador {self.id}] ✅ Chegou ao {formatar_andar(destino)}!")
        return True
