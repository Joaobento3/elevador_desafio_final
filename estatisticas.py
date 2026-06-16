import time
from collections import Counter

class Estatisticas:
    def __init__(self, num_elevadores: int = 2):
        self.chamadas_por_andar = Counter()
        self.distancia_total = [0] * num_elevadores
        self.tempos_espera = []

    def registrar_chamada(self, andar: int):
        self.chamadas_por_andar[andar] += 1

    def registrar_distancia(self, id_elevador: int, dist: int):
        self.distancia_total[id_elevador] += dist

    def registrar_espera(self, tempo: float):
        self.tempos_espera.append(tempo)

    def obter_resumo(self):
        andar_mais_chamado = self.chamadas_por_andar.most_common(1)[0][0] if self.chamadas_por_andar else "N/A"
        tempo_medio = sum(self.tempos_espera) / len(self.tempos_espera) if self.tempos_espera else 0

        return {
            "chamadas_por_andar": dict(self.chamadas_por_andar),
            "andar_mais_chamado": andar_mais_chamado,
            "distancia_elevadores": self.distancia_total,
            "tempo_medio_espera": tempo_medio
        }
